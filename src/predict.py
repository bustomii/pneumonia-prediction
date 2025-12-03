"""
Script untuk melakukan prediksi menggunakan model yang sudah ditraining
"""

import pandas as pd
import numpy as np
import os
from pycaret.classification import load_model, predict_model
from pycaret.regression import load_model as load_reg_model, predict_model as predict_reg_model
import warnings
warnings.filterwarnings('ignore')


def preprocess_data_for_prediction(df, reference_data_path='data/processed_pneumonia_data.csv', exclude_target=None):
    """
    Preprocess data baru agar formatnya sama dengan data training
    
    Parameters:
    -----------
    df : pd.DataFrame
        Data yang akan diproses
    reference_data_path : str
        Path ke data reference untuk mendapatkan semua kolom
    exclude_target : str atau None
        Target yang akan dikecualikan ('Mortality' atau 'LOS_days')
    """
    df = df.copy()
    
    # Drop Patient_ID jika ada
    if 'Patient_ID' in df.columns:
        df = df.drop(columns=['Patient_ID'])
    
    # Encode categorical variables seperti saat training
    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    # Hapus target dari categorical jika ada (untuk prediksi)
    if 'Mortality' in categorical_cols:
        categorical_cols.remove('Mortality')
    if 'LOS_days' in df.columns:
        # LOS_days harus tetap ada, tapi tidak perlu di-encode
        pass
    
    for col in categorical_cols:
        if col in df.columns:
            if df[col].nunique() == 2:  # Binary
                df[col] = le.fit_transform(df[col])
            else:  # Multi-class, gunakan one-hot encoding
                df = pd.get_dummies(df, columns=[col], prefix=col)
    
    # Pastikan semua kolom dari data training ada (tambahkan dengan nilai 0 jika tidak ada)
    try:
        # Load reference data untuk mendapatkan semua kolom
        project_root = os.path.dirname(os.path.dirname(__file__))
        ref_path = os.path.join(project_root, reference_data_path)
        if os.path.exists(ref_path):
            ref_df = pd.read_csv(ref_path, nrows=1)  # Hanya baca header
            # Ambil semua kolom dari reference
            ref_cols = list(ref_df.columns)
            
            # Hapus target yang dikecualikan jika ada
            if exclude_target and exclude_target in ref_cols:
                ref_cols.remove(exclude_target)
            
            # Tambahkan kolom yang hilang dengan nilai default
            missing_cols = [c for c in ref_cols if c not in df.columns]
            if missing_cols:
                print(f"Menambahkan {len(missing_cols)} kolom yang hilang...")
                for col in missing_cols:
                    # Untuk LOS_days, gunakan nilai default yang masuk akal
                    if col == 'LOS_days':
                        df[col] = 20  # Nilai default LOS (mean dari data)
                    elif col == 'Mortality':
                        df[col] = 0  # Default untuk Mortality (No)
                    else:
                        df[col] = 0
            
            # Pastikan urutan kolom sama dan semua kolom ada
            # Reorder sesuai reference
            df = df.reindex(columns=ref_cols, fill_value=0)
        else:
            print(f"Warning: File reference tidak ditemukan: {ref_path}")
    except Exception as e:
        print(f"Warning: Tidak bisa load reference data: {str(e)}")
        print("Menggunakan kolom yang ada saja...")
    
    return df


def predict_mortality(new_data, model_path='models/mortality_model'):
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
    
    print(f"\nData shape sebelum preprocessing: {df.shape}")
    
    # Preprocess data agar formatnya sama dengan data training
    # Untuk prediksi mortalitas, kita perlu semua kolom termasuk LOS_days
    df = preprocess_data_for_prediction(df, exclude_target='Mortality')
    
    print(f"Data shape setelah preprocessing: {df.shape}")
    
    # Load model - handle relative path
    if not os.path.isabs(model_path):
        # Jika path relatif, coba dari current dir atau dari project root
        if not os.path.exists(model_path):
            # Coba dengan path dari project root
            project_root = os.path.dirname(os.path.dirname(__file__))
            model_path = os.path.join(project_root, model_path)
    
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
    # PyCaret menggunakan 'prediction_label' dan 'prediction_score'
    if 'prediction_label' in predictions.columns:
        if 'prediction_score' in predictions.columns:
            print(predictions[['prediction_label', 'prediction_score']].head(10))
        else:
            print(predictions['prediction_label'].head(10))
    elif 'Label' in predictions.columns:
        if 'Score' in predictions.columns:
            print(predictions[['Label', 'Score']].head(10))
        else:
            print(predictions['Label'].head(10))
    else:
        # Tampilkan beberapa kolom terakhir (biasanya prediksi ada di kolom terakhir)
        print(predictions.iloc[:, -3:].head(10))
    
    return predictions


def predict_los(new_data, model_path='models/los_model'):
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
    
    print(f"\nData shape sebelum preprocessing: {df.shape}")
    
    # Preprocess data agar formatnya sama dengan data training
    # Untuk prediksi LOS, kita perlu semua kolom termasuk Mortality
    df = preprocess_data_for_prediction(df, exclude_target='LOS_days')
    
    print(f"Data shape setelah preprocessing: {df.shape}")
    
    # Load model - handle relative path
    if not os.path.isabs(model_path):
        # Jika path relatif, coba dari current dir atau dari project root
        if not os.path.exists(model_path):
            # Coba dengan path dari project root
            project_root = os.path.dirname(os.path.dirname(__file__))
            model_path = os.path.join(project_root, model_path)
    
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
    # PyCaret menggunakan 'prediction_label' untuk regresi
    if 'prediction_label' in predictions.columns:
        print(predictions['prediction_label'].describe())
        print(f"\nContoh prediksi:")
        print(predictions[['prediction_label']].head(10))
    elif 'Label' in predictions.columns:
        print(predictions['Label'].describe())
        print(f"\nContoh prediksi:")
        print(predictions[['Label']].head(10))
    else:
        # Gunakan kolom terakhir
        pred_col = predictions.columns[-1]
        print(predictions[pred_col].describe())
        print(f"\nContoh prediksi:")
        print(predictions[[pred_col]].head(10))
    
    return predictions


def predict_both(new_data, mortality_model='models/mortality_model', 
                 los_model='models/los_model'):
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
    
    # Ambil prediksi LOS (PyCaret menggunakan 'prediction_label')
    if 'prediction_label' in los_pred.columns:
        results['Predicted_LOS'] = los_pred['prediction_label'].values
    elif 'Label' in los_pred.columns:
        results['Predicted_LOS'] = los_pred['Label'].values
    else:
        # Gunakan kolom terakhir
        results['Predicted_LOS'] = los_pred.iloc[:, -1].values
    
    # Rename mortality prediction
    if 'prediction_label' in results.columns:
        results.rename(columns={'prediction_label': 'Predicted_Mortality'}, inplace=True)
        # Rename score juga jika ada
        if 'prediction_score' in results.columns:
            results.rename(columns={'prediction_score': 'Mortality_Probability'}, inplace=True)
    elif 'Label' in results.columns:
        results.rename(columns={'Label': 'Predicted_Mortality'}, inplace=True)
        if 'Score' in results.columns:
            results.rename(columns={'Score': 'Mortality_Probability'}, inplace=True)
    else:
        # Cari kolom prediksi
        pred_cols = [c for c in results.columns if 'prediction' in c.lower() or 'label' in c.lower()]
        if pred_cols:
            results.rename(columns={pred_cols[0]: 'Predicted_Mortality'}, inplace=True)
        else:
            # Gunakan kolom terakhir
            last_col = results.columns[-1]
            results.rename(columns={last_col: 'Predicted_Mortality'}, inplace=True)
    
    # Pastikan kolom yang ditampilkan ada
    display_cols = []
    if 'Predicted_Mortality' in results.columns:
        display_cols.append('Predicted_Mortality')
    if 'Mortality_Probability' in results.columns or 'Score' in results.columns:
        prob_col = 'Mortality_Probability' if 'Mortality_Probability' in results.columns else 'Score'
        display_cols.append(prob_col)
    if 'Predicted_LOS' in results.columns:
        display_cols.append('Predicted_LOS')
    
    print("\n" + "=" * 60)
    print("HASIL PREDIKSI GABUNGAN")
    print("=" * 60)
    if display_cols:
        print(results[display_cols].head(10))
    else:
        print(results.head(10))
    
    return results


if __name__ == "__main__":
    # Contoh penggunaan
    print("Script Prediksi Pneumonia")
    print("=" * 60)
    
    # Contoh data baru (ganti dengan data aktual Anda)
    # Gunakan nama kolom yang sama dengan data training
    sample_data = pd.DataFrame({
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
    results = predict_both(sample_data)
    
    if results is not None:
        # Save results - pastikan folder ada
        project_root = os.path.dirname(os.path.dirname(__file__))
        results_dir = os.path.join(project_root, 'results')
        os.makedirs(results_dir, exist_ok=True)
        output_path = os.path.join(results_dir, 'predictions.csv')
        results.to_csv(output_path, index=False)
        print(f"\nHasil prediksi disimpan ke: {output_path}")
