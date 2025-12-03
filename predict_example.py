"""
Contoh Penggunaan predict.py untuk Prediksi Pneumonia
Script ini menunjukkan cara menggunakan fungsi prediksi
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from predict import predict_mortality, predict_los, predict_both
import pandas as pd


def contoh_prediksi_satu_pasien():
    """Contoh prediksi untuk satu pasien"""
    print("=" * 70)
    print("CONTOH 1: PREDIKSI UNTUK SATU PASIEN")
    print("=" * 70)
    
    # Data satu pasien
    pasien = pd.DataFrame({
        'Age': [79],
        'Sex': ['M'],
        'BMI': [18.5],
        'Heart_rate': [100],
        'Respiration_rate': [30],
        'Temperature': [36.9],
        'Systolic_BP': [120],
        'Oxygen_need': ['Yes'],
        'Shock_vital': ['Yes'],
        'WBC': [9.8],
        'Hemoglobin': [11.2],
        'Platelet': [250],
        'Total_protein': [6.7],
        'Albumin': [2.8],
        'Sodium': [138],
        'BUN': [29],
        'CRP': [15.7],
        'LOC': ['Yes'],
        'Bedsore': ['Yes'],
        'Aspiration': ['Yes'],
        'ADL_category': ['Dependent'],
        'CCI': [6],
        'Nursing_insurance': ['Yes'],
        'Key_person': ['Son']
    })
    
    # Prediksi keduanya
    hasil = predict_both(pasien)
    
    if hasil is not None:
        print("\n" + "=" * 70)
        print("HASIL PREDIKSI")
        print("=" * 70)
        print(f"Mortalitas: {'Ya' if hasil['Predicted_Mortality'].iloc[0] == 1 else 'Tidak'}")
        print(f"Probabilitas Mortalitas: {hasil['Mortality_Probability'].iloc[0]:.2%}")
        print(f"Prediksi LOS: {hasil['Predicted_LOS'].iloc[0]:.1f} hari")
    
    return hasil


def contoh_prediksi_banyak_pasien():
    """Contoh prediksi untuk banyak pasien sekaligus"""
    print("\n" + "=" * 70)
    print("CONTOH 2: PREDIKSI UNTUK BANYAK PASIEN")
    print("=" * 70)
    
    # Data beberapa pasien
    pasien_banyak = pd.DataFrame({
        'Age': [79, 76, 65, 82, 70],
        'Sex': ['M', 'F', 'M', 'F', 'M'],
        'BMI': [18.5, 19.2, 20.0, 17.8, 21.5],
        'Heart_rate': [100, 95, 90, 105, 88],
        'Respiration_rate': [30, 24, 22, 28, 20],
        'Temperature': [36.9, 37.6, 37.0, 38.2, 36.5],
        'Systolic_BP': [120, 130, 125, 115, 135],
        'Oxygen_need': ['Yes', 'No', 'Yes', 'Yes', 'No'],
        'Shock_vital': ['Yes', 'No', 'No', 'Yes', 'No'],
        'WBC': [9.8, 10.3, 8.5, 12.1, 7.9],
        'Hemoglobin': [11.2, 11.8, 12.0, 10.5, 13.2],
        'Platelet': [250, 216, 220, 180, 280],
        'Total_protein': [6.7, 6.8, 7.0, 6.5, 7.2],
        'Albumin': [2.8, 3.3, 3.0, 2.5, 3.5],
        'Sodium': [138, 137, 139, 135, 140],
        'BUN': [29, 19, 20, 35, 18],
        'CRP': [15.7, 8.6, 10.0, 18.2, 6.5],
        'LOC': ['Yes', 'No', 'No', 'Yes', 'No'],
        'Bedsore': ['Yes', 'No', 'No', 'Yes', 'No'],
        'Aspiration': ['Yes', 'No', 'No', 'Yes', 'No'],
        'ADL_category': ['Dependent', 'Independent', 'Independent', 'Dependent', 'Independent'],
        'CCI': [6, 2, 3, 7, 1],
        'Nursing_insurance': ['Yes', 'Yes', 'No', 'Yes', 'No'],
        'Key_person': ['Son', 'Daughter', 'Spouse', 'Son', 'Spouse']
    })
    
    # Prediksi
    hasil = predict_both(pasien_banyak)
    
    if hasil is not None:
        # Simpan hasil - pastikan folder ada
        import os
        results_dir = 'results'
        os.makedirs(results_dir, exist_ok=True)
        output_path = os.path.join(results_dir, 'predictions_banyak_pasien.csv')
        hasil.to_csv(output_path, index=False)
        print(f"\n✓ Hasil prediksi disimpan ke: {output_path}")
        
        # Tampilkan ringkasan
        print("\n" + "=" * 70)
        print("RINGKASAN HASIL")
        print("=" * 70)
        print(f"Total pasien: {len(hasil)}")
        print(f"Prediksi mortalitas (Ya): {sum(hasil['Predicted_Mortality'] == 1)}")
        print(f"Prediksi mortalitas (Tidak): {sum(hasil['Predicted_Mortality'] == 0)}")
        print(f"Rata-rata LOS: {hasil['Predicted_LOS'].mean():.1f} hari")
        print(f"LOS minimum: {hasil['Predicted_LOS'].min():.1f} hari")
        print(f"LOS maksimum: {hasil['Predicted_LOS'].max():.1f} hari")
    
    return hasil


def contoh_prediksi_dari_file():
    """Contoh prediksi dari file Excel atau CSV"""
    print("\n" + "=" * 70)
    print("CONTOH 3: PREDIKSI DARI FILE")
    print("=" * 70)
    
    # Jika ada file data baru, bisa langsung diprediksi
    # Contoh: hasil = predict_both('data/data_baru.xlsx')
    
    print("Untuk prediksi dari file, gunakan:")
    print("  hasil = predict_both('path/to/file.xlsx')")
    print("  atau")
    print("  hasil = predict_both('path/to/file.csv')")


def main():
    """Main function"""
    print("\n" + "=" * 70)
    print("CONTOH PENGGUNAAN PREDIKSI PNEUMONIA")
    print("=" * 70)
    
    # Contoh 1: Satu pasien
    contoh_prediksi_satu_pasien()
    
    # Contoh 2: Banyak pasien
    contoh_prediksi_banyak_pasien()
    
    # Contoh 3: Dari file
    contoh_prediksi_dari_file()
    
    print("\n" + "=" * 70)
    print("SELESAI!")
    print("=" * 70)


if __name__ == "__main__":
    main()

