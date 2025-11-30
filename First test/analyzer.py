import json
import time
import re
import google.generativeai as genai

# Import Config
from agent_config import (
    GEMINI_API_KEY, 
    SYSTEM_INSTRUCTION, 
    ANALYSIS_PROMPT, 
    MODEL_NAME, 
    GENERATION_CONFIG
)

genai.configure(api_key=GEMINI_API_KEY)

def clean_json_string(text):
    """Robustly cleans Markdown wrapper from JSON."""
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```', '', text)
    return text.strip()

def analyze_paper(paper):
    """
    Analyzes a single paper.
    """
    title = paper.get('title', 'Unknown Title')
    abstract = paper.get('abstract', '')
    
    if not abstract:
        return {'excluded': True, 'reason_for_exclusion': 'No abstract'}
        
    prompt = ANALYSIS_PROMPT.format(title=title, abstract=abstract)
    
    model = genai.GenerativeModel(
        MODEL_NAME, 
        system_instruction=SYSTEM_INSTRUCTION,
        generation_config=GENERATION_CONFIG
    )
    
    # Retry Logic
    for attempt in range(3):
        try:
            response = model.generate_content(prompt)
            clean_text = clean_json_string(response.text)
            return json.loads(clean_text)
        except Exception as e:
            if "429" in str(e) or "Quota" in str(e):
                print(f"    ⚠️ Quota hit. Cooling down for 10s...")
                time.sleep(10)
            else:
                print(f"    ! Error analyzing '{title[:20]}...': {e}")
                break

    return {'excluded': True, 'reason_for_exclusion': 'Analysis Failed'}

def analyze_batch(papers):
    """
    SLOW & STEADY MODE:
    Processes papers one by one with a delay to respect rate limits.
    """
    analyzed_papers = []
    total = len(papers)
    
    print(f"  -> Processing {total} papers sequentially (Safe Mode)...")
    
    for i, paper in enumerate(papers):
        # 1. Analyze
        print(f"    [{i+1}/{total}] Analyzing: {paper['title'][:40]}...")
        analysis_result = analyze_paper(paper)
        
        # 2. Merge Data
        paper_data = paper.copy()
        paper_data.update(analysis_result)
        
        if not paper_data.get('excluded'):
            analyzed_papers.append(paper_data)
            print(f"      + Captured (Tier {paper_data.get('tier')})")
        else:
            print(f"      - Excluded")

        # 3. SAFETY SLEEP
        # Wait 4 seconds between papers. This keeps you under ~15 requests/minute
        time.sleep(4)
                
    return analyzed_papers