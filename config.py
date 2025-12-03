"""
File Konfigurasi untuk Project Prediksi Pneumonia
Sesuaikan parameter sesuai kebutuhan
"""

# ============================================================================
# PATH KONFIGURASI
# ============================================================================
RAW_DATA_PATH = "data/pneumonia_dataset.xlsx"
PROCESSED_DATA_PATH = "data/processed_pneumonia_data.csv"

# Path untuk model
MORTALITY_MODEL_PATH = "models/mortality_model"
MORTALITY_ET_MODEL_PATH = "models/mortality_et_model"
LOS_MODEL_PATH = "models/los_model"
LOS_ET_MODEL_PATH = "models/los_et_model"

# Path untuk hasil
RESULTS_PATH = "results/predictions.csv"

# ============================================================================
# KOLOM TARGET
# ============================================================================
MORTALITY_TARGET_COL = "mortality"  # Ganti jika nama kolom berbeda
LOS_TARGET_COL = "LOS"  # Ganti jika nama kolom berbeda

# ============================================================================
# PARAMETER TRAINING
# ============================================================================
TEST_SIZE = 0.2  # 20% untuk test, 80% untuk training
RANDOM_SEED = 123  # Untuk reproducibility

# Parameter PyCaret Setup
NORMALIZE = True
FEATURE_SELECTION = True
REMOVE_MULTICOLLINEARITY = True
MULTICOLLINEARITY_THRESHOLD = 0.95
IGNORE_LOW_VARIANCE = True

# Parameter Tuning
TUNING_N_ITER = 50  # Jumlah iterasi untuk hyperparameter tuning
MORTALITY_OPTIMIZE = 'Accuracy'  # Metrik untuk optimasi klasifikasi
LOS_OPTIMIZE = 'RMSE'  # Metrik untuk optimasi regresi

# ============================================================================
# MODEL YANG AKAN DICOMPARE
# ============================================================================
CLASSIFICATION_MODELS = ['lightgbm', 'xgboost', 'rf', 'et', 'gbc', 'ada', 'dt']
REGRESSION_MODELS = ['lightgbm', 'xgboost', 'rf', 'et', 'gbr', 'ada', 'dt']

# ============================================================================
# PARAMETER PREPROCESSING
# ============================================================================
MISSING_VALUE_STRATEGY = 'mean'  # 'mean', 'median', 'mode', atau 'drop'

# ============================================================================
# FITUR YANG DIGUNAKAN (Sesuai dokumen)
# ============================================================================
FEATURES = [
    'Age',
    'Sex',  # F/M atau 0/1
    'BMI',
    'Heart_rate',
    'Respiration',
    'Oxygen',  # Y/N atau 1/0
    'Shock_vital',  # Y/N atau 1/0
    'T',  # Temperature
    'WBC',  # White Blood Cell
    'Hgb',  # Hemoglobin
    'Platelet',
    'Total_protein',
    'Albumin',
    'Na',  # Sodium
    'BUN',  # Blood Urea Nitrogen
    'CRP',  # C-Reactive Protein
    'LOC',  # Level of Consciousness (Y/N atau 1/0)
    'Bedsore',  # Y/N atau 1/0
    'Aspiration',  # Y/N atau 1/0
    'ADL',  # Activities of Daily Living (0=independent, 1=semi-independent, 2=dependent)
    'CCI',  # Charlson Comorbidity Index
    'Insecure'  # Y/N atau 1/0
]

# ============================================================================
# CATATAN PENTING
# ============================================================================
"""
1. Pastikan dataset memiliki kolom sesuai dengan FEATURES di atas
2. Kolom target harus ada: MORTALITY_TARGET_COL dan LOS_TARGET_COL
3. Sesuaikan path sesuai struktur folder Anda
4. Untuk Google Colab, gunakan path relatif atau upload file
"""

