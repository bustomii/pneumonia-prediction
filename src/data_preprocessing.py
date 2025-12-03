"""
Data Preprocessing untuk Dataset Pneumonia
Mempersiapkan data untuk model machine learning
"""

import pandas as pd
import numpy as np
from pathlib import Path


class DataPreprocessor:
    """Class untuk preprocessing data pneumonia"""
    
    def __init__(self, data_path):
        """
        Initialize DataPreprocessor
        
        Parameters:
        -----------
        data_path : str
            Path ke file dataset
        """
        self.data_path = data_path
        self.df = None
        
    def load_data(self):
        """Load data dari file Excel atau CSV"""
        try:
            if self.data_path.endswith('.xlsx') or self.data_path.endswith('.xls'):
                self.df = pd.read_excel(self.data_path)
            elif self.data_path.endswith('.csv'):
                self.df = pd.read_csv(self.data_path)
            else:
                raise ValueError("Format file tidak didukung. Gunakan .xlsx, .xls, atau .csv")
            
            print(f"Data berhasil dimuat: {self.df.shape[0]} baris, {self.df.shape[1]} kolom")
            return self.df
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            return None
    
    def explore_data(self):
        """Eksplorasi data dasar"""
        if self.df is None:
            print("Data belum dimuat. Jalankan load_data() terlebih dahulu.")
            return
        
        print("=" * 50)
        print("INFORMASI DATASET")
        print("=" * 50)
        print(f"\nShape: {self.df.shape}")
        print(f"\nKolom: {list(self.df.columns)}")
        print(f"\nInfo Data:")
        print(self.df.info())
        print(f"\nStatistik Deskriptif:")
        print(self.df.describe())
        print(f"\nMissing Values:")
        print(self.df.isnull().sum())
        print(f"\nDuplikat: {self.df.duplicated().sum()}")
        
    def handle_missing_values(self, strategy='mean'):
        """
        Menangani missing values
        
        Parameters:
        -----------
        strategy : str
            'mean', 'median', 'mode', atau 'drop'
        """
        if self.df is None:
            print("Data belum dimuat.")
            return
        
        missing_count = self.df.isnull().sum()
        if missing_count.sum() == 0:
            print("Tidak ada missing values.")
            return
        
        print(f"Missing values sebelum handling: {missing_count.sum()}")
        
        for col in self.df.columns:
            if self.df[col].isnull().sum() > 0:
                if strategy == 'mean' and self.df[col].dtype in ['int64', 'float64']:
                    self.df[col].fillna(self.df[col].mean(), inplace=True)
                elif strategy == 'median' and self.df[col].dtype in ['int64', 'float64']:
                    self.df[col].fillna(self.df[col].median(), inplace=True)
                elif strategy == 'mode':
                    self.df[col].fillna(self.df[col].mode()[0], inplace=True)
                elif strategy == 'drop':
                    self.df.dropna(subset=[col], inplace=True)
        
        print(f"Missing values setelah handling: {self.df.isnull().sum().sum()}")
    
    def encode_categorical(self):
        """Encode variabel kategorikal menjadi numerik"""
        if self.df is None:
            print("Data belum dimuat.")
            return
        
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        
        if len(categorical_cols) == 0:
            print("Tidak ada kolom kategorikal yang perlu di-encode.")
            return
        
        print(f"Kolom kategorikal yang akan di-encode: {list(categorical_cols)}")
        
        # Label encoding untuk kolom binary
        from sklearn.preprocessing import LabelEncoder
        le = LabelEncoder()
        
        for col in categorical_cols:
            if self.df[col].nunique() == 2:  # Binary
                self.df[col] = le.fit_transform(self.df[col])
                print(f"{col}: Binary encoding")
            else:  # Multi-class, gunakan one-hot encoding
                self.df = pd.get_dummies(self.df, columns=[col], prefix=col)
                print(f"{col}: One-hot encoding")
    
    def prepare_mortality_data(self, target_col='mortality'):
        """
        Siapkan data untuk prediksi mortalitas (klasifikasi)
        
        Parameters:
        -----------
        target_col : str
            Nama kolom target untuk mortalitas
        """
        if self.df is None:
            print("Data belum dimuat.")
            return None
        
        if target_col not in self.df.columns:
            print(f"Kolom '{target_col}' tidak ditemukan.")
            print(f"Kolom yang tersedia: {list(self.df.columns)}")
            return None
        
        # Pastikan target adalah binary (Yes/No atau 1/0)
        if self.df[target_col].dtype == 'object':
            self.df[target_col] = self.df[target_col].map({'Yes': 1, 'No': 0, 'Y': 1, 'N': 0})
        
        print(f"Data mortalitas siap: {self.df.shape[0]} sampel")
        print(f"Distribusi target: {self.df[target_col].value_counts().to_dict()}")
        
        return self.df
    
    def prepare_los_data(self, target_col='LOS'):
        """
        Siapkan data untuk prediksi Length of Stay (regresi)
        
        Parameters:
        -----------
        target_col : str
            Nama kolom target untuk LOS
        """
        if self.df is None:
            print("Data belum dimuat.")
            return None
        
        if target_col not in self.df.columns:
            print(f"Kolom '{target_col}' tidak ditemukan.")
            print(f"Kolom yang tersedia: {list(self.df.columns)}")
            return None
        
        # Pastikan target adalah numerik
        self.df[target_col] = pd.to_numeric(self.df[target_col], errors='coerce')
        
        print(f"Data LOS siap: {self.df.shape[0]} sampel")
        print(f"Statistik LOS: Min={self.df[target_col].min()}, Max={self.df[target_col].max()}, Mean={self.df[target_col].mean():.2f}")
        
        return self.df
    
    def save_processed_data(self, output_path):
        """Simpan data yang sudah diproses"""
        if self.df is None:
            print("Data belum dimuat.")
            return
        
        if output_path.endswith('.csv'):
            self.df.to_csv(output_path, index=False)
        elif output_path.endswith('.xlsx'):
            self.df.to_excel(output_path, index=False)
        else:
            self.df.to_csv(output_path + '.csv', index=False)
        
        print(f"Data berhasil disimpan ke: {output_path}")


if __name__ == "__main__":
    # Contoh penggunaan
    print("Data Preprocessing untuk Dataset Pneumonia")
    print("=" * 50)
    
    # Ganti dengan path dataset Anda
    data_path = "../data/pneumonia_dataset.xlsx"
    
    preprocessor = DataPreprocessor(data_path)
    df = preprocessor.load_data()
    
    if df is not None:
        preprocessor.explore_data()
        preprocessor.handle_missing_values(strategy='mean')
        preprocessor.encode_categorical()

