# Panduan Instalasi

## ⚠️ Catatan Penting tentang Python 3.13

Python 3.13 adalah versi yang sangat baru dan beberapa library (seperti pandas, scikit-learn versi lama) mungkin belum sepenuhnya kompatibel. 

**Rekomendasi**: Gunakan **Python 3.11** atau **Python 3.12** untuk kompatibilitas terbaik.

## Cara Instalasi

### Opsi 1: Menggunakan Python 3.11 atau 3.12 (Direkomendasikan)

1. **Install Python 3.11 atau 3.12** (jika belum ada):
```bash
# Menggunakan Homebrew (macOS)
brew install python@3.11

# Atau download dari python.org
```

2. **Buat virtual environment dengan Python 3.11/3.12**:
```bash
cd pneumonia-prediction
python3.11 -m venv venv  # atau python3.12
source venv/bin/activate  # macOS/Linux
# atau
venv\Scripts\activate  # Windows
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

### Opsi 2: Menggunakan Python 3.13 (Dengan Versi Library Terbaru)

Jika Anda tetap ingin menggunakan Python 3.13, install versi library terbaru yang sudah support:

```bash
cd pneumonia-prediction
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip

# Install versi terbaru yang support Python 3.13
pip install pycaret pandas numpy scikit-learn matplotlib seaborn plotly openpyxl xlrd lightgbm xgboost catboost jupyter ipykernel tqdm
```

### Opsi 3: Menggunakan Google Colab (Paling Mudah)

Google Colab sudah memiliki semua dependencies yang diperlukan. Cukup:

1. Upload file `notebooks/colab_pneumonia_prediction.py` ke Google Colab
2. Upload dataset Anda
3. Jalankan script

## Verifikasi Instalasi

Setelah instalasi, verifikasi dengan:

```bash
python -c "import pycaret; import pandas; import numpy; print('✓ Semua library berhasil diinstall!')"
```

## Troubleshooting

### Error: "externally-managed-environment"
- Gunakan virtual environment (sudah dijelaskan di atas)

### Error: "Cannot install package"
- Pastikan menggunakan Python 3.11 atau 3.12
- Atau upgrade pip: `pip install --upgrade pip`

### Error: "Module not found"
- Pastikan virtual environment sudah diaktifkan
- Install ulang: `pip install -r requirements.txt`

## Alternatif: Menggunakan Conda

Jika Anda menggunakan Anaconda/Miniconda:

```bash
conda create -n pneumonia python=3.11
conda activate pneumonia
pip install -r requirements.txt
```

