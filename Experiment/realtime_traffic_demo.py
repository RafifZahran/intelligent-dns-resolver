import pandas as pd
from xgboost import XGBClassifier
from scapy.all import sniff, IP, conf, get_working_ifaces # conf sudah ditambah
import sys

print("--- SISTEM MITIGASI REAL-TIME (WI-FI MODE) ---")

# 1. Load Model Cepat
try:
    df = pd.read_csv('CIC_DoH_Small_Sample.csv')
    X = df.drop('Label', axis=1).select_dtypes(include=['number'])
    y = df['Label'].map({'Benign': 0, 'Malicious': 1})
    model = XGBClassifier().fit(X, y)
    feature_names = X.columns.tolist()
except Exception as e:
    print(f"Gagal load model: {e}")
    sys.exit()

# 2. PAKSA PAKAI WI-FI (Berdasarkan list kamu, Wi-Fi ada di indeks ke-4)
try:
    ifaces = get_working_ifaces()
    # Kita kunci ke indeks 4 karena itu Intel(R) Wi-Fi 6E kamu
    conf.iface = ifaces[4].name 
    print(f"MENGGUNAKAN: {ifaces[4].description}")
except:
    print("Gagal mengunci interface Wi-Fi.")
    sys.exit()

def callback(pkt):
    if pkt.haslayer(IP):
        pkt_len = len(pkt)
        test_data = pd.DataFrame([[pkt_len] * len(feature_names)], columns=feature_names)
        
        pred = model.predict(test_data)[0]
        
        if pred == 1:
            status = "TRACKER"
            action = "SINKHOLED -> 0.0.0.0" # Simulasi pemutusan
        else:
            status = "BENIGN"
            action = "FORWARDED -> 8.8.8.8" # Simulasi diizinkan
            
        print(f"[{status}] {pkt[IP].src} -> {pkt[IP].dst} | Len: {pkt_len} | Action: {action}")

print("\n[START] Mendengarkan trafik Wi-Fi...")
print("Tekan Ctrl+C berkali-kali untuk stop.\n")

try:
    # Jalankan tanpa filter berat agar feedback cepat muncul
    sniff(iface=conf.iface, prn=callback, store=0)
except KeyboardInterrupt:
    print("\nSesi dihentikan.")
    sys.exit()