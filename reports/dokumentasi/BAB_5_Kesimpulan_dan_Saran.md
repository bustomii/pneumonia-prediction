# BAB V
# KESIMPULAN DAN SARAN

## 5.1 Kesimpulan

Berdasarkan hasil penelitian yang telah dilakukan, dapat ditarik beberapa kesimpulan sebagai berikut:

### 5.1.1 Kesimpulan Umum

1. **Pendekatan Low Code dengan PyCaret berhasil diimplementasikan** untuk mengembangkan model prediksi mortalitas dan length of stay (LOS) pasien pneumonia. Pendekatan ini terbukti efisien dan memudahkan proses development model machine learning tanpa perlu menulis kode yang kompleks.

2. **Dataset 669 pasien pneumonia** dari 2 rumah sakit di Jepang berhasil diproses dan digunakan untuk training model. Dataset menunjukkan karakteristik yang baik dengan distribusi mortalitas yang seimbang (50.4% vs 49.6%) dan tidak ada missing values.

3. **Model LightGBM menunjukkan performa yang baik** untuk kedua task:
   - **Prediksi Mortalitas (Klasifikasi):** Model mampu membedakan pasien dengan risiko mortalitas tinggi dan rendah dengan akurasi dan AUC yang baik
   - **Prediksi LOS (Regresi):** Model mampu memprediksi length of stay dengan RMSE dan R² yang memadai

4. **Proses preprocessing berhasil** mengubah 27 kolom menjadi 31 kolom setelah encoding, dengan semua variabel kategorikal diubah menjadi numerik. Data siap untuk training model machine learning.

5. **Model dapat digunakan untuk prediksi pada data baru** dengan hasil yang konsisten. Contoh prediksi menunjukkan model mampu memberikan probabilitas mortalitas dan estimasi LOS yang masuk akal.

### 5.1.2 Kesimpulan Spesifik

**Terkait Eksplorasi Data:**
- Dataset terdiri dari 669 pasien dengan karakteristik demografis yang bervariasi
- Distribusi mortalitas seimbang, tidak ada class imbalance yang signifikan
- LOS memiliki mean 20.09 hari dengan standar deviasi 10.94 hari
- Tidak ada missing values dalam dataset

**Terkait Preprocessing:**
- Cleaning data berhasil dengan menghapus identifier (Patient_ID)
- Encoding kategorikal berhasil: 8 variabel binary di-label encode, 2 variabel multi-class di-one-hot encode
- Normalisasi dilakukan otomatis oleh PyCaret
- Data siap untuk training dengan 31 fitur

**Terkait Model Building:**
- PyCaret berhasil membandingkan 7 algoritma untuk setiap task
- LightGBM dipilih sebagai model utama berdasarkan performa dan kesesuaian dengan dokumen
- Extra Tree digunakan sebagai model alternatif untuk validasi
- Hyperparameter tuning dengan 50 iterasi berhasil meningkatkan performa model

**Terkait Evaluasi Model:**
- Model klasifikasi dievaluasi dengan Accuracy, AUC, Precision, Recall, F1-Score, dan Kappa
- Model regresi dievaluasi dengan RMSE, MAE, R², RMSLE, dan MAPE
- Kedua model menunjukkan performa yang memadai untuk digunakan dalam setting klinis

**Terkait Prediksi:**
- Model berhasil melakukan prediksi pada data baru
- Probabilitas mortalitas dapat diinterpretasikan untuk pengambilan keputusan klinis
- Prediksi LOS memberikan estimasi yang masuk akal sesuai dengan distribusi data training

### 5.1.3 Pencapaian Tujuan Penelitian

1. ✅ **Tujuan 1:** Mengembangkan model prediksi mortalitas pasien pneumonia menggunakan machine learning dengan low code PyCaret - **TERCAPAI**

2. ✅ **Tujuan 2:** Mengembangkan model prediksi length of stay (LOS) pasien pneumonia menggunakan machine learning dengan low code PyCaret - **TERCAPAI**

3. ✅ **Tujuan 3:** Mengevaluasi performa model menggunakan metrik yang sesuai (Accuracy, AUC untuk klasifikasi; RMSE, R² untuk regresi) - **TERCAPAI**

4. ✅ **Tujuan 4:** Membuat pipeline yang dapat digunakan untuk prediksi pada data baru - **TERCAPAI**

---

## 5.2 Saran

Berdasarkan hasil penelitian dan keterbatasan yang ditemukan, berikut adalah saran untuk pengembangan lebih lanjut:

### 5.2.1 Saran untuk Penelitian Lanjutan

1. **Validasi Eksternal:**
   - Melakukan validasi model pada dataset dari rumah sakit atau negara lain
   - Menguji generalisasi model pada populasi yang berbeda
   - Validasi prospektif untuk memastikan performa di setting real-world

2. **Peningkatan Dataset:**
   - Mengumpulkan data dari lebih banyak rumah sakit untuk meningkatkan generalisasi
   - Menambah jumlah sampel untuk meningkatkan power statistik
   - Menambahkan variabel klinis yang mungkin relevan (misalnya: hasil kultur, jenis antibiotik, dll)

3. **Pengembangan Model:**
   - Mencoba algoritma deep learning untuk perbandingan performa
   - Mengembangkan model dinamis yang mempertimbangkan perubahan kondisi pasien selama perawatan
   - Mengintegrasikan data time-series untuk memodelkan perkembangan penyakit

4. **Interpretabilitas Model:**
   - Menggunakan teknik explainable AI (XAI) seperti SHAP values untuk menjelaskan prediksi
   - Mengidentifikasi fitur-fitur yang paling penting dalam prediksi
   - Membuat visualisasi yang mudah dipahami oleh klinisi

5. **Integrasi dengan Sistem Klinis:**
   - Mengembangkan API atau web service untuk integrasi dengan sistem informasi rumah sakit
   - Membuat dashboard untuk visualisasi prediksi dan monitoring
   - Mengintegrasikan dengan electronic health record (EHR)

### 5.2.2 Saran untuk Implementasi Klinis

1. **Pilot Study:**
   - Melakukan pilot study di satu atau beberapa rumah sakit
   - Mengumpulkan feedback dari klinisi tentang kegunaan dan akurasi prediksi
   - Menyesuaikan model berdasarkan feedback

2. **Training Klinisi:**
   - Memberikan training kepada klinisi tentang interpretasi hasil prediksi
   - Menjelaskan keterbatasan model dan kapan tidak boleh digunakan
   - Menekankan bahwa prediksi adalah alat bantu, bukan pengganti judgment klinis

3. **Monitoring dan Update:**
   - Membuat sistem monitoring untuk performa model secara berkala
   - Update model secara berkala dengan data baru
   - Retraining model ketika performa menurun

4. **Etika dan Regulasi:**
   - Memastikan compliance dengan regulasi kesehatan data (misalnya: GDPR, HIPAA)
   - Mendapatkan approval dari ethics committee
   - Memastikan informed consent untuk penggunaan data

### 5.2.3 Saran untuk Pengembangan Teknis

1. **Optimasi Kode:**
   - Mengoptimalkan kode untuk performa yang lebih baik
   - Menambahkan error handling yang lebih robust
   - Menambahkan logging untuk debugging dan monitoring

2. **Dokumentasi:**
   - Menyediakan dokumentasi yang lebih lengkap untuk pengguna
   - Membuat tutorial video atau interaktif
   - Menyediakan contoh penggunaan untuk berbagai skenario

3. **Testing:**
   - Menambahkan unit test untuk setiap fungsi
   - Menambahkan integration test untuk seluruh pipeline
   - Menambahkan test untuk edge cases

4. **Deployment:**
   - Mengembangkan containerization (Docker) untuk kemudahan deployment
   - Menyediakan cloud deployment option
   - Membuat CI/CD pipeline untuk automated testing dan deployment

### 5.2.4 Saran untuk Penelitian Lain

1. **Perbandingan dengan Metode Lain:**
   - Membandingkan dengan metode tradisional (skor klinis, rule-based)
   - Membandingkan dengan deep learning approaches
   - Membandingkan dengan ensemble methods yang lebih kompleks

2. **Aplikasi pada Penyakit Lain:**
   - Menerapkan pendekatan yang sama pada penyakit infeksi lain
   - Mengembangkan model untuk komplikasi pneumonia
   - Menerapkan pada prediksi kebutuhan ICU atau ventilator

3. **Integrasi Multi-modal Data:**
   - Mengintegrasikan data imaging (X-ray, CT scan)
   - Mengintegrasikan data laboratorium time-series
   - Mengintegrasikan data genetik atau biomarker

4. **Personalized Medicine:**
   - Mengembangkan model yang mempertimbangkan karakteristik individu pasien
   - Mengintegrasikan dengan data genetik untuk personalized treatment
   - Mengembangkan model untuk prediksi response terhadap treatment tertentu

---

## 5.3 Kontribusi Penelitian

Penelitian ini memberikan kontribusi sebagai berikut:

### 5.3.1 Kontribusi Teoritis

1. **Demonstrasi Pendekatan Low Code:**
   - Membuktikan bahwa pendekatan low code dengan PyCaret dapat digunakan untuk mengembangkan model ML yang efektif
   - Menunjukkan bahwa tidak selalu diperlukan kode yang kompleks untuk menghasilkan model yang baik

2. **Metodologi yang Dapat Direproduksi:**
   - Menyediakan pipeline yang lengkap dan dapat direproduksi
   - Menyediakan dokumentasi yang jelas untuk setiap langkah
   - Memudahkan peneliti lain untuk mengadopsi atau memodifikasi pendekatan

### 5.3.2 Kontribusi Praktis

1. **Tool untuk Klinisi:**
   - Menyediakan tool yang dapat membantu klinisi dalam pengambilan keputusan
   - Dapat digunakan sebagai early warning system
   - Dapat membantu dalam perencanaan perawatan

2. **Efisiensi Sumber Daya:**
   - Prediksi LOS dapat membantu perencanaan alokasi tempat tidur
   - Prediksi mortalitas dapat membantu alokasi perhatian dan sumber daya
   - Dapat mengurangi biaya dengan perencanaan yang lebih baik

3. **Kemudahan Implementasi:**
   - Kode yang sederhana memudahkan maintenance dan update
   - Dapat diintegrasikan dengan sistem yang ada
   - Tidak memerlukan expertise ML yang mendalam untuk digunakan

### 5.3.3 Kontribusi untuk Penelitian Lanjutan

1. **Baseline untuk Perbandingan:**
   - Menyediakan baseline performa untuk penelitian lanjutan
   - Dapat digunakan sebagai benchmark untuk metode lain

2. **Dataset dan Pipeline:**
   - Dataset yang sudah diproses dapat digunakan untuk penelitian lain
   - Pipeline dapat diadaptasi untuk dataset atau penyakit lain

3. **Metodologi:**
   - Metodologi yang digunakan dapat diadopsi untuk penelitian serupa
   - Dapat dikembangkan lebih lanjut dengan teknik yang lebih advanced

---

## 5.4 Penutup

Penelitian ini berhasil mengembangkan model prediksi mortalitas dan length of stay pasien pneumonia menggunakan pendekatan low code dengan PyCaret. Model yang dihasilkan menunjukkan performa yang memadai dan dapat digunakan sebagai alat bantu dalam pengambilan keputusan klinis.

Pendekatan low code terbukti efektif dalam mempercepat proses development model machine learning tanpa mengorbankan kualitas hasil. Dengan dokumentasi yang lengkap dan kode yang dapat direproduksi, penelitian ini dapat menjadi dasar untuk pengembangan lebih lanjut dan implementasi di setting klinis.

Diharapkan penelitian ini dapat memberikan manfaat bagi:
- **Klinisi:** Sebagai alat bantu dalam pengambilan keputusan dan perencanaan perawatan
- **Rumah Sakit:** Sebagai tool untuk optimasi alokasi sumber daya
- **Peneliti:** Sebagai baseline dan metodologi untuk penelitian lanjutan
- **Pasien:** Sebagai kontribusi untuk perawatan yang lebih baik

Dengan terus berkembangnya teknologi machine learning dan ketersediaan data kesehatan, diharapkan model prediksi seperti ini dapat semakin berkembang dan memberikan manfaat yang lebih besar bagi sistem kesehatan.

