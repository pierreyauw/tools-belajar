def periksa_angka(angka2, label, tipe=(int, float), minimal=0, maksimal=None):
    if isinstance(angka2, bool) or not isinstance(angka2, tipe):
        raise TypeError(f"{label} harus berupa angka")
    if angka2 < minimal:
        raise ValueError(f"{label} tidak boleh kurang dari {minimal}")
    if maksimal is not None and angka2 > maksimal:
        raise ValueError(f"{label} tidak boleh lebih dari {maksimal}")
    return angka2

def periksa_teks(teks1, label):
    if not isinstance(teks1, str):
        raise TypeError(f"{label} harus berupa teks")
    teks1 = teks1.strip()
    if not teks1:
        raise ValueError(f"{label} tidak boleh kosong")
    return teks1
 
class Barang:
    idbarang = 1

    def __init__(self, nama, stock, harga):
        self.nama = periksa_teks(nama, "Nama")
        self.stock = periksa_angka(stock, "Stock", tipe=int, minimal=0)
        self.harga = periksa_angka(harga, "Harga", minimal=0)
        self.subtotal = self.hitung_subtotal()
        self.idbar = Barang.idbarang
        Barang.idbarang += 1
    
    def hitung_subtotal(self):
        return self.stock * self.harga
        
    def ke_dict(self):
        return {
            "nama": self.nama,
            "id": self.idbar,
            "stock": self.stock,
            "harga": self.harga,
        }
    
    def ubah(self, nama, stock, harga):
        namabaru = periksa_teks(nama, "Nama")
        stockbaru = periksa_angka(stock, "Stock", tipe=int, minimal=0)
        hargabaru = periksa_angka(harga, "Harga", minimal=0)
        self.nama = namabaru
        self.stock = stockbaru
        self.harga = hargabaru
        self.subtotal = self.hitung_subtotal()
        
class daftarbarang:
    def __init__(self):
        self.barang = []
    
    def tambah(self, tambah):
        if not isinstance(tambah, Barang):
            raise TypeError("Hanya objek Barang yang dapat ditambahkan")
        self.barang.append(tambah)
    
    def semua(self):
        return self.barang
    
    def carikan(self, kunci):
        if not isinstance(kunci, str):
            raise TypeError("Keyword harus berupa teks")
        cari = kunci.lower().split()
        if not cari:
            return []
        hasil = []
        for caribar in self.barang:
            gabungan = str(caribar.idbar) + " " + caribar.nama.lower()
            if all(cocok in gabungan for cocok in cari):
                hasil.append(caribar)
        return hasil
    
    def ke_list_dict(self):
        return [{"nama": barang.nama, "id": barang.idbar, "stock": barang.stock, "harga": barang.harga} for barang in self.barang]
    
    def ada_nama(self, nama):
        nama = nama.strip().lower()
        return any(barang.nama.lower() == nama for barang in self.barang)
    
    def hapus(self, hapus):
        if hapus in self.barang:
            self.barang.remove(hapus)
    
    def view(self, data):
        print(f"{'No':>4} {'Nama':<20} {'ID':>6} {'Qty':>6} {'Harga':>12}")
        print("-" * 52)
        for i, item in enumerate(data, start=1):
            print(f"{i:>4} {item.nama:<20} {item.idbar:>6} {item.stock:>6} {item.harga:>12,.0f}")
    
    def isijeson(self, data):
        for item in data:
            self.tambah(Barang(item["nama"], item["stock"], item["harga"]))

class KeranjangBelanja:
    id = 1
    def __init__(self):
        self.keranjang = []
        self.idtrans = f"TRX-{KeranjangBelanja.id}"
        KeranjangBelanja.id += 1
        
        self.potongan = 0
        self.nominal_diskon = 0
        self.total_belanja = 0
        self.total_akhir = 0

    def is_empty(self):
        return len(self.keranjang) == 0

    def tambah(self, barang_obj, jumlah):
        self.keranjang.append({"barang": barang_obj, "jumlah": jumlah})

    def total(self):
        total = 0
        for item in self.keranjang:
            total += item["barang"].harga * item["jumlah"]
        return total

    def diskon(self, potongan):
        self.potongan = potongan
        self.total_belanja = self.total()
        self.nominal_diskon = self.total_belanja * (potongan / 100)
        self.total_akhir = self.total_belanja - self.nominal_diskon
        return self.nominal_diskon

    def proses_potong_stok(self):
        for item in self.keranjang:
            item["barang"].stock -= item["jumlah"]
            item["barang"].subtotal = item["barang"].hitung_subtotal()

    def ke_list_trans(self, total_akhir_custom=None):
        self.total_belanja = self.total()
        if total_akhir_custom is not None:
            self.total_akhir = total_akhir_custom
            self.nominal_diskon = self.total_belanja - self.total_akhir
        else:
            self.nominal_diskon = self.diskon(self.potongan)
        
        return {
            "idtrans": self.idtrans,
            "barang": [
                {
                    "nama": item["barang"].nama,
                    "jumlah": item["jumlah"],
                    "harga": item["barang"].harga
                }
                for item in self.keranjang
            ],
            "diskon": self.potongan,
            "nominal_diskon": self.nominal_diskon,
            "total_belanja": self.total_belanja,
            "total_akhir": self.total_akhir
        }

    def tampilkan(self):
        print(f"\nID Transaksi: {self.idtrans}")
        print(f"{'No':>4} {'Nama':<20} {'Qty':>6} {'Harga':>12} {'Subtotal':>14}")
        print("-" * 60)

        for i, item in enumerate(self.keranjang, start=1):
            b = item["barang"]
            qty = item["jumlah"]
            subtotal = b.harga * qty
            print(f"{i:>4} {b.nama:<20} {qty:>6} {b.harga:>12,.0f} {subtotal:>14,.0f}")

        print("-" * 60)
        print(f"{'Total Belanja':<30} Rp{self.total_belanja:>15,.0f}")
        print(f"{'Diskon':<30} {self.potongan:>14}%")
        print(f"{'Nominal Diskon':<30} Rp{self.nominal_diskon:>15,.0f}")
        print(f"{'Total Setelah Diskon':<30} Rp{self.total_akhir:>15,.0f}")

    def untukjeson(self, data):
        self.idtrans = data.get("idtrans", self.idtrans)
        self.potongan = data.get("diskon", 0)
        self.nominal_diskon = data.get("nominal_diskon", 0)
        self.total_belanja = data.get("total_belanja", 0)
        self.total_akhir = data.get("total_akhir", 0)
                        
        self.keranjang = []
        for item in data.get("barang", []):
            b_temp = Barang(item["nama"], 0, item["harga"])
            self.keranjang.append({"barang": b_temp, "jumlah": item["jumlah"]})