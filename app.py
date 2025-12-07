import streamlit as st
import pandas as pd
import styles
import logic
from typing import Dict, Any, List

# Konfigurasi Awal
def configure_page() -> None:
    st.set_page_config(
        page_title="Annual Report Analyzer",
        page_icon="📊",
        layout="wide"
    )
    st.markdown(styles.get_main_css(), unsafe_allow_html=True)
    st.markdown(styles.get_download_btn_css(), unsafe_allow_html=True)

# Manajemen Session State
def init_session_state() -> None:
    if 'step' not in st.session_state: st.session_state.step = 1
    if 'zip_name' not in st.session_state: st.session_state.zip_name = ""
    if 'analysis_results' not in st.session_state: st.session_state.analysis_results = []

def reset_app() -> None:
    st.session_state.step = 1
    st.session_state.zip_name = ""
    st.session_state.analysis_results = []
    st.rerun()

# Fungsi Render Halaman
def render_landing_page() -> None:
    st.write("")
    st.write("")
    st.markdown("<div style='font-size: 5rem; text-align: center;'>📊</div>", unsafe_allow_html=True)
    st.markdown('<h1 class="app-title">Annual Report Analyzer</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="app-subtitle">Batch Analysis for Annual Reports.<br>'
        'Detects Fintech, AI, Blockchain keywords automatically.</p>', 
        unsafe_allow_html=True
    )
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✨ Start Analysis", use_container_width=True):
            st.session_state.step = 2
            st.rerun()

def render_upload_page() -> None:
    st.markdown("## Upload Reports (ZIP)")
    st.markdown("<p style='text-align:center; opacity:0.7'>Upload a .zip file containing PDF/DOCX annual reports.</p>", unsafe_allow_html=True)
    
    uploaded_zip = st.file_uploader(
        label="Upload Annual Reports (ZIP format)", 
        type=['zip'], 
        label_visibility="collapsed"
    )
    
    c_opt1, c_opt2 = st.columns(2)
    with c_opt1:
        is_bilingual = st.checkbox("Enable Bilingual Search (Indonesia + English)", value=False)
    with c_opt2:
        include_scanned = st.checkbox(
            "Sertakan Dokumen Scan (OCR)", 
            value=False, 
            help="Jika dicentang, file PDF scan (gambar) akan diproses OCR (Maks 50 halaman pertama) dengan peningkatan kualitas gambar (DPI 300 + Sharpening)."
        )
    
    if uploaded_zip:
        st.session_state.zip_name = uploaded_zip.name
        st.write("")
        col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
        
        with col_c2:
            if st.button("🚀 Process Files", use_container_width=True):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                def update_progress(current, total, filename):
                    percent = int((current / total) * 100)
                    progress_bar.progress(percent)
                    clean_name = filename.split('/')[-1]
                    status_text.text(f"Processing ({current}/{total}): {clean_name}")

                try:
                    results = logic.process_zip_file(
                        uploaded_zip, 
                        is_bilingual, 
                        include_scanned,
                        progress_callback=update_progress
                    )
                    
                    st.session_state.analysis_results = results
                    st.session_state.step = 3
                    st.rerun()
                except Exception as e:
                    st.error(f"Terjadi kesalahan fatal: {str(e)}")

    st.write("")
    if st.button("Cancel"):
        reset_app()

def render_results_page() -> None:
    st.markdown("## Analysis Complete")
    results = st.session_state.analysis_results
    
    if not results:
        st.warning("Tidak ada file valid yang ditemukan atau diproses.")
        if st.button("📂 Start Over"): reset_app()
        return

    df = pd.DataFrame(results)
    keyword_cols = list(logic.BASE_PATTERNS.keys())
    
    df_success = df[df["Status"] != "SKIPPED (Scan)"]
    
    total_files = len(results)
    total_processed = len(df_success)
    
    if not df_success.empty:
        total_keyword_hits = df_success[keyword_cols].sum().sort_values(ascending=False)
        top_keyword = total_keyword_hits.index[0] if not total_keyword_hits.empty else "None"
        top_keyword_count = total_keyword_hits.iloc[0] if not total_keyword_hits.empty else 0
        total_words_scanned = df_success["Total Kata Dokumen"].sum()
    else:
        top_keyword = "N/A"
        top_keyword_count = 0
        total_words_scanned = 0

    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-card">
            <div class="metric-label">Files Processed</div>
            <div class="metric-value">{total_processed}/{total_files}</div>
            <div class="metric-sub">Reports analyzed (Scans skipped: {total_files - total_processed})</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Global Top Topic</div>
            <div class="metric-value" style="font-size: 2.5rem;">{top_keyword}</div>
            <div class="metric-sub">{top_keyword_count} occurrences</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Total Words</div>
            <div class="metric-value" style="font-size: 2.5rem;">{total_words_scanned:,}</div>
            <div class="metric-sub">Across valid files</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("### 📂 File Breakdown")
    cols = st.columns(3)
    
    for i, row in df.iterrows():
        with cols[i % 3]:
            if row['Status'] == 'SKIPPED (Scan)':
                st.markdown(f"""
                <div class="file-card" style="border: 1px dashed #ccc; opacity: 0.6;">
                    <div class="fc-header" title="{row['Nama Bank']}">{row['Nama Bank']}</div>
                    <div class="fc-sub">{row['Tahun']} • {row['Nama File'][:15]}...</div>
                    <div style="margin-top:20px; text-align:center; font-style:italic;">
                        ⚠️ Skipped (Scanned File)
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                row_keywords = row[keyword_cols]
                file_top_kw = row_keywords.idxmax() if not row_keywords.empty else "N/A"
                file_top_count = row_keywords.max() if not row_keywords.empty else 0
                
                card_html = styles.render_file_card(
                    bank=row['Nama Bank'],
                    year=row['Tahun'],
                    filename=row['Nama File'],
                    total_words=row['Total Kata Dokumen'],
                    top_keyword=file_top_kw,
                    top_count=file_top_count
                )
                st.markdown(card_html, unsafe_allow_html=True)

    st.write("")
    st.divider()

    st.markdown('<div class="download-header">📥 Export Data</div>', unsafe_allow_html=True)
    csv_data = logic.generate_csv_output(results)
    safe_zip_name = st.session_state.zip_name.replace('.zip', '') if st.session_state.zip_name else "Analysis"
    
    col_d1, col_d2, col_d3 = st.columns([1, 2, 1])
    with col_d2:
        st.download_button(
            label="📄 Download Full CSV Report",
            data=csv_data,
            file_name=f"{safe_zip_name}_Analysis.csv",
            mime="text/csv",
            use_container_width=True
        )

    st.write("")
    st.markdown("### 🔎 Detailed Data Preview")
    
    # PERBAIKAN: Menambahkan 'Tahun' dan 'Total Kata Dokumen' ke dalam list display
    display_cols = ["Nama Bank", "Tahun", "Status", "Nama File"] + keyword_cols + ["Total Kata Dokumen"]
    valid_cols = [c for c in display_cols if c in df.columns]
    
    st.dataframe(df[valid_cols], use_container_width=True)

    st.write("")
    if st.button("📂 Start Over"):
        reset_app()

def main() -> None:
    configure_page()
    init_session_state()
    if st.session_state.step == 1: render_landing_page()
    elif st.session_state.step == 2: render_upload_page()
    elif st.session_state.step == 3: render_results_page()

if __name__ == "__main__":

    main()
