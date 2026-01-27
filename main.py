import json
import os
from datetime import datetime
from tabulate import tabulate

# File untuk menyimpan data tugas
DATA_FILE = "tugas.json"

def load_tugas():
    """Memuat data tugas dari file JSON"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_tugas(tugas_list):
    """Menyimpan data tugas ke file JSON"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(tugas_list, f, ensure_ascii=False, indent=2)

def tampilkan_tugas():
    """Menampilkan semua tugas yang tersimpan"""
    tugas_list = load_tugas()
    
    if not tugas_list:
        print("\n" + "="*60)
        print("📋 DAFTAR TUGAS ANDA")
        print("="*60)
        print("❌ Tidak ada tugas. Tambahkan tugas baru!")
        print("="*60 + "\n")
        return
    
    print("\n" + "="*60)
    print("📋 DAFTAR TUGAS ANDA")
    print("="*60 + "\n")
    
    # Membuat data untuk tabel
    table_data = []
    for idx, tugas in enumerate(tugas_list, 1):
        table_data.append([
            idx,
            tugas['nama_tugas'],
            tugas['mata_pelajaran'],
            tugas['deadline']
        ])
    
    # Menampilkan tabel
    headers = ["No", "Nama Tugas", "Mata Pelajaran", "Deadline"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    print("\n" + "="*60 + "\n")

def tambah_tugas():
    """Menambahkan tugas baru"""
    print("\n" + "="*60)
    print("➕ TAMBAH TUGAS BARU")
    print("="*60)
    
    nama_tugas = input("Masukkan nama tugas: ").strip()
    if not nama_tugas:
        print("❌ Nama tugas tidak boleh kosong!")
        return
    
    mata_pelajaran = input("Masukkan mata pelajaran: ").strip()
    if not mata_pelajaran:
        print("❌ Mata pelajaran tidak boleh kosong!")
        return
    
    while True:
        deadline = input("Masukkan deadline (format: DD-MM-YYYY): ").strip()
        try:
            # Validasi format tanggal
            datetime.strptime(deadline, "%d-%m-%Y")
            break
        except ValueError:
            print("❌ Format tanggal salah! Gunakan format DD-MM-YYYY")
    
    tugas_list = load_tugas()
    tugas_baru = {
        "nama_tugas": nama_tugas,
        "mata_pelajaran": mata_pelajaran,
        "deadline": deadline
    }
    
    tugas_list.append(tugas_baru)
    save_tugas(tugas_list)
    print(f"✅ Tugas '{nama_tugas}' berhasil ditambahkan!")
    print("="*60 + "\n")

def hapus_tugas():
    """Menghapus tugas"""
    tugas_list = load_tugas()
    
    if not tugas_list:
        print("\n" + "="*60)
        print("❌ Tidak ada tugas untuk dihapus!")
        print("="*60 + "\n")
        return
    
    print("\n" + "="*60)
    print("🗑️  HAPUS TUGAS")
    print("="*60 + "\n")
    
    # Membuat data untuk tabel
    table_data = []
    for idx, tugas in enumerate(tugas_list, 1):
        table_data.append([
            idx,
            tugas['nama_tugas'],
            tugas['mata_pelajaran'],
            tugas['deadline']
        ])
    
    # Menampilkan tabel
    headers = ["No", "Nama Tugas", "Mata Pelajaran", "Deadline"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    print()
    
    while True:
        try:
            nomor = int(input("Masukkan nomor tugas yang ingin dihapus: "))
            if 1 <= nomor <= len(tugas_list):
                break
            else:
                print("❌ Nomor tidak valid!")
        except ValueError:
            print("❌ Masukkan angka yang valid!")
    
    tugas_dihapus = tugas_list.pop(nomor - 1)
    save_tugas(tugas_list)
    print(f"✅ Tugas '{tugas_dihapus['nama_tugas']}' berhasil dihapus!")
    print("="*60 + "\n")

def menu_utama():
    """Menampilkan menu utama"""
    while True:
        print("="*60)
        print("📝 APLIKASI TO-DO LIST")
        print("="*60)
        print("1. 📋 Tampilkan Semua Tugas")
        print("2. ➕ Tambah Tugas Baru")
        print("3. 🗑️  Hapus Tugas")
        print("4. ❌ Keluar")
        print("="*60)
        
        pilihan = input("Pilih menu (1-4): ").strip()
        
        if pilihan == "1":
            tampilkan_tugas()
        elif pilihan == "2":
            tambah_tugas()
        elif pilihan == "3":
            hapus_tugas()
        elif pilihan == "4":
            print("\n👋 Terima kasih telah menggunakan aplikasi To-Do List!")
            print("="*60 + "\n")
            break
        else:
            print("\n❌ Pilihan tidak valid! Silakan pilih 1-4.\n")

if __name__ == "__main__":
    menu_utama()
