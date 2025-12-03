"""
Main Script untuk Project Prediksi Pneumonia
Menggabungkan semua proses: preprocessing, training, dan prediksi
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from data_preprocessing import DataPreprocessor
from train_mortality import train_mortality_model, train_extra_tree_model
from train_los import train_los_model, train_extra_tree_regressor
from predict import predict_both
import pandas as pd


def main():
    """Main function untuk menjalankan seluruh pipeline"""
    
    print("=" * 70)
    print("PROJECT PREDIKSI MORTALITAS DAN RAWAT INAP PASIEN PNEUMONIA")
    print("Menggunakan Algoritma Machine Learning dengan Low Code PyCaret")
    print("=" * 70)
    
    # Konfigurasi
    RAW_DATA_PATH = "data/pneumonia_dataset.xlsx"  # Ganti dengan path dataset Anda
    PROCESSED_DATA_PATH = "data/processed_pneumonia_data.csv"
    
    # Step 1: Data Preprocessing
    print("\n" + "=" * 70)
    print("STEP 1: DATA PREPROCESSING")
    print("=" * 70)
    
    preprocessor = DataPreprocessor(RAW_DATA_PATH)
    df = preprocessor.load_data()
    
    if df is None:
        print("Error: Gagal memuat data. Pastikan file dataset ada di path yang benar.")
        return
    
    # Eksplorasi data
    preprocessor.explore_data()
    
    # Handle missing values
    preprocessor.handle_missing_values(strategy='mean')
    
    # Encode categorical
    preprocessor.encode_categorical()
    
    # Simpan data yang sudah diproses
    preprocessor.save_processed_data(PROCESSED_DATA_PATH)
    
    # Step 2: Training Model Mortalitas
    print("\n" + "=" * 70)
    print("STEP 2: TRAINING MODEL PREDIKSI MORTALITAS")
    print("=" * 70)
    
    try:
        # Train LightGBM untuk mortalitas
        mortality_model, mortality_pred = train_mortality_model(
            data_path=PROCESSED_DATA_PATH,
            target_col='mortality',  # Ganti dengan nama kolom target yang sesuai
            test_size=0.2
        )
        
        # Train Extra Tree untuk mortalitas
        et_mortality_model = train_extra_tree_model(
            data_path=PROCESSED_DATA_PATH,
            target_col='mortality',
            test_size=0.2
        )
        
        print("\n✓ Model mortalitas berhasil ditraining!")
    except Exception as e:
        print(f"\n✗ Error training model mortalitas: {str(e)}")
        print("Pastikan kolom 'mortality' ada di dataset")
    
    # Step 3: Training Model LOS
    print("\n" + "=" * 70)
    print("STEP 3: TRAINING MODEL PREDIKSI LENGTH OF STAY (LOS)")
    print("=" * 70)
    
    try:
        # Train LightGBM untuk LOS
        los_model, los_pred = train_los_model(
            data_path=PROCESSED_DATA_PATH,
            target_col='LOS',  # Ganti dengan nama kolom target yang sesuai
            test_size=0.2
        )
        
        # Train Extra Tree Regressor untuk LOS
        et_los_model = train_extra_tree_regressor(
            data_path=PROCESSED_DATA_PATH,
            target_col='LOS',
            test_size=0.2
        )
        
        print("\n✓ Model LOS berhasil ditraining!")
    except Exception as e:
        print(f"\n✗ Error training model LOS: {str(e)}")
        print("Pastikan kolom 'LOS' ada di dataset")
    
    # Step 4: Prediksi (contoh)
    print("\n" + "=" * 70)
    print("STEP 4: CONTOH PREDIKSI")
    print("=" * 70)
    
    # Buat data contoh untuk prediksi
    # Ganti dengan data aktual yang ingin diprediksi
    sample_data = pd.DataFrame({
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
        results = predict_both(
            new_data=sample_data,
            mortality_model='models/mortality_model',
            los_model='models/los_model'
        )
        
        if results is not None:
            output_path = 'results/predictions.csv'
            results.to_csv(output_path, index=False)
            print(f"\n✓ Hasil prediksi disimpan ke: {output_path}")
    except Exception as e:
        print(f"\n✗ Error melakukan prediksi: {str(e)}")
        print("Pastikan model sudah ditraining terlebih dahulu")
    
    print("\n" + "=" * 70)
    print("SELESAI!")
    print("=" * 70)
    print("\nModel yang sudah ditraining tersimpan di folder 'models/'")
    print("Hasil prediksi tersimpan di folder 'results/'")
    print("\nUntuk melakukan prediksi pada data baru, gunakan script predict.py")


if __name__ == "__main__":
    main()

