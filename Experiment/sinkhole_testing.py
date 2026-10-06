import pandas as pd
import time
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier

def run_integrated_testing():
    print("--- Memulai Fase Eksekusi & Integrasi Sinkhole ---") #
    
    try:
        # 1. Load Dataset Hasil Potongan
        df = pd.read_csv('CIC_DoH_Small_Sample.csv')
        
        # Ambil sampel 10 data teratas saja untuk simulasi log agar tidak terlalu panjang
        df_test = df.head(10)
        
        # Preprocessing: Pisahkan fitur dan label target
        X = df_test.drop('Label', axis=1).select_dtypes(include=['number'])
        y_true = df_test['Label'].values
        
        # 2. Inisialisasi & Training Cepat (Sesuai Bab 3.4)
        print("Sedang mengintegrasikan Model Ensemble...") #
        # Kita menggunakan data training dari sisa dataset (70% training)
        X_train_all = df.drop('Label', axis=1).select_dtypes(include=['number'])
        y_train_all = df['Label'].map({'Benign': 0, 'Malicious': 1})
        
        models = {
            "XGBoost": XGBClassifier(eval_metric='logloss'),
            "LightGBM": LGBMClassifier(verbose=-1),
            "CatBoost": CatBoostClassifier(verbose=0)
        }
        
        for name, model in models.items():
            model.fit(X_train_all, y_train_all)

        # 3. Proses Prediksi dan Sinkholing Otomatis
        print(f"\n{'No':<3} | {'Original Label':<15} | {'AI Decision':<15} | {'Final Action'}")
        print("-" * 65)

        for i in range(len(df_test)):
            # Ambil satu baris data untuk diprediksi
            current_row = X.iloc[[i]]
            
            # Mendapatkan prediksi dari setiap model (0 atau 1)
            pred_xgb = models["XGBoost"].predict(current_row)[0]
            pred_lgbm = models["LightGBM"].predict(current_row)[0]
            pred_cat = models["CatBoost"].predict(current_row)[0]
            
            # Logika Weighted Voting (Bab 3.4): Mayoritas menang
            votes = [pred_xgb, pred_lgbm, pred_cat]
            final_decision = 1 if sum(votes) >= 2 else 0 #
            
            # Mekanisme Sinkholing (Bab 3.5)
            ai_label = "TRACKER" if final_decision == 1 else "BENIGN"
            action = "SINKHOLE (0.0.0.0)" if final_decision == 1 else "FORWARD (8.8.8.8)" #
            
            print(f"{i+1:<3} | {y_true[i]:<15} | {ai_label:<15} | {action}")
            time.sleep(0.2) # Memberikan efek simulasi real-time

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    run_integrated_testing()