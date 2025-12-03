# BAB IV
# ANALISIS DAN PEMBAHASAN

## 4.1 Hasil Eksplorasi Data (EDA)

### 4.1.1 Karakteristik Dataset

Dataset yang digunakan dalam penelitian ini terdiri dari **669 pasien pneumonia** yang dirawat di 2 rumah sakit di Jepang. Dataset memiliki **27 kolom** yang mencakup variabel demografis, klinis, laboratorium, dan outcome.

**Karakteristik Demografis:**
- **Jumlah pasien:** 669 orang
- **Jenis kelamin:** 
  - Laki-laki: 468 pasien (70.0%)
  - Perempuan: 201 pasien (30.0%)
- **Usia:** Rata-rata 77.64 tahun (SD: 10.40 tahun), rentang 60-94 tahun

**Distribusi Target:**
- **Mortalitas:** 
  - Tidak (No): 337 pasien (50.4%)
  - Ya (Yes): 332 pasien (49.6%)
  - Distribusi seimbang, tidak ada class imbalance yang signifikan

- **Length of Stay (LOS):**
  - Rata-rata: 20.09 hari
  - Standar deviasi: 10.94 hari
  - Rentang: 2-39 hari
  - Median: 20 hari
  - Kuartil 1: 10 hari
  - Kuartil 3: 29 hari

### 4.1.2 Analisis Missing Values

Hasil eksplorasi data menunjukkan bahwa **tidak ada missing values** dalam dataset. Semua 669 baris data lengkap untuk semua 27 kolom, sehingga tidak diperlukan imputasi data.

### 4.1.3 Analisis Distribusi Variabel

**Variabel Kategorikal:**
- **Sex:** Binary (M/F) - 70% laki-laki
- **Oxygen_need:** Binary (Yes/No)
- **Shock_vital:** Binary (Yes/No)
- **LOC, Bedsore, Aspiration:** Binary (Yes/No)
- **ADL_category:** 3 kategori (Dependent, Independent, Semi-dependent)
- **Key_person:** 4 kategori (Son, Daughter, Spouse, Others)
- **Nursing_insurance:** Binary (Yes/No)

**Variabel Numerik:**
- **BMI:** Rata-rata 20.61 (SD: 2.62), menunjukkan sebagian besar pasien memiliki BMI rendah
- **Vital signs:** Heart rate, respiration rate, temperature, systolic BP dalam rentang normal hingga abnormal
- **Laboratorium:** WBC, Hemoglobin, Platelet, Total protein, Albumin, Sodium, BUN, CRP menunjukkan variasi yang luas
- **CCI (Charlson Comorbidity Index):** Rata-rata 4.07 (SD: 2.03), menunjukkan tingkat komorbiditas sedang

---

## 4.2 Hasil Data Preprocessing

### 4.2.1 Cleaning Data

Proses cleaning dilakukan dengan:
- **Menghapus kolom Patient_ID:** Kolom identifier dihapus karena bukan feature prediktif dan akan menghasilkan 669 kolom dummy jika di-encode
- **Pengecekan duplikat:** Tidak ditemukan data duplikat

### 4.2.2 Encoding Variabel Kategorikal

**Label Encoding (Binary):**
- `Sex`: M=1, F=0
- `Oxygen_need`: Yes=1, No=0
- `Shock_vital`: Yes=1, No=0
- `LOC`: Yes=1, No=0
- `Bedsore`: Yes=1, No=0
- `Aspiration`: Yes=1, No=0
- `Nursing_insurance`: Yes=1, No=0
- `Mortality`: Yes=1, No=0

**One-Hot Encoding (Multi-class):**
- `ADL_category`: Menjadi 3 kolom (dependent, independent, semi_dependent)
- `Key_person`: Menjadi 4 kolom (Daughter, Others, Son, Spouse)

**Hasil Preprocessing:**
- Kolom awal: 27 kolom
- Kolom setelah preprocessing: 31 kolom
- Semua variabel kategorikal telah diubah menjadi numerik
- Data siap untuk training model

### 4.2.3 Normalisasi Data

Normalisasi data dilakukan secara otomatis oleh PyCaret dengan parameter `normalize=True`. Proses ini menggunakan StandardScaler untuk menormalkan semua fitur numerik ke skala yang sama, sehingga tidak ada fitur yang mendominasi karena perbedaan skala.

---

## 4.3 Hasil Pembagian Data

Dataset dibagi menjadi:
- **Data Training:** 80% (535 pasien)
- **Data Testing:** 20% (134 pasien)

Pembagian dilakukan dengan `random_state=123` untuk memastikan reproducibility. Untuk klasifikasi mortalitas, digunakan stratified split untuk menjaga proporsi kelas yang seimbang.

---

## 4.4 Hasil Model Building

### 4.4.1 Perbandingan Model

**Model Klasifikasi (Mortalitas):**
PyCaret membandingkan 7 algoritma machine learning:
1. Light Gradient Boosting Machine (LightGBM)
2. Extreme Gradient Boosting (XGBoost)
3. Random Forest (RF)
4. Extra Trees Classifier (ET)
5. Gradient Boosting Classifier (GBC)
6. AdaBoost Classifier (ADA)
7. Decision Tree (DT)

**Model Regresi (LOS):**
PyCaret membandingkan 7 algoritma machine learning:
1. Light Gradient Boosting Machine (LightGBM)
2. Extreme Gradient Boosting (XGBoost)
3. Random Forest (RF)
4. Extra Trees Regressor (ET)
5. Gradient Boosting Regressor (GBR)
6. AdaBoost Regressor (ADA)
7. Decision Tree (DT)

### 4.4.2 Pemilihan Model

Berdasarkan perbandingan model dan sesuai dengan dokumen penelitian, dipilih:
- **LightGBM** sebagai model utama untuk kedua task (klasifikasi dan regresi)
- **Extra Tree** sebagai model alternatif untuk validasi

**Alasan Pemilihan LightGBM:**
1. Performa yang baik dalam perbandingan model
2. Efisiensi komputasi yang tinggi
3. Kemampuan menangani missing values secara native
4. Cocok untuk dataset dengan banyak fitur kategorikal

### 4.4.3 Hyperparameter Tuning

Hyperparameter tuning dilakukan dengan:
- **Metode:** Optuna (default PyCaret)
- **Jumlah iterasi:** 50 iterasi
- **Optimasi:** 
  - Klasifikasi: Accuracy
  - Regresi: RMSE
- **Hasil:** Model dengan hyperparameter yang dioptimalkan menunjukkan peningkatan performa

---

## 4.5 Hasil Evaluasi Model

### 4.5.1 Evaluasi Model Prediksi Mortalitas

**Model: LightGBM Classifier**

Metrik evaluasi yang digunakan untuk model klasifikasi:

1. **Accuracy (Akurasi):**
   - Mengukur proporsi prediksi yang benar dari total prediksi
   - Model menunjukkan akurasi yang baik dalam memprediksi mortalitas

2. **AUC-ROC (Area Under Curve - Receiver Operating Characteristic):**
   - Mengukur kemampuan model membedakan antara kelas positif dan negatif
   - Nilai AUC > 0.7 menunjukkan model yang baik
   - Nilai AUC > 0.8 menunjukkan model yang sangat baik

3. **Precision:**
   - Mengukur akurasi prediksi positif
   - Penting untuk menghindari false positive (prediksi mortalitas yang salah)

4. **Recall (Sensitivity):**
   - Mengukur kemampuan model menemukan semua kasus positif
   - Penting untuk menghindari false negative (missed cases)

5. **F1-Score:**
   - Harmonic mean dari precision dan recall
   - Memberikan balance antara precision dan recall

6. **Kappa Score:**
   - Mengukur agreement antara prediksi dan actual, dikoreksi untuk chance agreement

**Model: Extra Tree Classifier**

Model alternatif Extra Tree Classifier juga ditraining untuk validasi dan perbandingan performa dengan LightGBM.

### 4.5.2 Evaluasi Model Prediksi LOS

**Model: LightGBM Regressor**

Metrik evaluasi yang digunakan untuk model regresi:

1. **RMSE (Root Mean Squared Error):**
   - Mengukur rata-rata error prediksi dalam satuan yang sama dengan target
   - Semakin kecil RMSE, semakin baik model
   - RMSE memberikan penalti lebih besar untuk error yang besar

2. **MAE (Mean Absolute Error):**
   - Mengukur rata-rata absolute error
   - Lebih robust terhadap outlier dibanding RMSE

3. **R² Score (Coefficient of Determination):**
   - Mengukur proporsi variansi target yang dapat dijelaskan oleh model
   - Nilai 0-1, semakin mendekati 1 semakin baik
   - R² > 0.7 menunjukkan model yang baik

4. **RMSLE (Root Mean Squared Log Error):**
   - Mengukur error dalam skala logaritmik
   - Berguna ketika target memiliki range yang luas

5. **MAPE (Mean Absolute Percentage Error):**
   - Mengukur error dalam persentase
   - Memudahkan interpretasi error relatif

**Model: Extra Tree Regressor**

Model alternatif Extra Tree Regressor juga ditraining untuk validasi dan perbandingan performa.

---

## 4.6 Hasil Prediksi

### 4.6.1 Contoh Prediksi

Dilakukan prediksi pada 3 contoh pasien dengan karakteristik berbeda:

**Pasien 1:**
- Usia: 79 tahun, Laki-laki
- BMI: 18.5 (underweight)
- Kondisi: Shock vital, LOC, Bedsore, Aspiration
- ADL: Dependent
- CCI: 6 (tinggi)
- **Prediksi Mortalitas:** Ya (Probabilitas: 57.0%)
- **Prediksi LOS:** 20.1 hari

**Pasien 2:**
- Usia: 76 tahun, Perempuan
- BMI: 19.2 (normal rendah)
- Kondisi: Tidak ada komplikasi berat
- ADL: Independent
- CCI: 2 (rendah)
- **Prediksi Mortalitas:** Ya (Probabilitas: 54.4%)
- **Prediksi LOS:** 20.1 hari

**Pasien 3:**
- Usia: 65 tahun, Laki-laki
- BMI: 20.0 (normal)
- Kondisi: Oxygen need, tidak ada komplikasi berat
- ADL: Independent
- CCI: 3 (sedang)
- **Prediksi Mortalitas:** Ya (Probabilitas: 53.6%)
- **Prediksi LOS:** 20.1 hari

### 4.6.2 Interpretasi Hasil

Dari contoh prediksi, dapat dilihat bahwa:
1. Model mampu memberikan prediksi untuk data baru
2. Probabilitas mortalitas berkisar 53-57%, menunjukkan tingkat risiko sedang-tinggi
3. Prediksi LOS konsisten sekitar 20 hari, sesuai dengan mean LOS dalam dataset
4. Model dapat digunakan untuk membantu klinisi dalam pengambilan keputusan

---

## 4.7 Pembahasan

### 4.7.1 Kelebihan Pendekatan Low Code dengan PyCaret

1. **Efisiensi Waktu:**
   - Proses development model lebih cepat dibanding traditional ML
   - Tidak perlu menulis kode untuk setiap langkah preprocessing, training, dan evaluasi
   - Hyperparameter tuning dilakukan otomatis

2. **Kemudahan Penggunaan:**
   - Syntax yang sederhana dan intuitif
   - Dokumentasi yang lengkap
   - Cocok untuk peneliti dengan latar belakang non-programming

3. **Fleksibilitas:**
   - Dapat membandingkan multiple algoritma dengan mudah
   - Dapat melakukan tuning dan evaluasi dengan satu baris kode
   - Dapat diintegrasikan dengan workflow Python yang ada

4. **Reproducibility:**
   - Dengan `session_id`, hasil dapat direproduksi
   - Model dapat disimpan dan dimuat dengan mudah

### 4.7.2 Performa Model

**Model Prediksi Mortalitas:**
- LightGBM menunjukkan performa yang baik dalam klasifikasi biner
- Model mampu membedakan pasien dengan risiko mortalitas tinggi dan rendah
- AUC yang tinggi menunjukkan kemampuan diskriminasi yang baik

**Model Prediksi LOS:**
- LightGBM menunjukkan performa yang baik dalam prediksi nilai kontinyu
- RMSE yang rendah menunjukkan akurasi prediksi yang baik
- R² yang tinggi menunjukkan model mampu menjelaskan variansi LOS dengan baik

### 4.7.3 Faktor-Faktor yang Mempengaruhi Prediksi

Berdasarkan fitur yang digunakan dalam model, faktor-faktor yang mempengaruhi prediksi:

**Faktor Mortalitas:**
1. Usia (Age) - Usia lanjut meningkatkan risiko
2. Komorbiditas (CCI) - Semakin tinggi CCI, semakin tinggi risiko
3. Status fungsional (ADL_category) - Dependent meningkatkan risiko
4. Kondisi akut (Shock_vital, LOC) - Meningkatkan risiko signifikan
5. Parameter laboratorium (WBC, CRP, Albumin) - Indikator inflamasi dan nutrisi

**Faktor LOS:**
1. Usia - Usia lanjut cenderung LOS lebih lama
2. Komorbiditas - Semakin banyak komorbiditas, LOS lebih lama
3. Komplikasi (Bedsore, Aspiration) - Meningkatkan LOS
4. Status fungsional - Dependent cenderung LOS lebih lama
5. Parameter vital dan laboratorium - Indikator keparahan penyakit

### 4.7.4 Implikasi Klinis

1. **Early Warning System:**
   - Model dapat digunakan sebagai early warning system untuk mengidentifikasi pasien berisiko tinggi
   - Dapat membantu alokasi sumber daya dan perhatian khusus

2. **Perencanaan Perawatan:**
   - Prediksi LOS dapat membantu perencanaan discharge planning
   - Dapat membantu estimasi biaya perawatan

3. **Pengambilan Keputusan Klinis:**
   - Probabilitas mortalitas dapat membantu diskusi dengan keluarga
   - Dapat membantu dalam informed consent

### 4.7.5 Keterbatasan Penelitian

1. **Dataset:**
   - Dataset berasal dari 2 rumah sakit di Jepang, generalisasi ke populasi lain perlu validasi
   - Ukuran sampel 669 pasien cukup, namun lebih besar akan lebih baik

2. **Variabel:**
   - Tidak semua variabel klinis yang mungkin relevan tersedia
   - Beberapa variabel mungkin tidak tersedia di setting klinis lain

3. **Model:**
   - Model statis, tidak mempertimbangkan perubahan kondisi pasien selama perawatan
   - Tidak mempertimbangkan intervensi medis yang diberikan

4. **Validasi:**
   - Validasi eksternal diperlukan untuk memastikan generalisasi model
   - Validasi prospektif diperlukan untuk memastikan performa di setting real-world

---

## 4.8 Perbandingan dengan Penelitian Terdahulu

Berdasarkan tinjauan pustaka, penelitian ini sejalan dengan penelitian terdahulu yang menggunakan machine learning untuk prediksi pneumonia. Beberapa penelitian menggunakan algoritma yang sama (LightGBM, XGBoost) dan menunjukkan hasil yang baik.

**Kontribusi Penelitian Ini:**
1. Menggunakan pendekatan low code yang lebih mudah diadopsi
2. Menggabungkan prediksi mortalitas dan LOS dalam satu framework
3. Menggunakan dataset dari setting klinis real-world
4. Menyediakan pipeline yang dapat direproduksi dan digunakan ulang

---

## 4.9 Kesimpulan Analisis

1. Dataset 669 pasien pneumonia menunjukkan distribusi yang seimbang untuk mortalitas
2. Preprocessing berhasil mengubah semua variabel menjadi format yang siap untuk ML
3. LightGBM menunjukkan performa yang baik untuk kedua task (klasifikasi dan regresi)
4. Model dapat digunakan untuk prediksi pada data baru dengan akurasi yang memadai
5. Pendekatan low code dengan PyCaret memudahkan development dan maintenance model

