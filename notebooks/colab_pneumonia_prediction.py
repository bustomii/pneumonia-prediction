"""
Script untuk Google Colaboratory
Prediksi Mortalitas dan Rawat Inap Pasien Pneumonia menggunakan PyCaret
"""

# ============================================================================
# 1. INSTALL DEPENDENCIES
# ============================================================================
# Jalankan di cell pertama:
# !pip install pycaret pandas numpy matplotlib seaborn

# ============================================================================
# 2. IMPORT LIBRARIES
# ============================================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pycaret.classification import *
from pycaret.regression import *
import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# ============================================================================
# 3. LOAD DATASET
# ============================================================================
# Upload dataset ke Colab
from google.colab import files
uploaded = files.upload()

# Load dataset (ganti nama file sesuai dataset Anda)
df = pd.read_excel('pneumonia_dataset.xlsx')  # atau .csv
print(f"Data shape: {df.shape}")
print(f"\nKolom: {list(df.columns)}")
df.head()

# ============================================================================
# 4. DATA EXPLORATION
# ============================================================================
# Info dataset
print("=" * 60)
print("INFORMASI DATASET")
print("=" * 60)
df.info()
print("\n" + "=" * 60)
print("STATISTIK DESKRIPTIF")
print("=" * 60)
df.describe()

# Check missing values
print("\n" + "=" * 60)
print("MISSING VALUES")
print("=" * 60)
missing = df.isnull().sum()
print(missing[missing > 0])

# Visualisasi distribusi target (jika ada)
if 'mortality' in df.columns:
    plt.figure(figsize=(8, 5))
    df['mortality'].value_counts().plot(kind='bar')
    plt.title('Distribusi Mortalitas')
    plt.xlabel('Mortalitas')
    plt.ylabel('Jumlah')
    plt.show()

if 'LOS' in df.columns:
    plt.figure(figsize=(10, 5))
    df['LOS'].hist(bins=30)
    plt.title('Distribusi Length of Stay')
    plt.xlabel('LOS (hari)')
    plt.ylabel('Frekuensi')
    plt.show()

# ============================================================================
# 5. PREPROCESSING DATA
# ============================================================================
print("\n" + "=" * 60)
print("PREPROCESSING DATA")
print("=" * 60)

# Handle missing values
df = df.fillna(df.mean(numeric_only=True))  # Untuk numerik
df = df.fillna(df.mode().iloc[0])  # Untuk kategorikal

# Encode categorical jika perlu
# Contoh: df['Sex'] = df['Sex'].map({'M': 1, 'F': 0})

print("Preprocessing selesai!")
print(f"Data shape setelah preprocessing: {df.shape}")

# ============================================================================
# 6. TRAINING MODEL PREDIKSI MORTALITAS (KLASIFIKASI)
# ============================================================================
print("\n" + "=" * 60)
print("TRAINING MODEL PREDIKSI MORTALITAS")
print("=" * 60)

# Setup PyCaret untuk klasifikasi
clf = setup(
    data=df,
    target='mortality',  # Ganti dengan nama kolom target Anda
    train_size=0.8,
    session_id=123,
    normalize=True,
    feature_selection=True,
    remove_multicollinearity=True,
    multicollinearity_threshold=0.95,
    ignore_low_variance=True,
    silent=True
)

# Compare models
print("\nMembandingkan berbagai model...")
best_models = compare_models(
    include=['lightgbm', 'xgboost', 'rf', 'et', 'gbc', 'ada', 'dt'],
    sort='Accuracy',
    n_select=3
)

# Create LightGBM model (sesuai dokumen)
print("\nMembuat model LightGBM...")
lgbm_model = create_model('lightgbm')

# Tune model
print("\nTuning hyperparameters...")
tuned_lgbm = tune_model(lgbm_model, optimize='Accuracy', n_iter=50)

# Evaluate model
print("\nEvaluasi model...")
evaluate_model(tuned_lgbm)

# Finalize model
print("\nFinalizing model...")
final_mortality_model = finalize_model(tuned_lgbm)

# Save model
save_model(final_mortality_model, 'mortality_model')
print("\nModel mortalitas disimpan!")

# ============================================================================
# 7. TRAINING MODEL PREDIKSI LOS (REGRESI)
# ============================================================================
print("\n" + "=" * 60)
print("TRAINING MODEL PREDIKSI LENGTH OF STAY (LOS)")
print("=" * 60)

# Setup PyCaret untuk regresi
reg = setup(
    data=df,
    target='LOS',  # Ganti dengan nama kolom target Anda
    train_size=0.8,
    session_id=123,
    normalize=True,
    feature_selection=True,
    remove_multicollinearity=True,
    multicollinearity_threshold=0.95,
    ignore_low_variance=True,
    silent=True
)

# Compare models
print("\nMembandingkan berbagai model regresi...")
best_reg_models = compare_models(
    include=['lightgbm', 'xgboost', 'rf', 'et', 'gbr', 'ada', 'dt'],
    sort='RMSE',
    n_select=3
)

# Create LightGBM model
print("\nMembuat model LightGBM...")
lgbm_reg = create_model('lightgbm')

# Tune model
print("\nTuning hyperparameters...")
tuned_lgbm_reg = tune_model(lgbm_reg, optimize='RMSE', n_iter=50)

# Evaluate model
print("\nEvaluasi model...")
evaluate_model(tuned_lgbm_reg)

# Finalize model
print("\nFinalizing model...")
final_los_model = finalize_model(tuned_lgbm_reg)

# Save model
save_model(final_los_model, 'los_model')
print("\nModel LOS disimpan!")

# ============================================================================
# 8. PREDIKSI DATA BARU
# ============================================================================
print("\n" + "=" * 60)
print("PREDIKSI DATA BARU")
print("=" * 60)

# Load model
mortality_model = load_model('mortality_model')
los_model = load_model('los_model')

# Contoh data baru (ganti dengan data aktual)
new_data = pd.DataFrame({
    'Age': [79],
    'Sex': [1],  # 1=Male, 0=Female
    'BMI': [18.5],
    'Heart_rate': [100],
    'Respiration': [30],
    'Oxygen': [1],  # 1=Yes, 0=No
    'Shock_vital': [1],
    'T': [36.9],
    'WBC': [9.8],
    'Hgb': [11.2],
    'Platelet': [25.0],
    'Total_protein': [6.7],
    'Albumin': [2.8],
    'Na': [138],
    'BUN': [29],
    'CRP': [15.7],
    'LOC': [1],
    'Bedsore': [1],
    'Aspiration': [1],
    'ADL': [1],  # 0=independent, 1=semi-independent, 2=dependent
    'CCI': [6],
    'Insecure': [1]
    # Tambahkan semua fitur yang diperlukan
})

# Prediksi mortalitas
print("\nPrediksi Mortalitas:")
mortality_pred = predict_model(mortality_model, data=new_data)
print(f"Hasil: {mortality_pred['Label'].values[0]}")

# Prediksi LOS
print("\nPrediksi Length of Stay:")
los_pred = predict_model(los_model, data=new_data)
print(f"Hasil: {los_pred['Label'].values[0]:.2f} hari")

print("\n" + "=" * 60)
print("SELESAI!")
print("=" * 60)

