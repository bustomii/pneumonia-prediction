# Perbandingan Alur Flowchart dengan Implementasi Program

## ✅ Checklist Kesesuaian dengan Flowchart

### 1. Mulai Penelitian
- ✅ **Pneumonia** - Dataset: `data/data-669-patients.xlsx` (669 pasien)
- ✅ **Machine Learning** - Menggunakan algoritma ML (LightGBM, Extra Tree)
- ✅ **Low Code & PyCaret** - Menggunakan PyCaret untuk low-code ML

**Implementasi:** `main.py` baris 22-25

---

### 2. Identifikasi Masalah
- ✅ **Implisit dalam project** - Prediksi mortalitas dan LOS pasien pneumonia

**Implementasi:** Tercantum di dokumentasi dan komentar kode

---

### 3. Pengumpulan Data
- ✅ **669 pasien** - Dataset: `data/data-669-patients.xlsx`
- ✅ **2 RS Jepang** - Informasi tercantum di dataset

**Implementasi:** `main.py` baris 28, `data_preprocessing.py` baris 26-40

---

### 4. Eksplorasi Data (EDA)
- ✅ **Statistik** - `df.describe()` menampilkan statistik deskriptif
- ✅ **Missing Value** - `df.isnull().sum()` menampilkan missing values
- ✅ **Distribusi Variabel** - Menampilkan distribusi variabel kategorikal dan numerik

**Implementasi:** `data_preprocessing.py` baris 42-79, fungsi `explore_data()`

**Output:**
- Shape data
- Info data types
- Statistik deskriptif
- Missing values
- Duplikat
- Distribusi variabel kategorikal
- Distribusi variabel numerik (target)

---

### 5. Data Preprocessing
- ✅ **Cleaning** - Drop `Patient_ID` (identifier, bukan feature)
- ✅ **Encoding** - Label encoding untuk binary, one-hot encoding untuk multi-class
- ✅ **Normalisasi** - Dilakukan oleh PyCaret (`normalize=True`)
- ✅ **Handling NA** - `handle_missing_values()` dengan strategy mean/median/mode

**Implementasi:** `data_preprocessing.py`
- `encode_categorical()` - baris 94-118
- `handle_missing_values()` - baris 61-92
- Normalisasi dilakukan oleh PyCaret di `train_mortality.py` dan `train_los.py`

---

### 6. Pembagian Data Train-Test Split
- ✅ **Train-Test Split** - 80% train, 20% test (`test_size=0.2`)

**Implementasi:** 
- `train_mortality.py` baris 48: `train_size=1-test_size`
- `train_los.py` baris 48: `train_size=1-test_size`

---

### 7. Model Building (PyCaret)
- ✅ **Model Building** - Menggunakan PyCaret untuk low-code ML
- ✅ **Compare Models** - Membandingkan berbagai algoritma
- ✅ **Model Selection** - LightGBM dan Extra Tree (sesuai dokumen)
- ✅ **Hyperparameter Tuning** - `tune_model()` dengan n_iter=50
- ✅ **Model Finalization** - `finalize_model()` untuk model final

**Implementasi:**
- `train_mortality.py` - Model klasifikasi (LightGBM, Extra Tree)
- `train_los.py` - Model regresi (LightGBM, Extra Tree Regressor)

**Algoritma yang digunakan:**
- LightGBM (sesuai dokumen)
- Extra Tree Classifier/Regressor (sesuai dokumen)
- Compare dengan: XGBoost, Random Forest, Gradient Boosting, AdaBoost, Decision Tree

---

### 8. Evaluasi Model
- ✅ **Accuracy** - Untuk klasifikasi (mortalitas)
- ✅ **AUC** - Untuk klasifikasi (mortalitas)
- ✅ **RMSE** - Untuk regresi (LOS)

**Implementasi:**
- `train_mortality.py` baris 107: `evaluate_model(tuned_model)` - Menampilkan Accuracy, AUC, dll
- `train_los.py` baris 107: `evaluate_model(tuned_model)` - Menampilkan RMSE, MAE, R², dll

**Metrik yang ditampilkan oleh PyCaret:**
- **Klasifikasi:** Accuracy, AUC, Recall, Precision, F1, Kappa
- **Regresi:** MAE, MSE, RMSE, R², RMSLE, MAPE

---

### 9. Analisis & Pembahasan
- ⚠️ **Dokumentasi saja** - Tidak diimplementasikan dalam kode (sesuai instruksi)

---

### 10. Kesimpulan & Saran
- ⚠️ **Dokumentasi saja** - Tidak diimplementasikan dalam kode (sesuai instruksi)

---

### 11. Selesai
- ✅ **Selesai** - Program menampilkan pesan selesai dan lokasi file output

**Implementasi:** `main.py` baris 154-159

---

## Ringkasan Implementasi

### File Utama:
1. **`main.py`** - Pipeline utama yang menggabungkan semua langkah
2. **`src/data_preprocessing.py`** - EDA dan preprocessing
3. **`src/train_mortality.py`** - Training model mortalitas
4. **`src/train_los.py`** - Training model LOS
5. **`src/predict.py`** - Prediksi untuk data baru

### Alur Eksekusi:
```
1. Load Data (data-669-patients.xlsx)
   ↓
2. EDA (Statistik, Missing Value, Distribusi)
   ↓
3. Preprocessing (Cleaning, Encoding, Handling NA)
   ↓
4. Train-Test Split (80-20)
   ↓
5. Model Building dengan PyCaret
   ↓
6. Model Evaluation (Accuracy, AUC, RMSE)
   ↓
7. Model Saving
   ↓
8. Prediksi (contoh)
```

## ✅ Kesimpulan

**Program sudah sesuai dengan alur flowchart!**

Semua langkah dari flowchart sudah diimplementasikan:
- ✅ Pengumpulan data (669 pasien)
- ✅ EDA lengkap (statistik, missing value, distribusi)
- ✅ Preprocessing lengkap (cleaning, encoding, normalisasi, handling NA)
- ✅ Train-test split
- ✅ Model building dengan PyCaret
- ✅ Evaluasi model dengan metrik yang sesuai (Accuracy, AUC, RMSE)
- ✅ Prediksi untuk data baru

Program mengikuti metodologi penelitian yang ditunjukkan dalam flowchart.

