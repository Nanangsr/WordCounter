def get_main_css():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background-color: #0E4E68; /* Dark Teal */
        font-family: 'DM Sans', sans-serif;
    }
    
    /* Hide Streamlit Elements */
    header, footer, #MainMenu {visibility: hidden;}
    
    /* Text Colors */
    h1, h2, h3, h4, p, span, label, div {
        color: white;
    }
    
    /* Titles */
    .app-title {
        font-size: 3rem;
        font-weight: 700;
        color: #89CFF0 !important; /* Light Blue */
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .app-subtitle {
        text-align: center;
        opacity: 0.8;
        font-size: 1.1rem;
        margin-bottom: 3rem;
    }
    
    /* Primary Buttons */
    .stButton > button {
        background-color: #89CFF0;
        color: #0E4E68 !important;
        border-radius: 50px;
        font-weight: 700;
        border: none;
        padding: 0.6rem 2rem;
        width: 100%;
        transition: transform 0.2s;
    }
    
    .stButton > button:hover {
        transform: scale(1.02);
        background-color: white;
    }

    /* Recommendation Chips (Small Buttons) */
    div[data-testid="column"] .stButton > button {
        background-color: rgba(137, 207, 240, 0.15);
        border: 1px solid #89CFF0;
        color: #89CFF0 !important;
        font-size: 0.9rem;
    }
    div[data-testid="column"] .stButton > button:hover {
        background-color: #89CFF0;
        color: #0E4E68 !important;
    }

    /* Result Card (White Box) */
    .result-card {
        background-color: white;
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin: 2rem 0;
        animation: popUp 0.5s ease-out;
    }
    
    .result-label {
        color: #0E4E68 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
        font-size: 1rem;
    }
    
    .result-value {
        color: #0E4E68 !important;
        font-size: 6rem;
        font-weight: 700;
        line-height: 1.2;
    }
    
    /* Multi Result Item */
    .multi-result-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #eee;
        padding: 10px 0;
        text-align: left;
    }
    
    .multi-word {
        color: #0E4E68 !important;
        font-weight: 600;
        font-size: 1.2rem;
    }
    
    .multi-count {
        color: #0E4E68 !important;
        font-weight: 700;
        font-size: 1.5rem;
        background-color: #89CFF0;
        padding: 5px 15px;
        border-radius: 20px;
    }

    .synonym-box {
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid #eee;
    }
    
    .synonym-text {
        color: #666 !important;
        font-size: 0.9rem;
        font-style: italic;
    }
    
    /* Download Section Styling */
    .download-header {
        text-align: center;
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-size: 1rem;
        opacity: 0.8;
        border-top: 1px solid rgba(255,255,255,0.1);
        padding-top: 1rem;
    }

    @keyframes popUp {
        from { transform: scale(0.9); opacity: 0; }
        to { transform: scale(1); opacity: 1; }
    }
    
    /* File Uploader Customization */
    .stFileUploader {
        background-color: rgba(255,255,255,0.1);
        padding: 2rem;
        border-radius: 15px;
        border: 2px dashed #89CFF0;
    }
    
    /* Text Input Customization */
    .stTextInput input {
        background-color: rgba(0,0,0,0.2);
        color: white;
        border: none;
        border-radius: 10px;
        text-align: center;
        font-size: 1.2rem;
    }
    </style>
    """

def render_result_card(count, word, synonyms):
    syn_html = ""
    if synonyms:
        syn_list = ", ".join(synonyms)
        syn_html = f"""<div class="synonym-box">
<p class="result-label" style="font-size: 0.8rem; margin-bottom: 5px;">Synonym Suggestions</p>
<p class="synonym-text">{syn_list}</p>
</div>"""
    
    return f"""<div class="result-card">
<div class="result-label">Matches for "{word}"</div>
<div class="result-value">{count}</div>
{syn_html}
</div>"""

def render_multi_result_card(results_dict):
    """Menampilkan hasil untuk banyak kata"""
    items_html = ""
    for word, count in results_dict.items():
        items_html += f"""<div class="multi-result-item">
<span class="multi-word">{word}</span>
<span class="multi-count">{count}</span>
</div>"""
        
    return f"""<div class="result-card">
<div class="result-label" style="margin-bottom: 20px;">Multi-Word Analysis</div>
{items_html}
</div>"""