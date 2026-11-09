import json
import os

FOLDER_KASIR = os.path.dirname(os.path.abspath(__file__))

def lokasi_file(nama_file):
    return os.path.join(FOLDER_KASIR, nama_file)

def simpan_json(data, nama_file="barang.json"):
    nama_file = lokasi_file(nama_file)
    sementara = nama_file + ".tmp"
    with open(sementara, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    os.replace(sementara, nama_file)

def muat_json(nama_file="barang.json"):
    nama_file = lokasi_file(nama_file)
    try:
        with open(nama_file, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        cadangan_file = nama_file + ".rusak"
        os.replace(nama_file, cadangan_file)
        print(f"{nama_file} rusak. Disimpan sebagai {cadangan_file}, memulai dari data kosong.")
        return []
    
def transaksi_json(data, nama_file="trans.json"):
    nama_file = lokasi_file(nama_file)
    sementara = nama_file + ".tmp"
    with open(sementara, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    os.replace(sementara, nama_file)

def muat_transaksi(nama_file="trans.json"):
    nama_file = lokasi_file(nama_file)
    try:
        with open(nama_file, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        cadangan_file = nama_file + ".rusak"
        os.replace(nama_file, cadangan_file)
        print(f"{nama_file} rusak. Disimpan sebagai {cadangan_file}, memulai dari data kosong.")
        return []