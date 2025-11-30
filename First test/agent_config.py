import os

# --- API KEYS ---
# Try to get from environment variables first (Best Practice)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SEMANTIC_SCHOLAR_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY") 

# FALLBACK: Only if environment variable is missing (Keep this local only!)
if not GEMINI_API_KEY:
    # Replace this string with your actual key for local testing
    GEMINI_API_KEY = "AIzaSyBYZi_niKBYKBE-HjLk_3lVZUiPChJcVEw" 

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing! Set it in env vars or agent_config.py")

# --- MODEL CONFIGURATION ---
# We use Flash for speed and higher rate limits, or Pro for deep reasoning.
# 2.5/3 does not exist yet publically, use 1.5 versions.
MODEL_NAME = "models/gemini-2.5-flash" 

GENERATION_CONFIG = {
    "temperature": 0.2,
    "response_mime_type": "application/json"
}

# --- SEARCH CONFIGURATION ---
KEYWORDS = [
    "Microfluidics",
    "Millifluidics",
    "Continuous Flow",
    "Nanomaterials"
]

EVENT_KEYWORDS = [
    "Conference",
    "Workshop",
    "Summer School",
    "Symposium",
    "Call for Papers"
]

# --- FILTERING CONFIGURATION ---
# Hard Exclusions (Bio/Medical/Purely Analytical)
EXCLUSIONS = [
    "Organ-on-Chip",
    "Bio-MEMS",
    "Tissue Engineering",
    "Drug Toxicity",
    "Cell Culture",
    "In vivo",
    "Clinical"
]

# High Impact Factor Journal Whitelist
JOURNAL_WHITELIST = [
    "Nature",
    "Science",
    "Nature Communications",
    "Science Advances",
    "JACS",
    "Journal of the American Chemical Society",
    "Angewandte Chemie",
    "Advanced Materials",
    "ACS Nano",
    "Nano Letters",
    "Small",
    "Lab on a Chip",
    "Reaction Chemistry & Engineering",
    "Chemical Engineering Journal",
    "Chemistry of Materials",
    "Advanced Functional Materials"
]

# --- LLM PROMPTS ---
SYSTEM_INSTRUCTION = """
You are a Research Scout for a PhD project on "Fluidic Synthesis of Inorganic Nanomaterials."
Your role is to be a "Curious Scout". You look for connections.
If a technology is used in a different field (e.g., organic synthesis) but could solve a problem in inorganic synthesis (e.g., clogging, mixing speed), you CAPTURE it.

You will receive an abstract and title. You must classify it into one of the following tiers:

TIER 1: THE CORE (Deep Dive)
Criteria: Novel Fluidic Synthesis of Inorganic Materials (Metals, Oxides, QDs, Perovskites) OR Novel Hardware expressly for this purpose.

TIER 2: CROSS-POLLINATION (The "Curious" Finds)
Criteria: Interesting hardware used for ORGANIC chemistry that could be adapted. New inline sensors tested on simple fluids. Novel physics (acoustics, magnetics) used for separation.

TIER 3: THE LANDSCAPE (Brief List)
Criteria: Standard synthesis papers or Reviews.

EXCLUDE:
- Organ-on-Chip / Bio-MEMS (unless purely physical fluidic innovation)
- Purely Analytical (offline characterization only)
"""

ANALYSIS_PROMPT = """
Analyze the following paper:
Title: {title}
Abstract: {abstract}

1. Does this paper fall under "Hard Exclusions" (Organ-on-Chip, Bio-MEMS, Purely Analytical)?
2. If NOT excluded, which Tier does it belong to? (Tier 1, Tier 2, Tier 3)
3. Extract the following based on the Tier:
   - Tier 1: Innovation, The Process, Key Insight.
   - Tier 2: Tech, Relevance (Why is it useful for inorganic synthesis?).
   - Tier 3: Gist (1 sentence).

Output strictly in JSON format matching this schema:
{{
  "excluded": boolean,
  "tier": 1 | 2 | 3 | null,
  "reason_for_exclusion": "string" | null,
  "analysis": {{
    "innovation": "string" | null,
    "process": "string" | null,
    "insight": "string" | null,
    "tech": "string" | null,
    "relevance": "string" | null,
    "gist": "string" | null
  }}
}}
"""