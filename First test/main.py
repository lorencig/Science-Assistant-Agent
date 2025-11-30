import sys
import argparse
import time # Need this for sleep
from searcher import search_papers
from event_searcher import find_and_analyze_events 
from analyzer import analyze_batch
from reporter import generate_report

def main():
    parser = argparse.ArgumentParser(description="AI Science Agent - The Curious Scout")
    parser.add_argument("--days", type=int, default=7, help="Number of days to look back for papers")
    parser.add_argument("--skip-events", action="store_true", help="Skip event search")
    args = parser.parse_args()
    
    print("🚀 Starting AI Science Agent: The Curious Scout (Safe Mode)")
    
    # 1. Search for Papers
    print(f"\n🔎 PHASE 1: Searching for papers...")
    papers = search_papers(days_back=args.days)
    
    analyzed_papers = []
    if not papers:
        print("No papers found matching criteria.")
    else:
        # 2. Analyze Papers (Now slower/safer)
        print(f"\n🧠 PHASE 2: Analyzing {len(papers)} papers...")
        analyzed_papers = analyze_batch(papers)
    
    # --- BREATHING ROOM ---
    if not args.skip_events:
        print("\n☕ Taking a 10-second break to let APIs cool down...")
        time.sleep(10)

        # 3. Search for Events
        print("\n🌍 PHASE 3: Searching for events...")
        events = find_and_analyze_events()
    else:
        events = []
        
    # 4. Generate Report
    print("\n📝 PHASE 4: Generating Report...")
    report_file = generate_report(analyzed_papers, events)
    
    print(f"\n✅ Done! Report saved to: {report_file}")

if __name__ == "__main__":
    main()