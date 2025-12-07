# Menggunakan base image Python 3.12 versi ringan
FROM python:3.12-slim

# Set working directory di dalam container
WORKDIR /app

# Mencegah Python membuat file cache .pyc & buffering output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 1. Install dependencies sistem untuk OCR (Tesseract & Poppler)
# tesseract-ocr-ind: agar bisa baca bahasa Indonesia dengan baik
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    poppler-utils \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-ind \
    && rm -rf /var/lib/apt/lists/*

# Salin file requirements
COPY requirements.txt .

# Install library Python
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh kode aplikasi ke dalam container
COPY . .

# Expose port default Streamlit
EXPOSE 8501

# Healthcheck agar platform deployment tahu aplikasi sudah siap
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Jalankan aplikasi dengan maxUploadSize 1GB
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.maxUploadSize=1000"]