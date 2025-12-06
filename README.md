Word Count App 📝

Aplikasi web berbasis Python Streamlit yang memungkinkan pengguna mengunggah dokumen, menghitung kemunculan kata tertentu, dan mendapatkan rekomendasi sinonim (menggunakan NLTK).

Fitur Utama

Multi-format: Mendukung .docx, .pdf, dan .txt.

Workflow Intuitif: Alur langkah-demi-langkah (Upload -> Input -> Hasil).

Analisis Cerdas: Memberikan saran kata populer dari dokumen dan rekomendasi sinonim untuk kata target.

Tampilan Modern: UI bersih dengan mode gelap (Dark Teal).

Struktur File

app.py: Kontroler utama aplikasi (UI & State Management).

logic.py: Logika backend (pembacaan file & NLTK).

styles.py: Konfigurasi CSS untuk tampilan frontend.

Dockerfile: Konfigurasi deployment container.

Cara Menjalankan (Lokal)

Pastikan Python 3.12 terinstall.

Install dependensi:

pip install -r requirements.txt


Jalankan aplikasi:

streamlit run app.py


Cara Menjalankan dengan Docker 🐳

Build Image:

docker build -t word-count-app .


Jalankan Container:

docker run -p 8501:8501 word-count-app


Akses Aplikasi:
Buka browser di http://localhost:8501.