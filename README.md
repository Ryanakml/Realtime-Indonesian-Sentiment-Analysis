# Realtime Indonesian Sentiment Analysis

## Project Structure

```bash
indo-sentiment-mlops/
├──.github/
│   └── workflows/
│       └── ci-cd.yml         # Alur kerja CI/CD
├── api/
│   ├── Dockerfile            # Dockerfile untuk layanan API
│   ├── main.py               # Kode aplikasi FastAPI
│   └── requirements.txt      # Dependensi API
├── dags/
│   └── retraining_dag.py     # Definisi DAG Airflow
├── data/
│   ├── raw/                  # Data mentah (misalnya, corpus.parquet)
│   └── processed/            # Data yang telah diproses
├── dashboard/
│   ├── app.py                # Kode aplikasi Streamlit
│   └── requirements.txt
├── models/                   # Output model (checkpoints, onnx, dll.)
├── notebooks/                # Notebook Jupyter untuk eksplorasi
├── src/
│   ├── data/
│   │   ├── make_dataset.py
│   │   └── stream_simulator.py
│   ├── features/
│   │   ├── build_features.py
│   │   └── preprocessing.py
│   ├── models/
│   │   ├── train_baseline.py
│   │   ├── train_transformer.py
│   │   └── evaluate_model.py
│   └── monitoring/
│       └── check_drift.py
├── tests/                    # Tes unit dengan pytest
├──.env.template             # Template untuk variabel lingkungan
├── docker-compose.yml        # Orkestrasi lokal
├── README.md                 # Dokumentasi proyek (Bilingual)
└── pyproject.toml            # Manajemen dependensi dengan Poetry
```

## Project Overview

Project ini dirancang untuk dapat menganalisis sentiment secara real-time pada teks Bahasa Indonesia, dari komentar media sosial sampai review product ecommerce. Tujuannya adalah memberikan intelegensi bisnis ke stakeholder untuk bisa ditindaklanjuti untuk melakukan manajemen reputasi merek/ produk / persona.

API Analisis Sentimen Real-time Bahasa Indonesia
Repositori ini berisi proyek MLOps tingkat produksi untuk analisis sentimen real-time dari teks Bahasa Indonesia yang berasal dari media sosial dan ulasan produk.

## Architecture

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*DH5SfXFBXLN4aYEr4Ew-4Q.png)
![](https://excalidraw.com/#json=yu8-Wxsfwg7YvqE3iM0P3,dLkBnkwtk4gXeR79fBgkCw)

## Feature

- **API Performa Tinggi**: Dibangun dengan FastAPI.

- **Model Canggih**: Fine-tuning IndoBERT untuk akurasi tinggi.

- **MLOps End-to-End**: Pipeline CI/CD, deployment, monitoring, dan retraining otomatis.

- **Dashboard Interaktif**: Aplikasi Streamlit untuk demo langsung dan visualisasi.

## QuickStart (Demo)

1. Clone repositori:

```Bash
git clone https://github.com/your-username/sentiment-analysis-indonesia.git
cd sentiment-analysis-indonesia
```

2. Build dan jalankan dengan Docker Compose (Direkomendasikan):

```Bash
# Perintah ini akan menjalankan API, database, dan dashboard
docker-compose up --build
```

3. Akses layanan:

Dokumentasi API: `http://localhost:8000/docs`

Dashboard: `http://localhost:8501`