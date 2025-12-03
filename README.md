
# 🔬 Daily Research Intelligence Agent

**A "Set-and-Forget" Autonomous Research Assistant.**

I built this agent because I didn't want to miss critical papers in niche fields (e.g., *Flow Chemistry* & *Nanomaterials*). Traditional keyword alerts are too noisy, and manual searching is too slow.

This tool runs automatically (for me, every 15 days). It scans global scientific output, reads the abstracts using a Large Language Model (Google Gemini), and emails a curated digest of only the papers that actually matter.

---

## 🏗️ Architecture

The system follows a **"Funnel Architecture"** to balance cost, speed, and accuracy. Unlike fragile web scrapers that break when Google Scholar changes its layout, this system uses a robust, open data pipeline.


### The 4-Step Pipeline

1.  **The Wide Net (OpenAlex API):**
    * Queries OpenAlex, a massive open catalog of over 250 million scholarly works.
    * Uses broad boolean logic (e.g., `"Flow Chemistry" OR "Microfluidics"`) to ensure zero relevant papers are missed.
    * Fetches papers from the last days to capture the latest output.

2.  **The Memory (SQLite):**
    * Checks a local database (`seen_papers.db`) to ensure you never see the same paper twice, even if search windows overlap.

3.  **The Brain (Gemini 2.5):**
    * Relevant abstracts are sent to Google's Gemini model.
    * The AI acts as a **"Reviewer,"** scoring the paper from 0-10 based on strict scientific criteria defined in the config (e.g., *"Must be inorganic nanoparticles,"* *"Reject biological reviews"*).

4.  **The Delivery (Gmail):**
    * If (and only if) high-scoring papers are found, it composes a rich HTML briefing and sends it to your inbox via the Gmail API.

---

## 🚀 Installation & Local Setup

Follow these steps to run the agent on your own machine for testing.

### 1. Clone the repository
```bash
git clone [https://github.com/lorencig/AGENT.git](https://github.com/lorencig/AGENT.git)
cd AGENT
````

### 2\. Install dependencies

```bash
pip install -r requirements.txt
```

### 3\. Configure Environment & Secrets

Option A: For Local Testing Create a `.env` file in the root directory: 

```bash
GEMINI_API_KEY="your_google_ai_studio_key"
EMAIL_RECIPIENT="your_email@gmail.com"

# Gmail OAuth Credentials
GMAIL_CLIENT_ID="your_client_id"
GMAIL_CLIENT_SECRET="your_client_secret"
GMAIL_REFRESH_TOKEN="your_refresh_token"
```
Option B: For GitHub Actions (Production) To make this run automatically in the cloud, you must store these keys in GitHub's secure vault:
   * Go to your repository on GitHub.
   * Navigate to Settings > Secrets and variables > Actions.
   * Click New repository secret.
   * Add each of the 5 variables listed above (GEMINI_API_KEY, GMAIL_REFRESH_TOKEN, etc.) individually.
  
### 4\. Run the Agent (Locally)

```bash
python main.py
```

-----

## ⚙️ Customization

The logic for what papers get selected is entirely contained in `config.py`. The system is modular, allowing you to track multiple different research "Sessions" simultaneously.

To change what the agent looks for, edit the `SESSIONS` list:

```python
{
    "id": "my_new_topic",
    "title": "🧬 Genomic Sequencing",
    "api_filters": [
        # Broad keywords for the OpenAlex API
        'default.search:("genomics" OR "CRISPR")'
    ],
    "system_prompt": """
    ROLE: Senior Geneticist.
    TASK: Score papers on novel CRISPR off-target detection methods.
    SCORING: 10 for wet-lab validation, 0 for pure reviews.
    """
}
```

-----

## ☁️ Deployment (GitHub Actions)

This project is designed to run serverless using **GitHub Actions**. It runs entirely free of charge on the standard tier.

The workflow is defined in `.github/workflows/daily_digest.yml` and is scheduled on the 1st and 15th of every month at **07:00 UTC**.

**To deploy:**

1.  Push your code to GitHub.
2.  Go to your repository **Settings \> Secrets and variables \> Actions**.
3.  Add the 5 secrets from your `.env` file (`GEMINI_API_KEY`, `GMAIL_REFRESH_TOKEN`, etc.).
4.  The bot will automatically wake up on the next scheduled run.

-----

## 📚 Appendix: Generating the Gmail Token

To allow the script to send emails without storing your password (insecure) or requiring a browser login every time (breaks on servers), use **OAuth 2.0 with a Refresh Token**.

**1. Google Cloud Console Setup:**

  * Create a new project in the [Google Cloud Console](https://console.cloud.google.com/).
  * Enable the **Gmail API**.
  * Create **OAuth 2.0 Credentials** (Type: Desktop App) and download the `credentials.json` file.
  * **Crucial:** Set the App Status to **"Production" (Publish App)** in the OAuth consent screen settings to prevent the token from expiring every 7 days.

**2. Token Generation Script:**

  * Place `credentials.json` in the `tools/` folder.
  * Run the helper script included in this repo:

<!-- end list -->

```bash
python tools/get_gmail_token.py
```

  * This opens a browser window to authorize the app.
  * The script will print a `GMAIL_REFRESH_TOKEN` to the terminal. Save this token, along with your Client ID and Secret, into your `.env` file (locally) and GitHub Secrets (for production).

-----

## Data Sources & Credits

  * **[OpenAlex](https://openalex.org/):** Used for bibliographic data. OpenAlex is a fully open catalog of the global research system.
  * **[Google Gemini](https://deepmind.google/technologies/gemini/):** Used for the reasoning and filtering engine.

<!-- end list -->

```

***

### Next Step
Would you like me to generate the **Python code for the `tools/get_gmail_token.py` script** mentioned in the Appendix, so you can include it in the repository immediately?
```
