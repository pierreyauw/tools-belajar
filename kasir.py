import csv
import os
import sys
from datetime import datetime

from program import Barang, KeranjangBelanja, daftarbarang
from simpan import muat_json, muat_transaksi, simpan_json, transaksi_json

MENU = """
1. Tambah Barang
2. Lihat Barang
3. Cari, Ubah & Hapus
4. Tambah Transaksi
5. Daftar Transaksi
6. Eksport CSV
7. Keluar"""

simpanjson = simpan_json
muat = muat_json
transaksi = transaksi_json
muataja = muat_transaksi

barang_list = daftarbarang()
keranjang = KeranjangBelanja()
daftar_transaksi = []

def pilih(nomor, boleh_nol=False):
    batas_bawah = 0 if boleh_nol else 1
    while True:
        teks = input("Pilih Nomor : ")
        if teks.isdigit() and batas_bawah <= int(teks) <= nomor:
            return int(teks)
        print(f"Masukkan angka {batas_bawah} sampai {nomor}.")
        
def ambil_input(prompt, tipe_data=str):
    while True:
        teks = input(prompt).strip()
        if teks.lower() == 'batal':
            return None
        if tipe_data == str:
            if not teks:
                print("Input tidak boleh kosong.")
                continue
            return teks
        try:
            nilai = tipe_data(teks)
            if nilai < 0:
                print("Nilai tidak boleh negatif.")
                continue
            return nilai
        except ValueError:
            tipe_nama = "angka bulat" if tipe_data == int else "angka"
            print(f"Input harus berupa {tipe_nama}.")

def cetak_struk(keranjang_obj, total_awal, nominal_diskon, total_akhir, bayar):
    lebar = 50
    print("\n" + "=" * lebar)
    print("           TOKO KASIR PUNYA PIERRE          ".center(lebar))
    print("    Jl. Raya Indonesia    ".center(lebar))
    print("=" * lebar)
    print(f"ID Trans : {keranjang_obj.idtrans}")
    print(f"Tanggal  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * lebar)
    
    print(f"{'Nama Barang':<20} {'Qty':<5} {'Harga':<10} {'Subtotal':>13}")
    print("-" * lebar)
    
    for item in keranjang_obj.keranjang:
        b = item["barang"]
        qty = item["jumlah"]
        subtotal = b.harga * qty
        print(f"{b.nama[:19]:<20} {qty:<5} {b.harga:<10,.0f} {subtotal:>13,.0f}")
        
    print("-" * lebar)
    print(f"{'Total Belanja':<28} : Rp {total_awal:>15,.0f}")
    
    if nominal_diskon > 0:
        print(f"{'Diskon':<28} : Rp -{nominal_diskon:>14,.0f}")
        print(f"{'Total Akhir':<28} : Rp {total_akhir:>15,.0f}")
    
    kembalian = bayar - total_akhir
    print(f"{'Tunai / Bayar':<28} : Rp {bayar:>15,.0f}")
    print(f"{'Kembali':<28} : Rp {kembalian:>15,.0f}")
        
    print("=" * lebar)
    print("     Terima Kasih Telah Berbelanja!      ".center(lebar))
    print("=" * lebar + "\n")

def tambahbarang(tambah):
    print("\n--- Tambah Barang Baru (Ketik 'batal' kapan saja untuk keluar) ---")
    nama = ambil_input("Nama Barang : ", str)
    if nama is None:
        print("Proses dibatalkan.")
        return       
    if tambah.ada_nama(nama):
        print("Barang Sudah Ada.")
        return
    stock = ambil_input("Jumlah      : ", int)
    if stock is None:
        print("Proses dibatalkan.")
        return
    harga = ambil_input("Harga       : ", float)
    if harga is None:
        print("Proses dibatalkan.")
        return
    konfirmasi = input("\nYakin ingin menyimpan data ini? (y/n): ").strip().lower()
    if konfirmasi != 'y':
        print("Penyimpanan dibatalkan. Data tidak disimpan.")
        return
    barang = Barang(nama, stock, harga)
    tambah.tambah(barang)
    simpanjson(tambah.ke_list_dict())
    print(f"\n[SUKSES] Tersimpan: {barang.nama} | ID: {barang.idbar} | Stock: {barang.stock} | Harga: Rp {harga:,.2f}")
    
def lihat(daftar):
    data = daftar.semua()
    if not data:
        print("-------------- Belum ada Barang --------------")
        return
    print("--------------------- Daftar Barang ----------------------")
    barang_list.view(data)

def find(cari):
    kunci = input("Cari Nama Barang (ketik 'batal' untuk keluar): ").strip()
    if kunci.lower() == 'batal':
        print("Pencarian dibatalkan.")
        return

    hasil = cari.carikan(kunci)

    if not hasil:
        print("Barang Tidak Ditemukan.")
        return

    if len(hasil) == 1:
        ketemu = hasil[0]
    else:
        barang_list.view(hasil)
        print("Ketik 0 untuk kembali")
        nomor_pilihan = pilih(len(hasil), boleh_nol=True)
        if nomor_pilihan == 0:
            return
        ketemu = hasil[nomor_pilihan - 1]

    while True:
        print("\n1. Ubah")
        print("2. Hapus")
        print("3. Kembali")

        pilihan = pilih(3)

        if pilihan == 1:
            print(f"\n--- Ubah Data '{ketemu.nama}' (Ketik 'batal' untuk keluar) ---")
            nama = ambil_input("Ubah Nama  : ", str)
            if nama is None:
                print("Pengubahan barang dibatalkan.")
                return

            stock = ambil_input("Ubah Stock : ", int)
            if stock is None:
                print("Pengubahan barang dibatalkan.")
                return

            harga = ambil_input("Ubah Harga : ", float)
            if harga is None:
                print("Pengubahan barang dibatalkan.")
                return

            konfirmasi = input("\nYakin ingin mengubah data barang ini? (y/n): ").strip().lower()
            if konfirmasi != 'y':
                print("Pengubahan dibatalkan. Data tidak disimpan.")
                return

            ketemu.ubah(nama, stock, harga)
            simpanjson(barang_list.ke_list_dict())
            print("[SUKSES] Barang Berhasil Diubah.")
            return

        elif pilihan == 2:
            konfirmasi = input(f"\nYakin ingin menghapus barang '{ketemu.nama}'? (y/n): ").strip().lower()
            if konfirmasi != 'y':
                print("Penghapusan dibatalkan.")
                return

            cari.hapus(ketemu)
            simpanjson(barang_list.ke_list_dict())
            print("[SUKSES] Barang berhasil dihapus.")
            return

        else:
            return

def jualbarang(keranjang_saat_ini):
    print("\n=== TRANSAKSI PENJUALAN ===")

    while True:
        nama = ambil_input("Masukkan Nama Barang : ", str)
        if nama is None:
            print("Proses transaksi dibatalkan.")
            return keranjang_saat_ini

        hasil = barang_list.carikan(nama)
        if not hasil:
            print("Barang tidak ditemukan.")
            continue

        if len(hasil) == 1:
            ketemu = hasil[0]
        else:
            barang_list.view(hasil)
            print("Ketik 0 untuk kembali")
            nomor_pilihan = pilih(len(hasil), boleh_nol=True)
            if nomor_pilihan == 0:
                continue
            ketemu = hasil[nomor_pilihan - 1]

        jumlah = ambil_input(f"Masukkan Jumlah {ketemu.nama} (Stok: {ketemu.stock}) : ", int)
        if jumlah is None:
            print("Penambahan barang ini dibatalkan.")
            continue

        if jumlah > ketemu.stock:
            print(f"Stok tidak cukup! Stok tersedia: {ketemu.stock}")
            continue

        keranjang_saat_ini.tambah(ketemu, jumlah) 
        print(f"[SUKSES] {ketemu.nama} x{jumlah} masuk ke keranjang.")
        print(f"Subtotal: Rp {ketemu.harga * jumlah:,.2f}")

        lagi = input("\nApakah ada barang lain yang ingin dibeli? (y/n): ").strip().lower()
        if lagi != 'y':
            break

    if keranjang_saat_ini.is_empty():
        print("Keranjang kosong. Transaksi dibatalkan.")
        return keranjang_saat_ini

    total_belanja = keranjang_saat_ini.total()
    print(f"\nTotal Belanja Saat Ini: Rp {total_belanja:,.2f}")
    
    pilihan_diskon = input("Apakah ingin memasukkan diskon? (y/n): ").strip().lower()
    total_akhir = total_belanja
    nominal_diskon = 0

    if pilihan_diskon == 'y':
        diskon = ambil_input("Masukkan Diskon (%) : ", float)
        if diskon is not None:
            if 0 <= diskon <= 100:
                nominal_diskon = keranjang_saat_ini.diskon(diskon)
                total_akhir = total_belanja - nominal_diskon
                print(f"Diskon {diskon}% : -Rp {nominal_diskon:,.2f}")
            else:
                print("Diskon tidak valid")

    print(f"\nTOTAL BAYAR AKHIR: Rp {total_akhir:,.2f}")

    konfirmasi = input("\nSelesaikan transaksi dan bayar? (y/n): ").strip().lower()
    if konfirmasi == 'y':
        while True:
            teks_bayar = input("Masukkan Uang Tunai Pembayaran : Rp ").strip()
            if teks_bayar.lower() == 'batal':
                print("Pembayaran dibatalkan.")
                return KeranjangBelanja()
            
            teks_bersih = teks_bayar.replace(",", "").replace(".", "")
            
            try:
                bayar = float(teks_bersih)
                if bayar < total_akhir:
                    print(f"Uang pembayaran kurang! Minimal Rp {total_akhir:,.0f}")
                    continue
                break
            except ValueError:
                print("Input harus berupa angka.")

        keranjang_saat_ini.proses_potong_stok()
        simpanjson(barang_list.ke_list_dict())
        
        daftar_transaksi.append(keranjang_saat_ini)
        list_dict_transaksi = [t.ke_list_trans(t.total_akhir if t.total_akhir else t.total()) for t in daftar_transaksi]
        transaksi(list_dict_transaksi)
        
        cetak_struk(keranjang_saat_ini, total_belanja, nominal_diskon, total_akhir, bayar)
        
        print("[SUKSES] Transaksi selesai & data tersimpan!")
        return KeranjangBelanja()

def lihattransaksi(daftar_t):
    if not daftar_t:
        print("Belum ada transaksi.")
        return
    print("--------------------- Daftar Transaksi ----------------------")
    for riwayat in daftar_t:
        riwayat.tampilkan()

def eksport_barang_csv(daftar_barang):
    data = daftar_barang.semua()
    if not data:
        print("Tidak ada data barang untuk dieksport.")
        return
    
    lokasi = input("Masukkan path/folder simpan (tekan Enter untuk 'daftar_barang.csv'): ").strip()
    if not lokasi:
        lokasi = "daftar_barang.csv"
    elif not lokasi.endswith(".csv"):
        lokasi += ".csv"

    try:
        with open(lokasi, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ID Barang", "Nama Barang", "Stok", "Harga Satuan"])
            for item in data:
                writer.writerow([item.idbar, item.nama, item.stock, item.harga])
        print(f"[SUKSES] Daftar barang berhasil dieksport ke: {os.path.abspath(lokasi)}")
    except (OSError, csv.Error, UnicodeError) as e:
        print(f"Gagal menyimpan file: {e}")

def eksport_transaksi_csv(daftar_t):
    if not daftar_t:
        print("Tidak ada riwayat transaksi untuk dieksport.")
        return
    
    lokasi = input("Masukkan path/folder simpan (tekan Enter untuk 'riwayat_transaksi.csv'): ").strip()
    if not lokasi:
        lokasi = "riwayat_transaksi.csv"
    elif not lokasi.endswith(".csv"):
        lokasi += ".csv"

    try:
        with open(lokasi, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ID Transaksi", "Nama Barang", "Jumlah", "Harga Satuan", "Subtotal", "Total Belanja", "Diskon (%)", "Nominal Diskon", "Total Akhir"])
            for trx in daftar_t:
                for item in trx.keranjang:
                    b = item["barang"]
                    qty = item["jumlah"]
                    subtotal = b.harga * qty
                    writer.writerow([
                        trx.idtrans, 
                        b.nama, 
                        qty, 
                        b.harga, 
                        subtotal, 
                        trx.total_belanja, 
                        trx.potongan, 
                        trx.nominal_diskon, 
                        trx.total_akhir
                    ])
        print(f"[SUKSES] Riwayat transaksi berhasil dieksport ke: {os.path.abspath(lokasi)}")
    except (OSError, csv.Error) as e:
        print(f"Gagal menyimpan file: {e}")

def menu_eksport():
    print("\n=== EKSPORT CSV ===")
    print("1. Eksport Daftar Barang")
    print("2. Eksport Riwayat Transaksi")
    print("3. Kembali")
    
    pilihan = pilih(3)
    if pilihan == 1:
        eksport_barang_csv(barang_list)
    elif pilihan == 2:
        eksport_transaksi_csv(daftar_transaksi)
    else:
        return

barang_list.isijeson(muat())

data_transaksi = muataja()
if isinstance(data_transaksi, dict):
    data_transaksi = [data_transaksi]

for data in data_transaksi:
    riwayat = KeranjangBelanja()
    riwayat.untukjeson(data)
    daftar_transaksi.append(riwayat)

def main():
    global keranjang
    while True:
        print(MENU)
        pilihan = pilih(7)

        if pilihan == 1:
            tambahbarang(barang_list)
        elif pilihan == 2:
            lihat(barang_list)
        elif pilihan == 3:
            find(barang_list)
        elif pilihan == 4:
            keranjang = jualbarang(keranjang)
        elif pilihan == 5:
            lihattransaksi(daftar_transaksi)
        elif pilihan == 6:
            menu_eksport()
        elif pilihan == 7:
            print("Terima kasih telah menggunakan program ini.")
            sys.exit(0)

if __name__ == "__main__":
    main()