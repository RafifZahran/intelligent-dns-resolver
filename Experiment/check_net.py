from scapy.all import get_if_list, conf

print("--- Daftar Kartu Jaringan yang Terdeteksi ---")
interfaces = get_if_list()
for i, iface in enumerate(interfaces):
    print(f"{i}. {iface}")

print(f"\nInterface Default yang digunakan Scapy: {conf.iface}")
print("\nJika daftar di atas kosong, berarti Npcap belum terinstall dengan benar.")