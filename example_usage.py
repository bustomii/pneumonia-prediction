"""
Contoh Penggunaan Project Prediksi Pneumonia
File ini menunjukkan cara menggunakan berbagai fungsi yang tersedia
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / 'src'))

import pandas as pd
from data_preprocessing import DataPreprocessor
from train_mortality import train_mortality_model
from train_los import train_los_model
from predict import predict_mortality, predict_los, predict_both


# ============================================================================
# CONTOH 1: PREPROCESSING DATA
# ============================================================================
def example_preprocessing():
    """Contoh melakukan preprocessing data"""
    print("=" * 60)
    print("CONTOH 1: PREPROCESSING DATA")
    print("=" * 60)
    
    # Inisialisasi preprocessor
    data_path = "data/pneumonia_dataset.xlsx"  # Ganti dengan path dataset Anda
    preprocessor = DataPreprocessor(data_path)
    
    # Load data
    df = preprocessor.load_data()
    
    if df is not None:
        # Eksplorasi data
        preprocessor.explore_data()
        
        # Handle missing values
        preprocessor.handle_missing_values(strategy='mean')
        
        # Encode categorical
        preprocessor.encode_categorical()
        
        # Simpan data yang sudah diproses
        preprocessor.save_processed_data("data/processed_data.csv")
        print("\n✓ Preprocessing selesai!")


# ============================================================================
# CONTOH 2: TRAINING MODEL MORTALITAS
# ============================================================================
def example_train_mortality():
    """Contoh training model prediksi mortalitas"""
    print("\n" + "=" * 60)
    print("CONTOH 2: TRAINING MODEL MORTALITAS")
    print("=" * 60)
    
    data_path = "data/processed_data.csv"
    
    try:
        # Train model
        model, predictions = train_mortality_model(
            data_path=data_path,
            target_col='mortality',  # Sesuaikan dengan nama kolom di dataset
            test_size=0.2
        )
        print("\n✓ Model mortalitas berhasil ditraining!")
        return model
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        return None


# ============================================================================
# CONTOH 3: TRAINING MODEL LOS
# ============================================================================
def example_train_los():
    """Contoh training model prediksi LOS"""
    print("\n" + "=" * 60)
    print("CONTOH 3: TRAINING MODEL LOS")
    print("=" * 60)
    
    data_path = "data/processed_data.csv"
    
    try:
        # Train model
        model, predictions = train_los_model(
            data_path=data_path,
            target_col='LOS',  # Sesuaikan dengan nama kolom di dataset
            test_size=0.2
        )
        print("\n✓ Model LOS berhasil ditraining!")
        return model
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        return None


# ============================================================================
# CONTOH 4: PREDIKSI MORTALITAS
# ============================================================================
def example_predict_mortality():
    """Contoh melakukan prediksi mortalitas"""
    print("\n" + "=" * 60)
    print("CONTOH 4: PREDIKSI MORTALITAS")
    print("=" * 60)
    
    # Data baru untuk prediksi
    new_data = pd.DataFrame({
        'Age': [79],
        'Sex': [1],
        'BMI': [18.5],
        'Heart_rate': [100],
        'Respiration': [30],
        'Oxygen': [1],
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
        'ADL': [1],
        'CCI': [6],
        'Insecure': [1]
    })
    
    try:
        # Prediksi
        results = predict_mortality(
            new_data=new_data,
            model_path='models/mortality_model'
        )
        
        if results is not None:
            print("\n✓ Prediksi berhasil!")
            print(f"Hasil: {results['Label'].values[0]}")
            return results
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        return None


# ============================================================================
# CONTOH 5: PREDIKSI LOS
# ============================================================================
def example_predict_los():
    """Contoh melakukan prediksi LOS"""
    print("\n" + "=" * 60)
    print("CONTOH 5: PREDIKSI LOS")
    print("=" * 60)
    
    # Data baru untuk prediksi
    new_data = pd.DataFrame({
        'Age': [79],
        'Sex': [1],
        'BMI': [18.5],
        'Heart_rate': [100],
        'Respiration': [30],
        'Oxygen': [1],
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
        'ADL': [1],
        'CCI': [6],
        'Insecure': [1]
    })
    
    try:
        # Prediksi
        results = predict_los(
            new_data=new_data,
            model_path='models/los_model'
        )
        
        if results is not None:
            print("\n✓ Prediksi berhasil!")
            print(f"Hasil: {results['Label'].values[0]:.2f} hari")
            return results
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        return None


# ============================================================================
# CONTOH 6: PREDIKSI KEDUANYA (MORTALITAS + LOS)
# ============================================================================
def example_predict_both():
    """Contoh melakukan prediksi mortalitas dan LOS sekaligus"""
    print("\n" + "=" * 60)
    print("CONTOH 6: PREDIKSI MORTALITAS DAN LOS")
    print("=" * 60)
    
    # Data baru untuk prediksi
    new_data = pd.DataFrame({
        'Age': [79, 76, 65],
        'Sex': [1, 0, 1],
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
        'ADL': [1, 0, 0],
        'CCI': [6, 2, 3],
        'Insecure': [1, 0, 0]
    })
    
    try:
        # Prediksi keduanya
        results = predict_both(
            new_data=new_data,
            mortality_model='models/mortality_model',
            los_model='models/los_model'
        )
        
        if results is not None:
            print("\n✓ Prediksi berhasil!")
            print("\nHasil prediksi:")
            print(results[['Predicted_Mortality', 'Predicted_LOS']])
            
            # Simpan hasil
            results.to_csv('results/example_predictions.csv', index=False)
            print("\n✓ Hasil disimpan ke: results/example_predictions.csv")
            return results
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        return None


# ============================================================================
# MAIN
# ============================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("CONTOH PENGGUNAAN PROJECT PREDIKSI PNEUMONIA")
    print("=" * 60)
    print("\nPilih contoh yang ingin dijalankan:")
    print("1. Preprocessing Data")
    print("2. Training Model Mortalitas")
    print("3. Training Model LOS")
    print("4. Prediksi Mortalitas")
    print("5. Prediksi LOS")
    print("6. Prediksi Keduanya (Mortalitas + LOS)")
    print("0. Jalankan Semua")
    
    choice = input("\nMasukkan pilihan (0-6): ")
    
    if choice == '1':
        example_preprocessing()
    elif choice == '2':
        example_train_mortality()
    elif choice == '3':
        example_train_los()
    elif choice == '4':
        example_predict_mortality()
    elif choice == '5':
        example_predict_los()
    elif choice == '6':
        example_predict_both()
    elif choice == '0':
        example_preprocessing()
        example_train_mortality()
        example_train_los()
        example_predict_both()
    else:
        print("Pilihan tidak valid!")

