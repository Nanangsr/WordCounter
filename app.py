import streamlit as st
import time
import logic
import styles

# Konfigurasi Awal
st.set_page_config(
    page_title="Word Count App",
    page_icon="📝",
    layout="centered"
)

st.markdown(styles.get_main_css(), unsafe_allow_html=True)

st.markdown("""
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
.stDownloadButton > button:active {
    background-color: #89CFF0;
    color: #0E4E68 !important;
}
</style>
""", unsafe_allow_html=True)

# Inisialisasi Session State
if 'step' not in st.session_state: st.session_state.step = 1
if 'file_data' not in st.session_state: st.session_state.file_data = None
if 'file_name' not in st.session_state: st.session_state.file_name = ""
if 'target_word' not in st.session_state: st.session_state.target_word = ""
if 'final_count' not in st.session_state: st.session_state.final_count = 0
if 'top_words' not in st.session_state: st.session_state.top_words = []
if 'synonyms' not in st.session_state: st.session_state.synonyms = []
if 'multi_results' not in st.session_state: st.session_state.multi_results = None

# Fungsi Navigasi
def reset_app():
    st.session_state.step = 1
    st.session_state.file_data = None
    st.session_state.top_words = []
    st.session_state.synonyms = []
    st.session_state.multi_results = None

def process_input(input_text):
    """
    Memproses input pengguna.
    Bisa menangani satu kata ATAU banyak kata yang dipisah koma.
    """
    st.session_state.target_word = input_text
    st.session_state.multi_results = None
    
    # Cek apakah input mengandung koma (indikasi multi-word)
    if ',' in input_text:
        # Split berdasarkan koma dan bersihkan spasi
        words_list = [w.strip() for w in input_text.split(',') if w.strip()]
        
        with st.spinner("Analyzing multiple words..."):
            time.sleep(0.8)
            results = logic.count_multiple_words(st.session_state.file_data, words_list)
            st.session_state.multi_results = results
            st.session_state.step = 4
            st.rerun()
            
    else:
        word = input_text.strip()
        with st.spinner("Analyzing..."):
            time.sleep(0.8)
            count = logic.count_word_occurrences(st.session_state.file_data, word)
            st.session_state.final_count = count
            st.session_state.synonyms = logic.get_synonyms(word)
            st.session_state.step = 4
            st.rerun()

# LANDING PAGE
if st.session_state.step == 1:
    st.write("")
    st.markdown("<div style='font-size: 5rem; text-align: center;'>📝</div>", unsafe_allow_html=True)
    st.markdown('<h1 class="app-title">Word Count</h1>', unsafe_allow_html=True)
    st.markdown('<p class="app-subtitle">Upload documents, count words, and get recommendations instantly.</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✨ Start New Analysis", use_container_width=True):
            st.session_state.step = 2
            st.rerun()

# UPLOAD DOCUMENT
elif st.session_state.step == 2:
    st.markdown("## Upload Document")
    st.markdown("<p style='text-align:center; opacity:0.7'>Support .docx, .pdf, .txt</p>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("", type=['docx', 'pdf', 'txt'], label_visibility="collapsed")
    
    if uploaded_file:
        ext = uploaded_file.name.split('.')[-1].lower()
        try:
            if ext == 'docx':
                text = logic.read_docx(uploaded_file)
            elif ext == 'pdf':
                text = logic.read_pdf(uploaded_file)
            elif ext == 'txt':
                text = logic.read_txt(uploaded_file)
            
            st.session_state.file_data = text
            st.session_state.file_name = uploaded_file.name
            st.session_state.top_words = logic.get_top_words(text, top_n=4)
            
            time.sleep(0.5)
            st.session_state.step = 3
            st.rerun()
        except Exception as e:
            st.error(f"Error: {str(e)}")

    st.write("")
    if st.button("Cancel"):
        reset_app()
        st.rerun()

# INPUT & PROCESS
elif st.session_state.step == 3:
    st.markdown("## Enter Target Word(s)")
    st.markdown(f"<p style='text-align:center; opacity:0.7'>Source: {st.session_state.file_name}</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size: 0.8rem; margin-top: -15px; color: #89CFF0;'>Tip: Separate with commas for multiple words (e.g., banking, mobile)</p>", unsafe_allow_html=True)
    
    # Input Manual
    manual_input = st.text_input("", placeholder="Type words here...", label_visibility="collapsed")
    
    st.write("")
    
    # Rekomendasi Top Words
    if st.session_state.top_words:
        st.markdown("<p style='text-align:center; font-size:0.9rem; margin-bottom:5px;'>Suggested words:</p>", unsafe_allow_html=True)
        cols = st.columns(len(st.session_state.top_words))
        for idx, word in enumerate(st.session_state.top_words):
            with cols[idx]:
                if st.button(word, key=f"sug_{idx}"):
                    process_input(word)
    
    st.write("")
    
    # Tombol Proses
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if manual_input:
            if st.button("🚀 Count Words", use_container_width=True):
                process_input(manual_input)

    st.divider()
    
    with st.expander("📄 View Extracted Content"):
        st.text_area("", st.session_state.file_data, height=200, disabled=True)

    if st.button("Back to Upload"):
        st.session_state.step = 2
        st.rerun()

# RESULT
elif st.session_state.step == 4:
    st.write("")
    
    # Tampilkan Kartu Hasil
    if st.session_state.multi_results:
        st.markdown(
            styles.render_multi_result_card(st.session_state.multi_results),
            unsafe_allow_html=True
        )
        # Siapkan data download untuk Multi
        dl_target = None 
        dl_result = st.session_state.multi_results
    else:
        st.markdown(
            styles.render_result_card(
                st.session_state.final_count, 
                st.session_state.target_word, 
                st.session_state.synonyms
            ), 
            unsafe_allow_html=True
        )
        # Siapkan data download untuk Single
        dl_target = st.session_state.target_word
        dl_result = st.session_state.final_count

    # DOWNLOAD SECTION
    st.markdown('<div class="download-header">📥 Download Results</div>', unsafe_allow_html=True)
    
    # 1. Siapkan Nama File: (NamaAsli)_WordCount
    original_name = st.session_state.file_name
    base_name = original_name.rsplit('.', 1)[0] if '.' in original_name else original_name
    filename_csv = f"{base_name}_WordCount.csv"
    filename_txt = f"{base_name}_WordCount.txt"
    
    # 2. Generate Konten File
    csv_data = logic.format_results_for_download(dl_target, dl_result, "csv")
    txt_data = logic.format_results_for_download(dl_target, dl_result, "txt")
    
    # 3. Tombol Download 
    d1, d2 = st.columns(2)
    with d1:
        st.download_button(
            label="📄 Download CSV",
            data=csv_data,
            file_name=filename_csv,
            mime="text/csv",
            use_container_width=True
        )
    with d2:
        st.download_button(
            label="📝 Download TXT",
            data=txt_data,
            file_name=filename_txt,
            mime="text/plain",
            use_container_width=True
        )

    st.write("")
    st.divider()
    
    # Navigasi Bawah
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Count Another Word"):
            st.session_state.step = 3
            st.rerun()
    with col2:
        if st.button("📂 Start Over"):
            reset_app()
            st.rerun()