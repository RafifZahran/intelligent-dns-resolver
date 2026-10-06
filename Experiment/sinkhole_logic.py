import pandas as pd
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier

# 1. Inisialisasi Model (Gunakan hasil training sebelumnya)
# Untuk simulasi, kita asumsikan model sudah dilatih
def ensemble_sinkhole_decision(prediction_results):
    """
    Logika Weighted Voting sesuai Bab 3.4
    Jika mayoritas model (2 dari 3) mendeteksi tracker, maka blokir.
    """
    votes = sum(prediction_results)
    return 1 if votes >= 2 else 0

def execute_sinkhole(domain, final_decision):
    print(f"\n[QUERY RECEIVED]: {domain}")
    if final_decision == 1:
        print(f"RESULT: MALICIOUS/TRACKER DETECTED")
        print(f"ACTION: SINKHOLED -> Response: 0.0.0.0") # Sesuai Bab 3.5
    else:
        print(f"RESULT: BENIGN")
        print(f"ACTION: FORWARDED -> Response: 8.8.8.8")

# --- SIMULASI EKSEKUSI UNTUK BAB 4.3 ---
# Contoh domain yang diuji
test_queries = [
    {"url": "google-analytics.com", "preds": [1, 1, 0]}, # XGB=1, LGBM=1, Cat=0
    {"url": "binus.ac.id", "preds": [0, 0, 0]},         # Semua anggap aman
    {"url": "doubleclick.net", "preds": [1, 1, 1]}      # Semua anggap tracker
]

for query in test_queries:
    decision = ensemble_sinkhole_decision(query['preds'])
    execute_sinkhole(query['url'], decision)