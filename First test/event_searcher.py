import json
import time
import re
from duckduckgo_search import DDGS
import google.generativeai as genai
from agent_config import GEMINI_API_KEY, MODEL_NAME, GENERATION_CONFIG

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

def clean_json_string(text):
    """Robustly extracts JSON from a string."""
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```', '', text)
    return text.strip()

def search_events_web():
    """Searches the web for events using DuckDuckGo."""
    events_text = ""
    # Use current and next year for search context
    years = f"{time.strftime('%Y')} {int(time.strftime('%Y'))+1}"
    
    with DDGS() as ddgs:
        # Reduced to 1 keyword to save tokens/time for the test
        queries = [f"Microfluidics conferences {years}", f"Nanomaterials workshops {years}"]
        
        for query in queries:
            print(f"  -> Querying DuckDuckGo: {query}")
            try:
                results = ddgs.text(query, max_results=3)
                if results:
                    for r in results:
                        events_text += f"Title: {r.get('title')}\nSnippet: {r.get('body')}\nLink: {r.get('href')}\n\n"
            except Exception as e:
                print(f"  ! Error searching events: {e}")
                
    return events_text

def extract_events_with_llm(text_data):
    """
    Uses Gemini to structure the raw search text.
    INCLUDES RETRY LOGIC FOR 429 ERRORS.
    """
    if not text_data:
        return []

    prompt = f"""
    You are an event extraction assistant.
    Extract a list of academic conferences, workshops, or webinars from the text below.
    Ignore general news or ads.
    
    Text Data:
    {text_data}
    
    Output strictly valid JSON:
    [
      {{
        "title": "Name of event",
        "date": "Date string",
        "location": "City/Country or Online",
        "description": "Short summary"
      }}
    ]
    """

    model = genai.GenerativeModel(
        MODEL_NAME, 
        generation_config=GENERATION_CONFIG
    )

    # --- RETRY LOGIC START ---
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            clean_text = clean_json_string(response.text)
            return json.loads(clean_text)
            
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "Quota" in error_msg:
                wait_time = 15 * (attempt + 1) # Wait 15s, 30s...
                print(f"  ⚠️ Quota Hit (429) on Events. Waiting {wait_time}s to cooldown...")
                time.sleep(wait_time)
            else:
                print(f"  ! Error extracting events: {e}")
                break # Non-quota error, stop trying
    # --- RETRY LOGIC END ---
    
    return []

def find_and_analyze_events():
    """Main function to run the event search workflow."""
    print("  -> Searching web for raw event data...")
    raw_text = search_events_web()
    
    if not raw_text:
        print("  -> No raw event data found.")
        return []
        
    print("  -> Extracting structured data using AI...")
    structured_events = extract_events_with_llm(raw_text)
    
    print(f"✅ Found {len(structured_events)} relevant events.")
    return structured_events

if __name__ == "__main__":
    events = find_and_analyze_events()
    print(json.dumps(events, indent=2))