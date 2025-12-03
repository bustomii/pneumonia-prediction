"""
Script untuk melakukan prediksi menggunakan model yang sudah ditraining
"""

import pandas as pd
import numpy as np
from pycaret.classification import load_model, predict_model
from pycaret.regression import load_model as load_reg_model, predict_model as predict_reg_model
import warnings
warnings.filterwarnings('ignore')


def predict_mortality(new_data, model_path='../models/mortality_model'):
    """
    Prediksi mortalitas untuk data baru
    
    Parameters:
    -----------
    new_data : pd.DataFrame atau str
        Data baru untuk prediksi atau path ke file data
    model_path : str
        Path ke model yang sudah disimpan
    
    Returns:
    --------
    predictions : pd.DataFrame
        Data dengan kolom prediksi
    """
    
    print("=" * 60)
    print("PREDIKSI MORTALITAS")
    print("=" * 60)
    
    # Load data
    if isinstance(new_data, str):
        if new_data.endswith('.xlsx') or new_data.endswith('.xls'):
            df = pd.read_excel(new_data)
        else:
            df = pd.read_csv(new_data)
    else:
        df = new_data.copy()
    
    print(f"\nData shape: {df.shape}")
    
    # Load model
    print(f"\nLoading model dari: {model_path}")
    try:
        model = load_model(model_path)
        print("Model berhasil dimuat!")
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        return None
    
    # Predict
    print("\nMelakukan prediksi...")
    predictions = predict_model(model, data=df)
    
    print("\nPrediksi selesai!")
    print(f"\nHasil prediksi:")
    print(predictions[['Label', 'Score']].head(10) if 'Score' in predictions.columns else predictions['Label'].head(10))
    
    return predictions


def predict_los(new_data, model_path='../models/los_model'):
    """
    Prediksi Length of Stay untuk data baru
    
    Parameters:
    -----------
    new_data : pd.DataFrame atau str
        Data baru untuk prediksi atau path ke file data
    model_path : str
        Path ke model yang sudah disimpan
    
    Returns:
    --------
    predictions : pd.DataFrame
        Data dengan kolom prediksi LOS
    """
    
    print("=" * 60)
    print("PREDIKSI LENGTH OF STAY (LOS)")
    print("=" * 60)
    
    # Load data
    if isinstance(new_data, str):
        if new_data.endswith('.xlsx') or new_data.endswith('.xls'):
            df = pd.read_excel(new_data)
        else:
            df = pd.read_csv(new_data)
    else:
        df = new_data.copy()
    
    print(f"\nData shape: {df.shape}")
    
    # Load model
    print(f"\nLoading model dari: {model_path}")
    try:
        model = load_reg_model(model_path)
        print("Model berhasil dimuat!")
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        return None
    
    # Predict
    print("\nMelakukan prediksi...")
    predictions = predict_reg_model(model, data=df)
    
    print("\nPrediksi selesai!")
    print(f"\nHasil prediksi LOS:")
    print(predictions['Label'].describe())
    print(f"\nContoh prediksi:")
    print(predictions[['Label']].head(10))
    
    return predictions


def predict_both(new_data, mortality_model='../models/mortality_model', 
                 los_model='../models/los_model'):
    """
    Prediksi mortalitas dan LOS sekaligus
    
    Parameters:
    -----------
    new_data : pd.DataFrame atau str
        Data baru untuk prediksi
    mortality_model : str
        Path ke model mortalitas
    los_model : str
        Path ke model LOS
    
    Returns:
    --------
    results : pd.DataFrame
        Data dengan prediksi mortalitas dan LOS
    """
    
    print("=" * 60)
    print("PREDIKSI MORTALITAS DAN LENGTH OF STAY")
    print("=" * 60)
    
    # Prediksi mortalitas
    print("\n1. Prediksi Mortalitas...")
    mortality_pred = predict_mortality(new_data, mortality_model)
    
    # Prediksi LOS
    print("\n2. Prediksi Length of Stay...")
    los_pred = predict_los(new_data, los_model)
    
    if mortality_pred is None or los_pred is None:
        print("\nError: Gagal melakukan prediksi")
        return None
    
    # Combine results
    results = mortality_pred.copy()
    if 'Label' in los_pred.columns:
        results['Predicted_LOS'] = los_pred['Label']
    else:
        results['Predicted_LOS'] = los_pred.iloc[:, -1]  # Ambil kolom terakhir
    
    # Rename mortality prediction
    if 'Label' in results.columns:
        results.rename(columns={'Label': 'Predicted_Mortality'}, inplace=True)
    
    print("\n" + "=" * 60)
    print("HASIL PREDIKSI GABUNGAN")
    print("=" * 60)
    print(results[['Predicted_Mortality', 'Predicted_LOS']].head(10))
    
    return results


if __name__ == "__main__":
    # Contoh penggunaan
    print("Script Prediksi Pneumonia")
    print("=" * 60)
    
    # Contoh data baru (ganti dengan data aktual Anda)
    sample_data = pd.DataFrame({
        'Age': [79, 76, 65],
        'Sex': [1, 0, 1],  # 1=Male, 0=Female
        'BMI': [18.5, 19.2, 20.0],
        'Heart_rate': [100, 95, 90],
        'Respiration': [30, 24, 22],
        'Oxygen': [1, 0, 1],
        'Shock_vital': [1, 0, 0],
        'T': [36.9, 37.6, 37.0],
        'WBC': [9.8, 10.3, 8.5],
        'Hgb': [11.2, 11.8, 12.0],
        'Platelet': [25.0, 21.6, 22.0],
        'Total_protein': [6.7, 6.8, 7.0],
        'Albumin': [2.8, 3.3, 3.0],
        'Na': [138, 137, 139],
        'BUN': [29, 19, 20],
        'CRP': [15.7, 8.6, 10.0],
        'LOC': [1, 0, 0],
        'Bedsore': [1, 0, 0],
        'Aspiration': [1, 0, 0],
        'ADL': [1, 0, 0],  # 0=independent, 1=semi-independent, 2=dependent
        'CCI': [6, 2, 3],
        'Insecure': [1, 0, 0]
    })
    
    # Prediksi
    results = predict_both(sample_data)
    
    if results is not None:
        # Save results
        output_path = '../results/predictions.csv'
        results.to_csv(output_path, index=False)
        print(f"\nHasil prediksi disimpan ke: {output_path}")

