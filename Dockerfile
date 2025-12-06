# Menggunakan base image Python 3.12 versi ringan
FROM python:3.12-slim

# Set working directory di dalam container
WORKDIR /app

# Mencegah Python membuat file cache .pyc & buffering output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependensi sistem dasar
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Salin file requirements
COPY requirements.txt .

# Install library Python
RUN pip install --no-cache-dir -r requirements.txt

# Download data NLTK (WordNet & Punkt) saat build
# Ini penting agar tidak download setiap kali aplikasi start
RUN python -m nltk.downloader wordnet punkt

# Salin seluruh kode aplikasi ke dalam container
COPY . .

# Expose port default Streamlit
EXPOSE 8501

# Healthcheck untuk memastikan container berjalan
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Perintah untuk menjalankan aplikasi
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]