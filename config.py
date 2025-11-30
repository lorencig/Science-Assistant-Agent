# config.py

# --- 1. GLOBAL SETTINGS ---
DAYS_LOOKBACK = 2
MIN_RELEVANCE_SCORE = 7

# --- 2. OPENALEX CONCEPT IDS ---
CONCEPTS = {
    "Microfluidics": "C190062978",
    "Nanoparticles": "C104779481",
    "Inorganic_Chem": "C188027245",
    "Machine_Learning": "C154945302",
    "Materials_Science": "C192562407",
    "Iron_Oxide": "C2779702343", 
    "Biomedical_Eng": "C127313418",
    "Lipids": "C177713603",
    "Polymers": "C104186524",
    "Artificial_Intelligence": "C154945302"
}

# --- 3. THE SESSIONS ---
SESSIONS = [
    {
        "id": "fluidic_inorganic",
        "title": "⚗️ Inorganic Fluidic Synthesis",
        "api_filters": [
            f"concepts.id:{CONCEPTS['Microfluidics']}",
            f"concepts.id:{CONCEPTS['Nanoparticles']}",
            f"concepts.id:!{CONCEPTS['Lipids']}",
            f"concepts.id:!{CONCEPTS['Polymers']}"
        ],
        "system_prompt": """
        ROLE: Expert Material Scientist.
        TASK: Filter for INORGANIC nanoparticle synthesis in microfluidics.
        RULES:
        - REJECT (Score 1): Lipid Nanoparticles (LNPs), Liposomes, Polymer encapsulation.
        - REJECT (Score 2): Biological "drug delivery" without synthesis focus.
        - ACCEPT (Score 8+): Novel flow reactors, Gold/Silver/Silica/Quantum Dots synthesis.
        """
    },
    {
        "id": "mat_informatics",
        "title": "🤖 Materials Informatics",
        "api_filters": [
            f"concepts.id:{CONCEPTS['Materials_Science']}",
            f"concepts.id:{CONCEPTS['Artificial_Intelligence']}"
        ],
        "system_prompt": """
        ROLE: Research Scientist in AI for Materials.
        TASK: Identify papers using ML/AI to discover or optimize materials.
        RULES:
        - ACCEPT (Score 8+): Generative models (GANs/Diffusions) for crystals, Bayesian optimization, GNNs.
        - REJECT (Score 3): Routine use of commercial software without algorithmic novelty.
        """
    },
    {
        "id": "bio_iron",
        "title": "🧲 Bio-Medical Iron Oxide",
        "api_filters": [
            f"concepts.id:{CONCEPTS['Iron_Oxide']}",
            f"concepts.id:{CONCEPTS['Biomedical_Eng']}"
        ],
        "system_prompt": """
        ROLE: Biomedical Engineer.
        TASK: Track Iron Oxide Nanoparticles (SPIONs) applications.
        RULES:
        - ACCEPT: Magnetic Hyperthermia, MRI Contrast, Magnetic actuation.
        - REJECT: Water treatment or environmental remediation.
        """
    }
]