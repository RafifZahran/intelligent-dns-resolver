import pandas as pd
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier # Library baru yang berhasil diinstal
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
import time

# 1. Load Dataset Hasil Potongan (Sesuai Bab 3.2)
file_input = 'CIC_DoH_Small_Sample.csv'
print(f"--- Memulai Eksekusi Model pada {file_input} ---")

try:
    df = pd.read_csv(file_input)
    
    # 2. Preprocessing: Memisahkan fitur dan label
    # Memastikan hanya kolom angka yang masuk ke model
    X = df.drop('Label', axis=1).select_dtypes(include=['number'])
    y = df['Label'].map({'Benign': 0, 'Malicious': 1})

    # Split Data: 70% Training, 30% Testing sesuai Bab 4.c.3
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # 3. List Model Ensemble Lengkap (Sesuai Bab 3.4)
    models = {
        "XGBoost": XGBClassifier(eval_metric='logloss'),
        "LightGBM": LGBMClassifier(verbose=-1),
        "CatBoost": CatBoostClassifier(verbose=0) # Sekarang sudah bisa digunakan
    }

    print(f"{'Model':<15} | {'Accuracy':<10} | {'F1-Score':<10} | {'Latency (ms)':<12}")
    print("-" * 55)

    for name, model in models.items():
        # Training proses
        model.fit(X_train, y_train)
        
        # Hitung waktu untuk Inference Latency (Bab 3.6)[cite: 2]
        start_inf = time.time()
        y_pred = model.predict(X_test)
        end_inf = time.time()
        
        # Kalkulasi metrik untuk Bab 4.1[cite: 2]
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        # Latency rata-rata per query dalam milidetik
        latency = ((end_inf - start_inf) / len(X_test)) * 1000 

        print(f"{name:<15} | {acc:<10.4f} | {f1:<10.4f} | {latency:<12.4f}")

    print("-" * 55)

except Exception as e:
    print(f"Terjadi kesalahan saat eksekusi: {e}")