import google.generativeai as genai
import requests
import os
from agent_config import GEMINI_API_KEY

print("--- 1. CHECKING GEMINI MODELS ---")
try:
    genai.configure(api_key=GEMINI_API_KEY)
    print(f"API Key found: {GEMINI_API_KEY[:5]}...****")
    
    print("Listing available models...")
    found_flash = False
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f" - {m.name}")
            if "flash" in m.name:
                found_flash = True
    
    if found_flash:
        print("\n✅ Success: Flash model is available!")
    else:
        print("\n⚠️ Warning: Flash model NOT found in your list. Use 'gemini-1.5-pro' instead.")

except Exception as e:
    print(f"❌ Gemini Error: {e}")

print("\n--- 2. CHECKING SEMANTIC SCHOLAR ---")
try:
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {"query": "Microfluidics", "limit": 1}
    print(f"Pinging {url}...")
    r = requests.get(url, params=params, timeout=10)
    
    if r.status_code == 200:
        print("✅ Success: Semantic Scholar is reachable.")
        data = r.json()
        print(f"   Result: {data['data'][0]['title']}")
    elif r.status_code == 429:
        print("⚠️ Rate Limited (429). You are temporarily blocked. Wait 5 minutes.")
    else:
        print(f"❌ Error: Status {r.status_code}")
        
except Exception as e:
    print(f"❌ Network Error: {e}")