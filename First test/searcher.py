import json
import time
import re
from duckduckgo_search import DDGS
import google.generativeai as genai

from agent_config import (
    KEYWORDS, 
    GEMINI_API_KEY, 
    MODEL_NAME, 
    GENERATION_CONFIG
)

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

def clean_json_string(text):
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```', '', text)
    return text.strip()

def search_web_for_papers(days_back=30):
    """
    DEBUG MODE: Searches DuckDuckGo WITHOUT any time limits.
    This ensures we get results even if recent papers are scarce.
    """
    results_text = ""
    
    # DEBUG: We force timelimit to None to search "All Time"
    print(f"  -> 🔧 DEBUG MODE: Time filter REMOVED. Searching all history...")

    with DDGS() as ddgs:
        for keyword in KEYWORDS:
            # Broad query to catch any relevant academic content
            query = f'"{keyword}" (research paper OR journal article)'
            
            print(f"  -> 🦆 Web Search: {query}")
            
            try:
                # timelimit=None means "Any time"
                search_results = ddgs.text(
                    query, 
                    timelimit=None, 
                    max_results=5
                )
                
                if search_results:
                    for r in search_results:
                        results_text += f"Title: {r.get('title')}\nSnippet: {r.get('body')}\nLink: {r.get('href')}\n\n"
                        
            except Exception as e:
                print(f"  ! Error querying DuckDuckGo: {e}")
                time.sleep(1)

    return results_text

def extract_papers_with_llm(raw_text):
    """
    Uses Gemini to look at the raw search results and turn them into structured Paper objects.
    """
    if not raw_text:
        return []

    print("  -> 🧠 AI is reading search results to identify valid papers...")

    prompt = f"""
    You are a Research Assistant. I have performed a web search for scientific papers.
    Below is the raw text from the search results.
    
    Task:
    1. Identify items that look like **Academic Research Papers** or **Reviews**.
    2. Ignore general news, blogs, or ads.
    3. Extract the Title, Venue (Journal name), and a short Abstract/Summary from the snippet.
    4. IF the Venue is not explicitly clear, try to infer it from the link (e.g., nature.com -> Nature).

    Raw Search Data:
    {raw_text}

    Output strictly valid JSON in this format:
    [
      {{
        "title": "Paper Title",
        "venue": "Journal Name",
        "abstract": "Summary of what the paper is about based on the snippet",
        "url": "Link",
        "date": "YYYY-MM-DD" 
      }}
    ]
    """

    model = genai.GenerativeModel(
        MODEL_NAME, 
        generation_config=GENERATION_CONFIG
    )

    try:
        response = model.generate_content(prompt)
        clean_text = clean_json_string(response.text)
        return json.loads(clean_text)
    except Exception as e:
        print(f"  ! AI Parsing Error: {e}")
        return []

def search_papers(days_back=7):
    """
    Main entry point compatible with main.py
    """
    print(f"🔎 Scanning the web for papers (DEBUG: All Time)...")
    
    # We ignore the 'days_back' argument for this debug run
    raw_text = search_web_for_papers()
    
    if not raw_text:
        print("  -> No search results found.")
        return []

    papers = extract_papers_with_llm(raw_text)
    
    print(f"✅ AI identified {len(papers)} potential papers.")
    return papers

if __name__ == "__main__":
    # Test Run
    results = search_papers()
    print(json.dumps(results, indent=2))