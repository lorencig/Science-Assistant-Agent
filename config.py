import os

# --- 1. GLOBAL SETTINGS ---

DAYS_LOOKBACK = 15
MIN_RELEVANCE_SCORE = 6

# --- 2. SESSIONS (The "Wide Funnel" Production Config) ---

SESSIONS = [

    # -----------------------------------------------------------
    # 1. Flow Synthesis & Post-Processing
    # -----------------------------------------------------------
    {
        "id": "flow_synthesis",
        "title": "⚗️ Flow Synthesis, Coating & Assembly",
        "api_filters": [
            'default.search:("flow chemistry" OR "microfluidics" OR "microreactor" OR "continuous flow" OR "droplet microfluidics") AND ("nanoparticle" OR "iron oxide" OR "inorganic")'
        ],
        "system_prompt": """
        ROLE: Expert Flow Chemist.
        TASK: Filter a broad feed of microfluidics papers.
        
        CRITICAL RULES:
        - REJECT (Score 0): Biology (organs-on-chip), pure physics (droplet dynamics), or organic drug synthesis.
        - ACCEPT (Score 10): Flow synthesis/assembly SPECIFICALLY of Iron Oxide, SPIONs, or Magnetite.
        - ACCEPT (Score 8): Flow synthesis of inorganic nanoparticles (Gold, Silica) IF the method is transferable.
        """
    },

    # -----------------------------------------------------------
    # 2. Biomedical Applications (Already Optimized)
    # -----------------------------------------------------------
    {
        "id": "bio_app",
        "title": "🧲 Biomedical Nanomaterials",
        "api_filters": [
            'default.search:("iron oxide" OR "SPION" OR "nanoparticle") AND ("hyperthermia" OR "MRI" OR "cancer" OR "MPI")'
        ],
        "system_prompt": """
        ROLE: Biomedical Engineer.
        TASK: Track inorganic nanoparticles in medicine.
        SCORING RULES:
        - 10: Iron Oxide/SPIONs for Hyperthermia/MRI.
        - 0: Routine drug delivery.
        """
    },

    # -----------------------------------------------------------
    # 3. AI for Materials
    # -----------------------------------------------------------
    {
        "id": "ai_materials",
        "title": "🤖 AI in Material Science",
        "api_filters": [
            'default.search:("machine learning" OR "autonomous lab" OR "active learning") AND ("synthesis" OR "nanomaterials")'
        ],
        "system_prompt": """
        ROLE: Materials Informatics Researcher.
        TASK: Identify AI applied to material discovery.
        SCORING RULES:
        - 10: AI for NANOMATERIALS in BIOMEDICAL use.
        - 8: AI for inorganic synthesis optimization.
        - 0: Generic AI reviews.
        """
    }
]
