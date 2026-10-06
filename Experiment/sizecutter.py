import pandas as pd
import os

file_input = 'BCCC-CIRA-CIC-DoHBrw-2020.csv'
output_file = 'CIC_DoH_Small_Sample.csv'

print(f"--- Memulai Proses Pemotongan Dataset ---")
if not os.path.exists(file_input):
    print(f"ERROR: File {file_input} tidak ditemukan di folder ini!")
else:
    try:
        # Membaca hanya 5 baris pertama dulu untuk tes kecepatan
        print("Mengecek struktur file...")
        df_test = pd.read_csv(file_input, nrows=5)
        print(f"Kolom ditemukan: {df_test.columns.tolist()}")

        # Membaca seluruh file (ini butuh waktu karena 216MB)
        print("Membaca seluruh dataset (216MB)... Harap tunggu sebentar.")
        df = pd.read_csv(file_input)
        print(f"Total data asli: {len(df)} baris.")

        # Filter berdasarkan Label
        benign = df[df['Label'] == 'Benign']
        malicious = df[df['Label'] == 'Malicious']
        print(f"Data Benign: {len(benign)} | Data Malicious: {len(malicious)}")

        # Sampling sesuai Bab 3.2
        print("Melakukan sampling data...")
        df_small = pd.concat([
            benign.sample(n=min(len(benign), 20000), random_state=42),
            malicious.sample(n=min(len(malicious), 15000), random_state=42)
        ])

        # Simpan file
        df_small.to_csv(output_file, index=False)
        print(f"BERHASIL! File kecil disimpan: {output_file}")
        print(f"Ukuran file baru: {os.path.getsize(output_file) / 1024 / 1024:.2f} MB")

    except Exception as e:
        print(f"TERJADI KESALAHAN: {str(e)}")

print("--- Proses Selesai ---")