# Project Prediksi Mortalitas dan Rawat Inap Pasien Pneumonia

Project ini menggunakan algoritma Machine Learning dengan pendekatan **Low Code PyCaret** untuk memprediksi:
1. **Mortalitas** (kematian) pasien pneumonia
2. **Length of Stay (LOS)** - lama rawat inap pasien pneumonia

## 📋 Deskripsi

Project ini dikembangkan berdasarkan metodologi yang dijelaskan dalam proposal tugas akhir dengan judul "Prediksi Mortalitas dan Rawat Inap Pasien Pneumonia Menggunakan Algoritma Machine Learning Melalui Low Code Pycaret".

### Dataset
- **Jumlah pasien**: 669 pasien pneumonia
- **Sumber**: 2 rumah sakit di Jepang (Rumah Sakit Universitas Kota Yokohama dan Rumah Sakit Kanto Rosai)
- **Komposisi**: 201 perempuan, 468 laki-laki

## 🛠️ Tools dan Library

- **PyCaret**: Low code machine learning framework
- **LightGBM**: Gradient Boosting algorithm
- **Extra Tree Regressor/Classifier**: Ensemble learning method
- **Pandas & NumPy**: Data processing
- **Matplotlib & Seaborn**: Visualization
- **Google Colaboratory**: Platform untuk development (opsional)

## 📁 Struktur Project

```
pneumonia-prediction/
├── data/                  # Folder untuk dataset
│   ├── pneumonia_dataset.xlsx
│   └── processed_pneumonia_data.csv
├── models/                # Folder untuk model yang sudah ditraining
│   ├── mortality_model/
│   ├── mortality_et_model/
│   ├── los_model/
│   └── los_et_model/
├── notebooks/             # Jupyter notebooks (opsional)
├── results/               # Folder untuk hasil prediksi
│   └── predictions.csv
├── src/                   # Source code
│   ├── data_preprocessing.py
│   ├── train_mortality.py
│   ├── train_los.py
│   └── predict.py
├── main.py                # Main script untuk menjalankan seluruh pipeline
├── requirements.txt       # Dependencies
└── README.md
```

## 🚀 Instalasi

⚠️ **PENTING**: Python 3.13 mungkin memiliki masalah kompatibilitas dengan beberapa library. **Rekomendasi: Gunakan Python 3.11 atau 3.12**.

Lihat file [INSTALL.md](INSTALL.md) untuk panduan instalasi lengkap.

### Quick Start:

1. **Clone atau download project ini**

2. **Buat virtual environment** (dengan Python 3.11 atau 3.12):
```bash
python3.11 -m venv venv  # atau python3.12
source venv/bin/activate  # macOS/Linux
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

**Alternatif**: Gunakan Google Colab untuk menghindari masalah instalasi. Lihat file `notebooks/colab_pneumonia_prediction.py`.

3. **Siapkan dataset**:
   - Letakkan file dataset Excel/CSV di folder `data/`
   - Pastikan dataset memiliki kolom:
     - Target untuk mortalitas (misal: `mortality`)
     - Target untuk LOS (misal: `LOS`)
     - Fitur-fitur seperti: Age, Sex, BMI, Heart_rate, dll.

## 📖 Cara Penggunaan

### 1. Menjalankan Seluruh Pipeline

Jalankan script utama untuk melakukan preprocessing, training, dan prediksi:

```bash
python main.py
```

### 2. Preprocessing Data

Jika ingin melakukan preprocessing saja:

```python
from src.data_preprocessing import DataPreprocessor

preprocessor = DataPreprocessor("data/pneumonia_dataset.xlsx")
df = preprocessor.load_data()
preprocessor.explore_data()
preprocessor.handle_missing_values(strategy='mean')
preprocessor.encode_categorical()
preprocessor.save_processed_data("data/processed_data.csv")
```

### 3. Training Model Mortalitas

```python
from src.train_mortality import train_mortality_model

model, predictions = train_mortality_model(
    data_path="data/processed_data.csv",
    target_col='mortality',
    test_size=0.2
)
```

### 4. Training Model LOS

```python
from src.train_los import train_los_model

model, predictions = train_los_model(
    data_path="data/processed_data.csv",
    target_col='LOS',
    test_size=0.2
)
```

### 5. Prediksi Data Baru

```python
from src.predict import predict_both
import pandas as pd

# Siapkan data baru
new_data = pd.DataFrame({
    'Age': [79],
    'Sex': [1],
    'BMI': [18.5],
    # ... fitur lainnya
})

# Prediksi
results = predict_both(new_data)
print(results)
```

## 🔧 Konfigurasi

### Mengubah Nama Kolom Target

Jika dataset Anda menggunakan nama kolom yang berbeda, edit di file `main.py`:

```python
# Untuk mortalitas
target_col='mortality'  # Ganti dengan nama kolom di dataset Anda

# Untuk LOS
target_col='LOS'  # Ganti dengan nama kolom di dataset Anda
```

### Mengubah Parameter Training

Edit parameter di fungsi `setup()` pada file `train_mortality.py` atau `train_los.py`:

```python
clf = setup(
    data=df,
    target=target_col,
    train_size=0.8,  # 80% training, 20% test
    session_id=123,
    normalize=True,
    feature_selection=True,
    # ... parameter lainnya
)
```

## 📊 Metode yang Digunakan

### 1. Light Gradient Boosting Machine (LightGBM)
- Algoritma gradient boosting yang efisien
- Cocok untuk data besar dan fitur berdimensi tinggi
- Digunakan untuk prediksi mortalitas (klasifikasi) dan LOS (regresi)

### 2. Extra Tree Regressor/Classifier
- Ensemble method berbasis decision tree
- Menggunakan random split points
- Memberikan variasi yang lebih besar dibanding Random Forest

## 📈 Evaluasi Model

Model akan dievaluasi menggunakan metrik:

**Untuk Klasifikasi (Mortalitas)**:
- Accuracy
- Precision
- Recall
- F1-Score
- AUC-ROC

**Untuk Regresi (LOS)**:
- RMSE (Root Mean Squared Error)
- MAE (Mean Absolute Error)
- R² Score
- MAPE (Mean Absolute Percentage Error)

## 📝 Catatan Penting

1. **Dataset**: Pastikan dataset Anda memiliki format yang sesuai. Sesuaikan nama kolom di kode jika berbeda.

2. **Missing Values**: Script akan menangani missing values secara otomatis, tetapi disarankan untuk memeriksa data terlebih dahulu.

3. **Categorical Encoding**: Variabel kategorikal akan di-encode otomatis (binary → label encoding, multi-class → one-hot encoding).

4. **Model Saving**: Model yang sudah ditraining akan disimpan di folder `models/` dan bisa digunakan kembali untuk prediksi.

## 🔍 Troubleshooting

### Error: "Kolom tidak ditemukan"
- Pastikan nama kolom target sesuai dengan yang ada di dataset
- Periksa case sensitivity (huruf besar/kecil)

### Error: "Model tidak bisa dimuat"
- Pastikan model sudah ditraining terlebih dahulu
- Periksa path ke model file

### Error: "Memory error"
- Kurangi ukuran dataset atau gunakan sampling
- Kurangi parameter `n_iter` saat tuning

## 📚 Referensi

- PyCaret Documentation: https://pycaret.org/
- LightGBM Documentation: https://lightgbm.readthedocs.io/
- Chen, H., et al. (2025). "Employing a Low Code Machine Learning Approach To Predict In Hospital Mortality And Length Of Stay In Patients With Community Acquired Pneumonia"

## 👤 Author

Dikembangkan berdasarkan proposal tugas akhir:
- **Judul**: Prediksi Mortalitas dan Rawat Inap Pasien Pneumonia Menggunakan Algoritma Machine Learning Melalui Low Code Pycaret
- **Penulis**: Luthfi Ramadhan
- **Program Studi**: Teknik Informatika, Universitas Esa Unggul

## 📄 License

Project ini dibuat untuk keperluan akademik dan penelitian.

---

**Selamat menggunakan!** 🎉

Jika ada pertanyaan atau masalah, silakan buat issue atau hubungi developer.

