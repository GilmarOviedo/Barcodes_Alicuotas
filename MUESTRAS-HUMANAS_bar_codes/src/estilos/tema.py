def obtener_estilos_css():
    """Estilos CSS profesionales - Paleta OuraByte."""
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;600;700&display=swap');
    
    /* ========== VARIABLES OURABYTE ========== */
    :root {
        --primary: #C8E100;
        --primary-dark: #a6d700;
        --bg-main: #001f1c;
        --bg-card: rgba(1, 25, 20, 0.6);
        --bg-hover: rgba(114, 140, 49, 0.2);
        --green-yellow: #728C31;
        
        --text-primary: #f0f0f0;
        --text-secondary: rgba(240, 240, 240, 0.7);
        --text-muted: rgba(240, 240, 240, 0.5);
        
        --border: rgba(200, 225, 0, 0.2);
        --glow: 0 0 20px rgba(200, 225, 0, 0.3);
    }
    
    /* ========== BASE ========== */
    * {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .main {
        background: linear-gradient(135deg, var(--bg-main) 0%, #002925 100%);
        font-family: 'Roboto', -apple-system, BlinkMacSystemFont, sans-serif;
        padding: 2rem 1rem;
    }
    
    /* ========== HEADER ========== */
    .header-container {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
        border-bottom: 2px solid var(--border);
    }
    
    .header-container h1 {
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--primary);
        margin: 0;
        text-shadow: var(--glow);
    }
    
    .header-container .subtitle {
        color: var(--text-secondary);
        font-size: 0.95rem;
        margin-top: 0.5rem;
        font-weight: 300;
    }
    
    /* ========== SECCIONES ========== */
    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--primary);
        margin: 1.5rem 0 1rem 0;
        padding-left: 0.75rem;
        border-left: 3px solid var(--primary);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* ========== INFO PILL (COMPACTO) ========== */
    .info-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: var(--bg-hover);
        backdrop-filter: blur(8px);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 8px 16px;
        margin: 0.5rem 0;
    }
    
    .pill-icon {
        font-size: 1rem;
    }
    
    .pill-text {
        color: var(--text-secondary);
        font-size: 0.875rem;
        font-weight: 500;
    }
    
    /* ========== RESULT CARD (COMPACTO Y ESTÉTICO) ========== */
    .result-card {
        background: var(--bg-card);
        backdrop-filter: blur(10px);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    .result-header h3 {
        color: var(--primary);
        font-size: 1.2rem;
        font-weight: 600;
        margin: 0 0 1rem 0;
        text-align: center;
        text-shadow: var(--glow);
    }
    
    .result-stats {
        display: flex;
        gap: 10px;
        justify-content: center;
    }
    
    .stat-item {
        background: var(--bg-hover);
        backdrop-filter: blur(8px);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 14px 20px;
        text-align: center;
        min-width: 110px;
    }
    
    .stat-value {
        display: block;
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary);
        margin-bottom: 4px;
        text-shadow: var(--glow);
    }
    
    .stat-label {
        display: block;
        font-size: 0.7rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 400;
    }
    
    /* ========== INPUTS ========== */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        background: var(--bg-hover) !important;
        backdrop-filter: blur(8px);
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.95rem !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(200, 225, 0, 0.15) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: var(--text-muted) !important;
    }
    
    /* ========== BOTONES ========== */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
        color: var(--bg-main) !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        box-shadow: var(--glow);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 30px rgba(200, 225, 0, 0.5);
    }
    
    /* ========== RADIO BUTTONS ========== */
    .stRadio > div {
        background: var(--bg-card);
        backdrop-filter: blur(10px);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 1rem;
    }
    
    .stRadio [role="radiogroup"] label {
        background: var(--bg-hover);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        color: var(--text-secondary);
    }
    
    .stRadio [role="radiogroup"] label:hover {
        background: rgba(114, 140, 49, 0.3);
        border-color: var(--primary);
        color: var(--text-primary);
    }
    
    /* ========== EXPANDER ========== */
    .streamlit-expanderHeader {
        background: var(--bg-card) !important;
        backdrop-filter: blur(8px);
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
        padding: 0.8rem !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: var(--bg-hover) !important;
        border-color: var(--primary) !important;
    }
    
    .streamlit-expanderContent {
        background: var(--bg-card);
        backdrop-filter: blur(8px);
        border: 1px solid var(--border);
        border-top: none;
        border-radius: 0 0 8px 8px;
        padding: 1rem;
    }
    
    /* ========== DATAFRAME ========== */
    .dataframe {
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        overflow: hidden;
    }
    
    .dataframe thead tr th {
        background: var(--bg-hover) !important;
        backdrop-filter: blur(8px);
        color: var(--primary) !important;
        font-weight: 600 !important;
        border-bottom: 2px solid var(--border) !important;
    }
    
    .dataframe tbody tr {
        background: var(--bg-card) !important;
        backdrop-filter: blur(8px);
    }
    
    .dataframe tbody tr:hover {
        background: var(--bg-hover) !important;
    }
    
    .dataframe tbody tr td {
        color: var(--text-secondary) !important;
    }
    
    /* ========== ALERTAS ========== */
    .stSuccess {
        background: rgba(200, 225, 0, 0.15) !important;
        backdrop-filter: blur(8px);
        border-left: 4px solid var(--primary) !important;
        border-radius: 8px !important;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.15) !important;
        backdrop-filter: blur(8px);
        border-left: 4px solid #EF4444 !important;
        border-radius: 8px !important;
    }
    
    .stWarning {
        background: rgba(245, 158, 11, 0.15) !important;
        backdrop-filter: blur(8px);
        border-left: 4px solid #F59E0B !important;
        border-radius: 8px !important;
    }
    
    /* ========== SPINNER ========== */
    .stSpinner > div {
        border-top-color: var(--primary) !important;
    }
    
    /* ========== IMÁGENES ========== */
    img {
        border-radius: 8px;
        border: 1px solid var(--border);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    /* ========== SCROLLBAR ========== */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-main);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary);
        border-radius: 5px;
        box-shadow: var(--glow);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary-dark);
    }
    
    /* ========== OCULTAR ELEMENTOS ========== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* ========== ANIMACIÓN GLOW ========== */
    @keyframes glow {
        0%, 100% {
            box-shadow: 0 0 10px rgba(200, 225, 0, 0.3);
        }
        50% {
            box-shadow: 0 0 25px rgba(200, 225, 0, 0.6);
        }
    }
    </style>
    """
