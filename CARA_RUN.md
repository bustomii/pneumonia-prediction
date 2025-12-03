# Cara Menjalankan Script Prediksi Pneumonia

## Catatan Penting
Script ini menggunakan scikit-learn dan LightGBM langsung (tanpa PyCaret) untuk kompatibilitas dengan Python 3.13.

## Troubleshooting

### Error: "externally-managed-environment"
Error ini terjadi karena pip mencoba install ke Python sistem, bukan ke virtual environment. Solusi:

1. **Pastikan virtual environment aktif:**
```bash
# Cek apakah prompt menampilkan (venv)
# Jika tidak, aktifkan:
source venv/bin/activate
```

2. **Verifikasi virtual environment aktif:**
```bash
# Di macOS, venv biasanya hanya punya python3, bukan python
# Cek lokasi Python yang digunakan
which python3
# Harus menampilkan: .../pneumonia-predictions/venv/bin/python3

# Cek lokasi pip
which pip3
# Harus menampilkan: .../pneumonia-predictions/venv/bin/pip3
```

3. **Jika virtual environment tidak ada atau rusak, buat ulang:**
```bash
# Hapus venv lama
rm -rf venv

# Buat venv baru (gunakan Python 3.11 untuk PyCaret)
python3.11 -m venv venv

# Aktifkan
source venv/bin/activate

# Install dependencies (gunakan python3 di macOS)
python3 -m pip install -r requirements.txt
```

**Catatan macOS:** Di macOS, virtual environment biasanya hanya menyediakan `python3` dan `pip3`, bukan `python` dan `pip`. Ini normal dan tidak masalah. Gunakan `python3` dan `pip3` setelah venv aktif.

### Error: "command not found: pip" atau "command not found: python"
Di macOS, venv biasanya hanya menyediakan `python3` dan `pip3`, bukan `python` dan `pip`. Ini normal.

Gunakan:
```bash
# Setelah venv aktif
python3 -m pip install -r requirements.txt
# atau
pip3 install -r requirements.txt
```

### Error: "command not found: python"
Gunakan `python3` sebagai gantinya:
```bash
python3 main.py
```

### Virtual Environment tidak aktif
Pastikan prompt terminal menampilkan `(venv)` di depan. Jika tidak, aktifkan dengan:
```bash
source venv/bin/activate
```

## Persiapan

1. Pastikan virtual environment sudah aktif:
```bash
source venv/bin/activate
```

2. Install dependencies (jika belum):
```bash
# PENTING: Pastikan virtual environment aktif terlebih dahulu!
# Cek dengan: which python3 (harus menunjuk ke venv/bin/python3)

# Install dependencies (di macOS, gunakan python3 dari venv)
python3 -m pip install -r requirements.txt

# Atau jika pip3 tersedia di venv:
# pip3 install -r requirements.txt
```

**Catatan Penting:** 
- Jangan install packages ke Python sistem (akan error "externally-managed-environment")
- Selalu pastikan virtual environment aktif sebelum install (cek prompt menampilkan `(venv)`)
- Di macOS, venv biasanya hanya punya `python3` dan `pip3`, bukan `python` dan `pip` - ini normal
- Setelah venv aktif, `python3` akan menggunakan Python dari venv, bukan sistem

**Dependencies utama:**
- scikit-learn
- pandas
- numpy
- lightgbm
- joblib
- openpyxl
- python-docx (untuk generate dokumentasi .docx)

## Menjalankan Script

Jalankan script utama dengan perintah:

```bash
# Setelah virtual environment aktif, gunakan python3 (dari venv)
python3 main.py
```

**Catatan:** 
- Di macOS, setelah `source venv/bin/activate`, gunakan `python3` (bukan `python`)
- Meskipun menggunakan `python3`, ini akan menggunakan Python dari virtual environment, bukan sistem
- Cek dengan `which python3` untuk memastikan menggunakan Python dari venv

## Alur Eksekusi

Script akan menjalankan 4 langkah utama:

1. **Data Preprocessing** - Memuat dan memproses data dari `data/data-669-patients.xlsx`
   - Eksplorasi data
   - Handle missing values
   - Encode variabel kategorikal
   - Simpan data yang sudah diproses ke `data/processed_pneumonia_data.csv`

2. **Training Model Mortalitas** - Melatih model untuk prediksi mortalitas
   - Model LightGBM
   - Model Extra Tree Classifier
   - Model disimpan di `models/mortality_model` dan `models/mortality_et_model`

3. **Training Model LOS** - Melatih model untuk prediksi Length of Stay
   - Model LightGBM Regressor
   - Model Extra Tree Regressor
   - Model disimpan di `models/los_model` dan `models/los_et_model`

4. **Contoh Prediksi** - Melakukan prediksi pada data contoh
   - Hasil prediksi disimpan di `results/predictions.csv`

## Struktur Data

Dataset yang digunakan: `data/data-669-patients.xlsx`

**Kolom Target:**
- `Mortality` - Prediksi mortalitas (Yes/No)
- `LOS_days` - Prediksi Length of Stay dalam hari

**Kolom Fitur:**
- `Age`, `Sex`, `BMI`
- `Heart_rate`, `Respiration_rate`, `Temperature`, `Systolic_BP`
- `Oxygen_need`, `Shock_vital`
- `WBC`, `Hemoglobin`, `Platelet`
- `Total_protein`, `Albumin`, `Sodium`, `BUN`, `CRP`
- `LOC`, `Bedsore`, `Aspiration`
- `ADL_category`, `CCI`
- `Nursing_insurance`, `Key_person`

## Output

- **Data yang sudah diproses:** `data/processed_pneumonia_data.csv`
- **Model mortalitas:** `models/mortality_model`, `models/mortality_et_model`
- **Model LOS:** `models/los_model`, `models/los_et_model`
- **Hasil prediksi:** `results/predictions.csv`

## Generate Dokumentasi (.docx)

Untuk menghasilkan dokumentasi BAB 4 dan BAB 5 dalam format .docx:

```bash
# Pastikan virtual environment aktif dan python-docx sudah terinstall
cd reports/dokumentasi

# Generate dokumen
python3 generate_docx.py
```

**Output:**
- `BAB_4_Analisis_dan_Pembahasan.docx`
- `BAB_5_Kesimpulan_dan_Saran.docx`

**Catatan:** Pastikan `python-docx` sudah terinstall dengan:
```bash
python3 -m pip install python-docx
```

