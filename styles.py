def get_main_css() -> str:
    """
    Mengatur font, warna background, kartu metrik, dan kartu file.
    """
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap');
    
    .stApp {
        background-color: #0E4E68;
        font-family: 'DM Sans', sans-serif;
    }
    
    header, footer, #MainMenu {visibility: hidden;}
    h1, h2, h3, p, span, label, div { color: white; }
    
    /* JUDUL UTAMA */
    .app-title {
        font-size: 3rem;
        font-weight: 700;
        color: #89CFF0 !important;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .app-subtitle {
        text-align: center !important;
        width: 100%;
        display: block;
        opacity: 0.8;
        font-size: 1.1rem;
        margin-bottom: 3rem;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* TOMBOL STANDAR */
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

    /* KARTU RINGKASAN (STEP 3) */
    .metric-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-bottom: 30px;
        flex-wrap: wrap;
    }
    
    .metric-card {
        background-color: white;
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        width: 250px;
        min-height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .metric-value {
        color: #0E4E68 !important;
        font-size: 3.5rem;
        font-weight: 700;
        line-height: 1;
        margin: 10px 0;
    }
    
    .metric-label {
        color: #0E4E68 !important;
        font-size: 1rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-sub {
        color: #666 !important;
        font-size: 0.8rem;
    }
    
    /* KARTU FILE */
    .file-card {
        background-color: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 15px;
        transition: transform 0.2s;
        height: 100%;
    }
    
    .file-card:hover {
        background-color: rgba(255, 255, 255, 0.15);
        transform: translateY(-5px);
    }
    
    .fc-header {
        font-size: 1.1rem;
        font-weight: 700;
        color: #89CFF0 !important;
        margin-bottom: 5px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .fc-sub {
        font-size: 0.85rem;
        color: #ccc !important;
        margin-bottom: 10px;
    }
    
    .fc-stat {
        font-size: 0.9rem;
        font-weight: 600;
        margin-top: 5px;
        display: flex;
        justify-content: space-between;
    }

    /* UPLOAD AREA */
    .stFileUploader {
        background-color: rgba(255,255,255,0.1);
        padding: 2rem;
        border-radius: 15px;
        border: 2px dashed #89CFF0;
    }
    
    .download-header {
        text-align: center;
        margin-bottom: 1rem;
        font-size: 1.2rem;
        font-weight: bold;
        color: #89CFF0;
    }
    </style>
    """

def get_download_btn_css() -> str:
    """CSS khusus untuk tombol download agar seragam."""
    return """
    <style>
    .stDownloadButton > button {
        background-color: #89CFF0;
        color: #0E4E68 !important;
        border-radius: 50px;
        font-weight: 700;
        border: none;
        padding: 0.6rem 2rem;
        width: 100%;
        transition: transform 0.2s;
    }
    .stDownloadButton > button:hover {
        transform: scale(1.02);
        background-color: white;
        color: #0E4E68 !important;
        border: none;
    }
    </style>
    """

def render_file_card(bank: str, year: str, filename: str, total_words: int, top_keyword: str, top_count: int) -> str:
    """
    Membuat string HTML untuk menampilkan kartu ringkasan per file.
    
    Args:
        bank: Nama bank.
        year: Tahun laporan.
        filename: Nama file.
        total_words: Jumlah kata terdeteksi.
        top_keyword: Keyword terbanyak.
        top_count: Jumlah kemunculan keyword terbanyak.
        
    Returns:
        str: String HTML.
    """
    return f"""
    <div class="file-card">
        <div class="fc-header" title="{bank}">{bank}</div>
        <div class="fc-sub">{year} • {filename[:20]}...</div>
        <div style="border-top: 1px solid rgba(255,255,255,0.1); margin: 10px 0;"></div>
        <div class="fc-stat">
            <span>Total Words:</span>
            <span>{total_words:,}</span>
        </div>
        <div class="fc-stat" style="color: #FFD700 !important;">
            <span>Top Topic:</span>
            <span>{top_keyword} ({top_count})</span>
        </div>
    </div>

    """
