🔬 Daily Research Intelligence AgentA "Set-and-Forget" Autonomous Research Assistant.I built this agent because I was tired of drowning in RSS feeds and missing critical papers in my niche fields (Flow Chemistry & Nanomaterials). Traditional keyword alerts are too noisy, and manual searching is too slow.This tool runs automatically in the cloud every morning. It scans global scientific output, reads the abstracts using a Large Language Model (Google Gemini), and emails me a curated digest of only the papers that actually matter.🏗️ ArchitectureThe system follows a "Funnel Architecture" to balance cost, speed, and accuracy. Unlike fragile web scrapers that break when Google Scholar changes its layout, this system uses a robust, open data pipeline:The Wide Net (OpenAlex API): The agent queries OpenAlex, a massive open catalog of over 250 million scholarly works.It scans titles, abstracts, and full-text data.It uses broad boolean logic (e.g., "Flow Chemistry" OR "Microfluidics") to ensure no relevant paper is missed due to missing specific keywords.It fetches papers published in the last 7 days to capture the latest research.The Memory (SQLite): It checks a local database (seen_papers.db) to ensure I never see the same paper twice, even if the search window overlaps.The Brain (Gemini 2.5): Relevant abstracts are sent to Google's Gemini model. The AI acts as a "Reviewer," scoring the paper from 0-10 based on strict scientific criteria I defined (e.g., "Must be inorganic nanoparticles," "Reject biological reviews").The Delivery (Gmail): If (and only if) high-scoring papers are found, it composes an HTML briefing and sends it to my inbox via the Gmail API.🚀 Installation & Local SetupIf you want to run this on your own machine for testing:Clone the repository:git clone [https://github.com/lorencig/AGENT.git](https://github.com/lorencig/AGENT.git)
cd AGENT
Install dependencies:pip install -r requirements.txt
Configure Environment:Create a .env file in the root directory. You will need your API keys here (see the Appendix for how to get the Gmail token).GEMINI_API_KEY="your_google_ai_studio_key"
EMAIL_RECIPIENT="your_email@gmail.com"

# Gmail OAuth Credentials
GMAIL_CLIENT_ID="your_client_id"
GMAIL_CLIENT_SECRET="your_client_secret"
GMAIL_REFRESH_TOKEN="your_refresh_token"
Run the Agent:python main.py
⚙️ CustomizationThe logic for what papers get selected is entirely contained in config.py. I designed it to be modular so you can track multiple different research "Sessions".To change what the agent looks for, edit the SESSIONS list:{
    "id": "my_new_topic",
    "title": "🧬 Genomic Sequencing",
    "api_filters": [
        # Broad keywords for the API
        'default.search:("genomics" OR "CRISPR")'
    ],
    "system_prompt": """
    ROLE: Senior Geneticist.
    TASK: Score papers on novel CRISPR off-target detection methods.
    SCORING: 10 for wet-lab validation, 0 for pure reviews.
    """
}
☁️ Deployment (GitHub Actions)This project is designed to run serverless using GitHub Actions. It runs entirely free of charge on the standard tier.The workflow is defined in .github/workflows/daily_digest.yml. It is scheduled to run every day at 07:00 UTC.To deploy:Push your code to GitHub.Go to Settings > Secrets and variables > Actions.Add the 5 secrets from your .env file (GEMINI_API_KEY, GMAIL_REFRESH_TOKEN, etc.).The bot will automatically wake up tomorrow morning.📚 Appendix: Generating the Gmail TokenTo allow the script to send emails on my behalf without storing my actual password (which is insecure) or requiring a browser login every time (which breaks on servers), I use OAuth 2.0 with a Refresh Token.Here is the one-time setup I used to generate this credentials chain:Google Cloud Console:I created a new project in the Google Cloud Console.Enabled the Gmail API.Created OAuth 2.0 Credentials (Type: Desktop App) and downloaded the credentials.json file.Crucial: I set the App Status to "Production" (Publish App) to prevent the token from expiring every 7 days.Token Generation Script:I wrote a helper tool included in this repo to handle the handshake.Place credentials.json in the tools/ folder.Run the script:python tools/get_gmail_token.py
This opens a browser window to authorize the app.Final Step:The script prints a GMAIL_REFRESH_TOKEN to the terminal. I saved this token (along with the Client ID and Secret) into my .env file (locally) and GitHub Secrets (for production).Data Sources & CreditsOpenAlex: Used for the bibliographic data. OpenAlex is a fully open catalog of the global research system, replacing the need for fragile web scrapers.Google Gemini: Used for the reasoning and filtering engine.
