import os
import json
import time
import base64
import requests
import google.generativeai as genai
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

import config
import database
import utils

# --- CONFIGURATION ---
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
database.init_db()

# --- 1. OPENALEX FETCHER ---
def fetch_papers(filters):
    date_filter = (datetime.now() - timedelta(days=config.DAYS_LOOKBACK)).strftime("%Y-%m-%d")
    filter_str = ",".join(filters)
    url = f"https://api.openalex.org/works?filter=from_publication_date:{date_filter},{filter_str}&per-page=50&select=id,title,doi,abstract_inverted_index"
    
    try:
        return requests.get(url).json().get('results', [])
    except:
        return []

# --- 2. GEMINI FILTER ---
def analyze_paper(paper, prompt):
    abstract = utils.reconstruct_abstract(paper.get('abstract_inverted_index'))
    full_prompt = f"{prompt}\n\nPAPER: {paper['title']}\nABSTRACT: {abstract}\n\nOUTPUT JSON: {{ \"score\": 0-10, \"novelty\": \"1 sentence summary\" }}"
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(full_prompt, generation_config={"response_mime_type": "application/json"})
        return json.loads(res.text)
    except:
        return {"score": 0}

# --- 3. GMAIL SENDER (HEADLESS) ---
def send_email(report_html):
    # Reconstruct credentials from GitHub Secrets
    creds = Credentials(
        None, # No access token (refresh will fetch it)
        refresh_token=os.getenv("GMAIL_REFRESH_TOKEN"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv("GMAIL_CLIENT_ID"),
        client_secret=os.getenv("GMAIL_CLIENT_SECRET")
    )
    
    service = build('gmail', 'v1', credentials=creds)
    message = MIMEText(report_html, 'html')
    message['to'] = os.getenv("EMAIL_RECIPIENT")
    message['subject'] = f"🔬 Scientific Update: {datetime.now().strftime('%Y-%m-%d')}"
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    
    service.users().messages().send(userId="me", body={'raw': raw}).execute()

# --- MAIN LOOP ---
def main():
    report_content = "<h1>🔬 Daily Scientific Digest</h1>"
    has_news = False
    
    for session in config.SESSIONS:
        print(f"Checking {session['title']}...")
        papers = fetch_papers(session['api_filters'])
        
        session_html = f"<h2>{session['title']}</h2><ul>"
        count = 0
        
        for p in papers:
            if not database.is_new(p['id']): continue
            
            analysis = analyze_paper(p, session['system_prompt'])
            if analysis['score'] >= config.MIN_RELEVANCE_SCORE:
                link = p.get('doi') or "#"
                session_html += f"<li><b>[{analysis['score']}/10] <a href='{link}'>{p['title']}</a></b><br><i>{analysis['novelty']}</i></li>"
                count += 1
                time.sleep(1) # Rate limit respect
        
        session_html += "</ul>"
        if count > 0:
            report_content += session_html
            has_news = True
            
    if has_news:
        print("Sending Email...")
        send_email(report_content)
    else:
        print("No new relevant papers today.")

if __name__ == "__main__":
    main()