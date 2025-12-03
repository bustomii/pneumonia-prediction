# Cara Menggunakan predict.py untuk Prediksi

## 1. Prediksi dari Script Python

### Import fungsi yang diperlukan

```python
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / 'src'))

from predict import predict_mortality, predict_los, predict_both
import pandas as pd
```

### Contoh 1: Prediksi Mortalitas Saja

```python
# Data baru untuk prediksi
new_data = pd.DataFrame({
    'Age': [79, 76, 65],
    'Sex': ['M', 'F', 'M'],
    'BMI': [18.5, 19.2, 20.0],
    'Heart_rate': [100, 95, 90],
    'Respiration_rate': [30, 24, 22],
    'Temperature': [36.9, 37.6, 37.0],
    'Systolic_BP': [120, 130, 125],
    'Oxygen_need': ['Yes', 'No', 'Yes'],
    'Shock_vital': ['Yes', 'No', 'No'],
    'WBC': [9.8, 10.3, 8.5],
    'Hemoglobin': [11.2, 11.8, 12.0],
    'Platelet': [250, 216, 220],
    'Total_protein': [6.7, 6.8, 7.0],
    'Albumin': [2.8, 3.3, 3.0],
    'Sodium': [138, 137, 139],
    'BUN': [29, 19, 20],
    'CRP': [15.7, 8.6, 10.0],
    'LOC': ['Yes', 'No', 'No'],
    'Bedsore': ['Yes', 'No', 'No'],
    'Aspiration': ['Yes', 'No', 'No'],
    'ADL_category': ['Dependent', 'Independent', 'Independent'],
    'CCI': [6, 2, 3],
    'Nursing_insurance': ['Yes', 'Yes', 'No'],
    'Key_person': ['Son', 'Daughter', 'Spouse']
})

# Prediksi mortalitas
results = predict_mortality(new_data, model_path='models/mortality_model')
print(results)
```

### Contoh 2: Prediksi LOS Saja

```python
# Gunakan data yang sama
results = predict_los(new_data, model_path='models/los_model')
print(results)
```

### Contoh 3: Prediksi Keduanya (Mortalitas + LOS)

```python
# Prediksi mortalitas dan LOS sekaligus
results = predict_both(
    new_data,
    mortality_model='models/mortality_model',
    los_model='models/los_model'
)

# Simpan hasil
results.to_csv('results/predictions.csv', index=False)
print(results[['Predicted_Mortality', 'Predicted_LOS']])
```

## 2. Prediksi dari File Excel/CSV

### Dari File Excel

```python
# Prediksi dari file Excel
results = predict_both('data/data_baru.xlsx')
```

### Dari File CSV

```python
# Prediksi dari file CSV
results = predict_both('data/data_baru.csv')
```

## 3. Menjalankan Script Langsung

Jalankan script predict.py langsung:

```bash
cd /Users/bustomi/Public/Working/ai-generate/python/pneumonia-prediction
source venv/bin/activate
python src/predict.py
```

Script akan menggunakan data contoh yang sudah ada di dalam file.

## 4. Format Data Input

Data input harus memiliki kolom berikut:

### Kolom Wajib:
- `Age` (int): Usia pasien
- `Sex` (str): 'M' atau 'F'
- `BMI` (float): Body Mass Index
- `Heart_rate` (int): Denyut jantung
- `Respiration_rate` (int): Laju pernapasan
- `Temperature` (float): Suhu tubuh
- `Systolic_BP` (int): Tekanan darah sistolik
- `Oxygen_need` (str): 'Yes' atau 'No'
- `Shock_vital` (str): 'Yes' atau 'No'
- `WBC` (float): White Blood Cell count
- `Hemoglobin` (float): Kadar hemoglobin
- `Platelet` (int): Jumlah platelet
- `Total_protein` (float): Total protein
- `Albumin` (float): Kadar albumin
- `Sodium` (int): Kadar natrium
- `BUN` (int): Blood Urea Nitrogen
- `CRP` (float): C-Reactive Protein
- `LOC` (str): 'Yes' atau 'No' (Loss of Consciousness)
- `Bedsore` (str): 'Yes' atau 'No'
- `Aspiration` (str): 'Yes' atau 'No'
- `ADL_category` (str): 'Dependent', 'Independent', atau 'Semi-dependent'
- `CCI` (int): Charlson Comorbidity Index
- `Nursing_insurance` (str): 'Yes' atau 'No'
- `Key_person` (str): 'Son', 'Daughter', 'Spouse', atau 'Others'

### Kolom Opsional:
- `Patient_ID` (str): ID pasien (akan dihapus otomatis)
- `Mortality` (str): Jika ada, akan diabaikan saat prediksi
- `LOS_days` (int): Jika ada, akan diabaikan saat prediksi mortalitas

## 5. Output

### Prediksi Mortalitas:
- `Label`: Prediksi (0 = No, 1 = Yes)
- `Score`: Probabilitas (0-1)

### Prediksi LOS:
- `Label`: Prediksi Length of Stay dalam hari

### Prediksi Gabungan:
- `Predicted_Mortality`: Prediksi mortalitas
- `Mortality_Probability`: Probabilitas mortalitas
- `Predicted_LOS`: Prediksi Length of Stay (hari)

## 6. Contoh Script Lengkap

Buat file `predict_example.py`:

```python
"""
Contoh penggunaan predict.py
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / 'src'))

from predict import predict_both
import pandas as pd

# Data pasien baru
new_patients = pd.DataFrame({
    'Age': [79, 76, 65],
    'Sex': ['M', 'F', 'M'],
    'BMI': [18.5, 19.2, 20.0],
    'Heart_rate': [100, 95, 90],
    'Respiration_rate': [30, 24, 22],
    'Temperature': [36.9, 37.6, 37.0],
    'Systolic_BP': [120, 130, 125],
    'Oxygen_need': ['Yes', 'No', 'Yes'],
    'Shock_vital': ['Yes', 'No', 'No'],
    'WBC': [9.8, 10.3, 8.5],
    'Hemoglobin': [11.2, 11.8, 12.0],
    'Platelet': [250, 216, 220],
    'Total_protein': [6.7, 6.8, 7.0],
    'Albumin': [2.8, 3.3, 3.0],
    'Sodium': [138, 137, 139],
    'BUN': [29, 19, 20],
    'CRP': [15.7, 8.6, 10.0],
    'LOC': ['Yes', 'No', 'No'],
    'Bedsore': ['Yes', 'No', 'No'],
    'Aspiration': ['Yes', 'No', 'No'],
    'ADL_category': ['Dependent', 'Independent', 'Independent'],
    'CCI': [6, 2, 3],
    'Nursing_insurance': ['Yes', 'Yes', 'No'],
    'Key_person': ['Son', 'Daughter', 'Spouse']
})

# Prediksi
print("Melakukan prediksi...")
results = predict_both(new_patients)

# Tampilkan hasil
print("\n" + "="*60)
print("HASIL PREDIKSI")
print("="*60)
print(results[['Predicted_Mortality', 'Mortality_Probability', 'Predicted_LOS']])

# Simpan ke file
output_path = 'results/predictions_new.csv'
results.to_csv(output_path, index=False)
print(f"\nHasil disimpan ke: {output_path}")
```

Jalankan:
```bash
python predict_example.py
```

## Catatan Penting

1. **Pastikan model sudah ditraining** - Model harus ada di folder `models/`
2. **Format data harus benar** - Kolom harus sesuai dengan yang digunakan saat training
3. **Preprocessing otomatis** - Data akan di-preprocess otomatis sebelum prediksi
4. **Path model** - Jika model ada di lokasi lain, gunakan path absolut atau relatif yang benar

