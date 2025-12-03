#!/usr/bin/env python3
"""
Script untuk menghasilkan visualisasi data untuk analisis dan pembahasan
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pathlib import Path

# Set style untuk visualisasi akademik
plt.style.use('seaborn-v0_8-paper')
sns.set_palette("husl")
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 10
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'

# Buat folder untuk menyimpan gambar
output_dir = Path(__file__).parent / 'visualizations'
output_dir.mkdir(exist_ok=True)

# Load data
data_path = Path(__file__).parent.parent / 'pneumonia-prediction' / 'data' / 'data-669-patients.xlsx'
processed_path = Path(__file__).parent.parent / 'pneumonia-prediction' / 'data' / 'processed_pneumonia_data.csv'

print("Loading data...")
df_raw = pd.read_excel(data_path)
df_processed = pd.read_csv(processed_path)

# 1. Distribusi Jenis Kelamin
print("1. Membuat visualisasi distribusi jenis kelamin...")
fig, ax = plt.subplots(figsize=(8, 6))
sex_counts = df_raw['Sex'].value_counts()
colors = ['#3498db', '#e74c3c']
bars = ax.bar(sex_counts.index, sex_counts.values, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
ax.set_xlabel('Jenis Kelamin', fontsize=12, fontweight='bold')
ax.set_ylabel('Jumlah Pasien', fontsize=12, fontweight='bold')
ax.set_title('Distribusi Pasien Berdasarkan Jenis Kelamin\n(n=669)', fontsize=14, fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3, linestyle='--')

# Tambahkan nilai di atas bar
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}\n({height/len(df_raw)*100:.1f}%)',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig(output_dir / '1_distribusi_jenis_kelamin.png')
plt.close()

# 2. Distribusi Mortalitas
print("2. Membuat visualisasi distribusi mortalitas...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Pie chart
mortality_counts = df_raw['Mortality'].value_counts()
colors_pie = ['#2ecc71', '#e74c3c']
wedges, texts, autotexts = ax1.pie(mortality_counts.values, labels=mortality_counts.index, 
                                    autopct='%1.1f%%', colors=colors_pie, startangle=90,
                                    textprops={'fontsize': 11, 'fontweight': 'bold'})
ax1.set_title('Distribusi Mortalitas\n(n=669)', fontsize=14, fontweight='bold', pad=20)

# Bar chart
bars = ax2.bar(mortality_counts.index, mortality_counts.values, color=colors_pie, alpha=0.8, 
               edgecolor='black', linewidth=1.5)
ax2.set_xlabel('Mortalitas', fontsize=12, fontweight='bold')
ax2.set_ylabel('Jumlah Pasien', fontsize=12, fontweight='bold')
ax2.set_title('Distribusi Mortalitas (Bar Chart)', fontsize=14, fontweight='bold', pad=20)
ax2.grid(axis='y', alpha=0.3, linestyle='--')

for bar in bars:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}\n({height/len(df_raw)*100:.1f}%)',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig(output_dir / '2_distribusi_mortalitas.png')
plt.close()

# 3. Distribusi Length of Stay (LOS)
print("3. Membuat visualisasi distribusi LOS...")
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))

# Histogram
ax1.hist(df_raw['LOS_days'], bins=20, color='#3498db', alpha=0.7, edgecolor='black', linewidth=1)
ax1.axvline(df_raw['LOS_days'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df_raw["LOS_days"].mean():.2f}')
ax1.axvline(df_raw['LOS_days'].median(), color='green', linestyle='--', linewidth=2, label=f'Median: {df_raw["LOS_days"].median():.2f}')
ax1.set_xlabel('Length of Stay (Hari)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Frekuensi', fontsize=11, fontweight='bold')
ax1.set_title('Histogram Distribusi Length of Stay', fontsize=12, fontweight='bold')
ax1.legend()
ax1.grid(alpha=0.3, linestyle='--')

# Box plot
box = ax2.boxplot(df_raw['LOS_days'], patch_artist=True, widths=0.6)
box['boxes'][0].set_facecolor('#3498db')
box['boxes'][0].set_alpha(0.7)
ax2.set_ylabel('Length of Stay (Hari)', fontsize=11, fontweight='bold')
ax2.set_title('Box Plot Distribusi Length of Stay', fontsize=12, fontweight='bold')
ax2.grid(axis='y', alpha=0.3, linestyle='--')

# Violin plot dengan mortalitas
df_violin = df_raw.copy()
df_violin['Mortality_encoded'] = df_violin['Mortality'].map({'No': 0, 'Yes': 1})
parts = ax3.violinplot([df_violin[df_violin['Mortality_encoded']==0]['LOS_days'],
                        df_violin[df_violin['Mortality_encoded']==1]['LOS_days']],
                       positions=[1, 2], widths=0.6, showmeans=True)
for pc in parts['bodies']:
    pc.set_facecolor('#3498db')
    pc.set_alpha(0.7)
ax3.set_xticks([1, 2])
ax3.set_xticklabels(['No', 'Yes'])
ax3.set_xlabel('Mortalitas', fontsize=11, fontweight='bold')
ax3.set_ylabel('Length of Stay (Hari)', fontsize=11, fontweight='bold')
ax3.set_title('Distribusi LOS berdasarkan Mortalitas', fontsize=12, fontweight='bold')
ax3.grid(axis='y', alpha=0.3, linestyle='--')

# Q-Q plot untuk normalitas
from scipy import stats
stats.probplot(df_raw['LOS_days'], dist="norm", plot=ax4)
ax4.set_title('Q-Q Plot untuk Uji Normalitas LOS', fontsize=12, fontweight='bold')
ax4.grid(alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig(output_dir / '3_distribusi_los.png')
plt.close()

# 4. Distribusi Usia
print("4. Membuat visualisasi distribusi usia...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Histogram usia
ax1.hist(df_raw['Age'], bins=15, color='#9b59b6', alpha=0.7, edgecolor='black', linewidth=1)
ax1.axvline(df_raw['Age'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df_raw["Age"].mean():.2f}')
ax1.axvline(df_raw['Age'].median(), color='green', linestyle='--', linewidth=2, label=f'Median: {df_raw["Age"].median():.2f}')
ax1.set_xlabel('Usia (Tahun)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Frekuensi', fontsize=12, fontweight='bold')
ax1.set_title('Distribusi Usia Pasien\n(n=669)', fontsize=14, fontweight='bold', pad=20)
ax1.legend()
ax1.grid(alpha=0.3, linestyle='--')

# Box plot usia berdasarkan mortalitas
df_box = df_raw.copy()
df_box['Mortality_encoded'] = df_box['Mortality'].map({'No': 0, 'Yes': 1})
data_to_plot = [df_box[df_box['Mortality_encoded']==0]['Age'],
                df_box[df_box['Mortality_encoded']==1]['Age']]
bp = ax2.boxplot(data_to_plot, labels=['No', 'Yes'], patch_artist=True, widths=0.6)
bp['boxes'][0].set_facecolor('#2ecc71')
bp['boxes'][1].set_facecolor('#e74c3c')
for box in bp['boxes']:
    box.set_alpha(0.7)
ax2.set_xlabel('Mortalitas', fontsize=12, fontweight='bold')
ax2.set_ylabel('Usia (Tahun)', fontsize=12, fontweight='bold')
ax2.set_title('Distribusi Usia berdasarkan Mortalitas', fontsize=14, fontweight='bold', pad=20)
ax2.grid(axis='y', alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig(output_dir / '4_distribusi_usia.png')
plt.close()

# 5. Heatmap Korelasi
print("5. Membuat heatmap korelasi...")
# Pilih variabel numerik yang relevan
numeric_cols = ['Age', 'BMI', 'Heart_rate', 'Respiration_rate', 'Temperature', 
                'Systolic_BP', 'WBC', 'Hemoglobin', 'Platelet', 'Total_protein', 
                'Albumin', 'Sodium', 'BUN', 'CRP', 'CCI', 'LOS_days']
df_corr = df_raw[numeric_cols].copy()
df_corr['Mortality_encoded'] = df_raw['Mortality'].map({'No': 0, 'Yes': 1})
corr_matrix = df_corr.corr()

fig, ax = plt.subplots(figsize=(14, 12))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', cmap='coolwarm', 
            center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8},
            annot_kws={'size': 8}, ax=ax)
ax.set_title('Heatmap Korelasi Antar Variabel Numerik', fontsize=14, fontweight='bold', pad=20)
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig(output_dir / '5_heatmap_korelasi.png')
plt.close()

# 6. Distribusi Variabel Kategorikal
print("6. Membuat visualisasi variabel kategorikal...")
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
axes = axes.flatten()

categorical_vars = ['Oxygen_need', 'Shock_vital', 'LOC', 'Bedsore', 'Aspiration', 'Nursing_insurance']
for idx, var in enumerate(categorical_vars):
    counts = df_raw[var].value_counts()
    colors_cat = ['#3498db', '#e74c3c'] if len(counts) == 2 else sns.color_palette("husl", len(counts))
    bars = axes[idx].bar(counts.index, counts.values, color=colors_cat[:len(counts)], 
                         alpha=0.8, edgecolor='black', linewidth=1)
    axes[idx].set_xlabel(var.replace('_', ' ').title(), fontsize=10, fontweight='bold')
    axes[idx].set_ylabel('Jumlah Pasien', fontsize=10, fontweight='bold')
    axes[idx].set_title(f'Distribusi {var.replace("_", " ").title()}', fontsize=11, fontweight='bold')
    axes[idx].grid(axis='y', alpha=0.3, linestyle='--')
    
    for bar in bars:
        height = bar.get_height()
        axes[idx].text(bar.get_x() + bar.get_width()/2., height,
                      f'{int(height)}',
                      ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig(output_dir / '6_variabel_kategorikal.png')
plt.close()

# 7. ADL Category dan Key Person
print("7. Membuat visualisasi ADL Category dan Key Person...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# ADL Category
adl_counts = df_raw['ADL_category'].value_counts()
colors_adl = sns.color_palette("Set2", len(adl_counts))
bars1 = ax1.bar(adl_counts.index, adl_counts.values, color=colors_adl, 
                alpha=0.8, edgecolor='black', linewidth=1.5)
ax1.set_xlabel('ADL Category', fontsize=12, fontweight='bold')
ax1.set_ylabel('Jumlah Pasien', fontsize=12, fontweight='bold')
ax1.set_title('Distribusi ADL Category', fontsize=14, fontweight='bold', pad=20)
ax1.grid(axis='y', alpha=0.3, linestyle='--')
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
for bar in bars1:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}\n({height/len(df_raw)*100:.1f}%)',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

# Key Person
key_counts = df_raw['Key_person'].value_counts()
colors_key = sns.color_palette("Set3", len(key_counts))
bars2 = ax2.bar(key_counts.index, key_counts.values, color=colors_key, 
                alpha=0.8, edgecolor='black', linewidth=1.5)
ax2.set_xlabel('Key Person', fontsize=12, fontweight='bold')
ax2.set_ylabel('Jumlah Pasien', fontsize=12, fontweight='bold')
ax2.set_title('Distribusi Key Person', fontsize=14, fontweight='bold', pad=20)
ax2.grid(axis='y', alpha=0.3, linestyle='--')
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
for bar in bars2:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}\n({height/len(df_raw)*100:.1f}%)',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig(output_dir / '7_adl_key_person.png')
plt.close()

# 8. Scatter plot: Usia vs LOS dengan Mortalitas
print("8. Membuat scatter plot usia vs LOS...")
fig, ax = plt.subplots(figsize=(10, 8))
df_scatter = df_raw.copy()
df_scatter['Mortality_encoded'] = df_scatter['Mortality'].map({'No': 0, 'Yes': 1})

scatter1 = ax.scatter(df_scatter[df_scatter['Mortality_encoded']==0]['Age'],
                     df_scatter[df_scatter['Mortality_encoded']==0]['LOS_days'],
                     alpha=0.6, s=50, c='#2ecc71', label='No Mortality', edgecolors='black', linewidth=0.5)
scatter2 = ax.scatter(df_scatter[df_scatter['Mortality_encoded']==1]['Age'],
                     df_scatter[df_scatter['Mortality_encoded']==1]['LOS_days'],
                     alpha=0.6, s=50, c='#e74c3c', label='Mortality', edgecolors='black', linewidth=0.5)

ax.set_xlabel('Usia (Tahun)', fontsize=12, fontweight='bold')
ax.set_ylabel('Length of Stay (Hari)', fontsize=12, fontweight='bold')
ax.set_title('Hubungan Usia dan Length of Stay berdasarkan Mortalitas', fontsize=14, fontweight='bold', pad=20)
ax.legend(fontsize=11)
ax.grid(alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig(output_dir / '8_scatter_usia_los.png')
plt.close()

# 9. Distribusi Parameter Laboratorium
print("9. Membuat visualisasi parameter laboratorium...")
lab_vars = ['WBC', 'Hemoglobin', 'Platelet', 'Albumin', 'CRP', 'BUN']
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
axes = axes.flatten()

for idx, var in enumerate(lab_vars):
    ax = axes[idx]
    ax.hist(df_raw[var], bins=20, color='#16a085', alpha=0.7, edgecolor='black', linewidth=1)
    ax.axvline(df_raw[var].mean(), color='red', linestyle='--', linewidth=2, 
               label=f'Mean: {df_raw[var].mean():.2f}')
    ax.set_xlabel(var, fontsize=11, fontweight='bold')
    ax.set_ylabel('Frekuensi', fontsize=11, fontweight='bold')
    ax.set_title(f'Distribusi {var}', fontsize=12, fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig(output_dir / '9_parameter_laboratorium.png')
plt.close()

# 10. Perbandingan Mortalitas berdasarkan Variabel Kategorikal
print("10. Membuat visualisasi mortalitas berdasarkan variabel kategorikal...")
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
axes = axes.flatten()

cat_vars_mortality = ['Sex', 'Oxygen_need', 'Shock_vital', 'LOC', 'Bedsore', 'Aspiration']
for idx, var in enumerate(cat_vars_mortality):
    ax = axes[idx]
    crosstab = pd.crosstab(df_raw[var], df_raw['Mortality'])
    crosstab.plot(kind='bar', ax=ax, color=['#2ecc71', '#e74c3c'], alpha=0.8, 
                  edgecolor='black', linewidth=1)
    ax.set_xlabel(var.replace('_', ' ').title(), fontsize=11, fontweight='bold')
    ax.set_ylabel('Jumlah Pasien', fontsize=11, fontweight='bold')
    ax.set_title(f'Mortalitas berdasarkan {var.replace("_", " ").title()}', 
                fontsize=12, fontweight='bold')
    ax.legend(title='Mortalitas', fontsize=9)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

plt.tight_layout()
plt.savefig(output_dir / '10_mortalitas_kategorikal.png')
plt.close()

print(f"\n✓ Semua visualisasi berhasil dibuat di folder: {output_dir}")
print(f"Total file yang dibuat: {len(list(output_dir.glob('*.png')))}")

