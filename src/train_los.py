"""
Training Model untuk Prediksi Length of Stay (LOS) Pasien Pneumonia
Menggunakan PyCaret untuk Low Code Machine Learning (Regresi)
"""

import pandas as pd
import numpy as np
from pycaret.regression import *
import warnings
warnings.filterwarnings('ignore')


def train_los_model(data_path, target_col='LOS', test_size=0.2):
    """
    Train model untuk prediksi Length of Stay menggunakan PyCaret
    
    Parameters:
    -----------
    data_path : str
        Path ke dataset yang sudah diproses
    target_col : str
        Nama kolom target (LOS)
    test_size : float
        Proporsi data test (default 0.2 = 20%)
    """
    
    print("=" * 60)
    print("TRAINING MODEL PREDIKSI LENGTH OF STAY (LOS)")
    print("=" * 60)
    
    # Load data
    print("\n1. Loading data...")
    if data_path.endswith('.xlsx') or data_path.endswith('.xls'):
        df = pd.read_excel(data_path)
    else:
        df = pd.read_csv(data_path)
    
    print(f"   Data shape: {df.shape}")
    print(f"   Kolom: {list(df.columns)}")
    
    # Setup PyCaret untuk regresi
    print(f"\n2. Setup PyCaret Regression...")
    print(f"   Target: {target_col}")
    
    reg = setup(
        data=df,
        target=target_col,
        train_size=1-test_size,
        session_id=123,
        normalize=True,
        feature_selection=True,
        remove_multicollinearity=True,
        multicollinearity_threshold=0.95,
        ignore_low_variance=True,
        silent=True,
        verbose=False
    )
    
    print("   Setup selesai!")
    
    # Compare models
    print("\n3. Membandingkan berbagai model regresi...")
    best_models = compare_models(
        include=['lightgbm', 'xgboost', 'rf', 'et', 'gbr', 'ada', 'dt'],
        sort='RMSE',
        n_select=3,
        verbose=False
    )
    
    print("   Model terbaik:")
    for i, model in enumerate(best_models, 1):
        print(f"   {i}. {type(model).__name__}")
    
    # Pilih model LightGBM (sesuai dokumen)
    print("\n4. Memilih model LightGBM (sesuai dokumen)...")
    try:
        lgbm_model = create_model('lightgbm', verbose=False)
        print("   LightGBM model berhasil dibuat!")
    except:
        print("   LightGBM tidak tersedia, menggunakan model terbaik...")
        lgbm_model = best_models[0]
    
    # Tune model
    print("\n5. Tuning hyperparameters...")
    tuned_model = tune_model(
        lgbm_model,
        optimize='RMSE',
        n_iter=50,
        verbose=False
    )
    print("   Tuning selesai!")
    
    # Evaluate model
    print("\n6. Evaluasi model...")
    evaluate_model(tuned_model)
    
    # Finalize model
    print("\n7. Finalizing model...")
    final_model = finalize_model(tuned_model)
    print("   Model finalized!")
    
    # Save model
    model_path = '../models/los_model'
    save_model(final_model, model_path)
    print(f"\n8. Model disimpan ke: {model_path}")
    
    # Predictions
    print("\n9. Membuat prediksi pada test set...")
    predictions = predict_model(final_model)
    print("   Prediksi selesai!")
    
    return final_model, predictions


def train_extra_tree_regressor(data_path, target_col='LOS', test_size=0.2):
    """
    Train Extra Tree Regressor (sesuai dokumen)
    
    Parameters:
    -----------
    data_path : str
        Path ke dataset yang sudah diproses
    target_col : str
        Nama kolom target (LOS)
    test_size : float
        Proporsi data test
    """
    
    print("=" * 60)
    print("TRAINING EXTRA TREE REGRESSOR")
    print("=" * 60)
    
    # Load data
    print("\n1. Loading data...")
    if data_path.endswith('.xlsx') or data_path.endswith('.xls'):
        df = pd.read_excel(data_path)
    else:
        df = pd.read_csv(data_path)
    
    # Setup
    print("\n2. Setup PyCaret...")
    reg = setup(
        data=df,
        target=target_col,
        train_size=1-test_size,
        session_id=123,
        normalize=True,
        silent=True,
        verbose=False
    )
    
    # Create Extra Tree Regressor
    print("\n3. Membuat Extra Tree Regressor...")
    et_model = create_model('et', verbose=False)
    
    # Tune model
    print("\n4. Tuning model...")
    tuned_et = tune_model(et_model, optimize='RMSE', n_iter=50, verbose=False)
    
    # Evaluate
    print("\n5. Evaluasi model...")
    evaluate_model(tuned_et)
    
    # Finalize
    print("\n6. Finalizing model...")
    final_et = finalize_model(tuned_et)
    
    # Save
    model_path = '../models/los_et_model'
    save_model(final_et, model_path)
    print(f"\n7. Model disimpan ke: {model_path}")
    
    return final_et


if __name__ == "__main__":
    # Contoh penggunaan
    data_path = "../data/processed_pneumonia_data.csv"
    
    print("Training Model Prediksi Length of Stay")
    print("=" * 60)
    
    # Train LightGBM model
    model, predictions = train_los_model(
        data_path=data_path,
        target_col='LOS',
        test_size=0.2
    )
    
    # Train Extra Tree Regressor
    et_model = train_extra_tree_regressor(
        data_path=data_path,
        target_col='LOS',
        test_size=0.2
    )
    
    print("\n" + "=" * 60)
    print("TRAINING SELESAI!")
    print("=" * 60)

