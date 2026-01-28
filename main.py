import json
import os
from datetime import datetime, timedelta
from tabulate import tabulate

# File untuk menyimpan data tugas
DATA_FILE = "tugas.json"

# Konstanta untuk pemberitahuan
HARI_PERINGATAN = 7  # Peringatan jika deadline dalam 7 hari ke depan
HARI_URGENT = 3      # Status urgent jika deadline dalam 3 hari ke depan

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

def hitung_sisa_hari(deadline_str):
    """Menghitung sisa hari sampai deadline"""
    try:
        deadline_date = datetime.strptime(deadline_str, "%d-%m-%Y")
        hari_ini = datetime.now()
        selisih = (deadline_date - hari_ini).days
        return selisih
    except ValueError:
        return None

def get_status_deadline(sisa_hari):
    """Mendapatkan status dan simbol deadline"""
    if sisa_hari is None:
        return "❌ Format Salah", "red"
    elif sisa_hari < 0:
        return "⛔ TERLEWAT", "red"
    elif sisa_hari == 0:
        return "🔴 HARI INI", "red"
    elif sisa_hari <= HARI_URGENT:
        return f"🟠 URGENT ({sisa_hari} hari)", "orange"
    elif sisa_hari <= HARI_PERINGATAN:
        return f"🟡 PERHATIAN ({sisa_hari} hari)", "yellow"
    else:
        return f"🟢 OK ({sisa_hari} hari)", "green"

def buat_progress_bar(sisa_hari, max_hari=HARI_PERINGATAN):
    """Membuat progress bar countdown untuk deadline"""
    if sisa_hari < 0:
        return "█" * 20 + " 0% [TERLEWAT]"
    
    persen = max(0, min(100, int((sisa_hari / max_hari) * 100))) if max_hari > 0 else 0
    bar_length = 10
    filled = int(bar_length * persen / 100)
    empty = bar_length - filled
    
    bar = "█" * filled + "░" * empty
    return f"{bar} {persen}%"

def tampilkan_countdown_detail(tugas_list):
    """Menampilkan countdown detail untuk setiap tugas"""
    tugas_mendesak = []
    
    for tugas in tugas_list:
        sisa_hari = hitung_sisa_hari(tugas['deadline'])
        if sisa_hari is not None and 0 <= sisa_hari <= HARI_PERINGATAN:
            tugas_mendesak.append({
                'nama': tugas['nama_tugas'],
                'mata_pelajaran': tugas['mata_pelajaran'],
                'deadline': tugas['deadline'],
                'sisa_hari': sisa_hari
            })
    
    if tugas_mendesak:
        tugas_mendesak.sort(key=lambda x: x['sisa_hari'])
        print("\n" + "="*60)
        print("⏰ COUNTDOWN DEADLINE")
        print("="*60)
        
        for item in tugas_mendesak:
            progress = buat_progress_bar(item['sisa_hari'])
            
            # Tentukan emoji berdasarkan sisa hari
            if item['sisa_hari'] == 0:
                emoji = "🔴"
                durasi = "HARI INI!"
            elif item['sisa_hari'] == 1:
                emoji = "🟠"
                durasi = f"{item['sisa_hari']} HARI LAGI"
            elif item['sisa_hari'] <= HARI_URGENT:
                emoji = "🟠"
                durasi = f"{item['sisa_hari']} HARI LAGI"
            else:
                emoji = "🟡"
                durasi = f"{item['sisa_hari']} HARI LAGI"
            
            print(f"\n{emoji} {item['nama']}")
            print(f"   Mata Pelajaran: {item['mata_pelajaran']}")
            print(f"   Deadline: {item['deadline']}")
            print(f"   Countdown: {durasi}")
            print(f"   Progress: {progress}")
        
        print("\n" + "="*60 + "\n")

def cek_deadline_hampir_tiba():
    """Mengecek dan menampilkan notifikasi deadline yang hampir tiba"""
    tugas_list = load_tugas()
    deadline_urgent = []
    
    for tugas in tugas_list:
        sisa_hari = hitung_sisa_hari(tugas['deadline'])
        if sisa_hari is not None and 0 <= sisa_hari <= HARI_PERINGATAN:
            deadline_urgent.append({
                'nama': tugas['nama_tugas'],
                'sisa_hari': sisa_hari,
                'deadline': tugas['deadline']
            })
    
    if deadline_urgent:
        print("\n" + "="*60)
        print("⚠️  PEMBERITAHUAN: DEADLINE HAMPIR TIBA!")
        print("="*60)
        for item in sorted(deadline_urgent, key=lambda x: x['sisa_hari']):
            if item['sisa_hari'] == 0:
                print(f"🔴 {item['nama']} - DEADLINE HARI INI! ({item['deadline']})")
            elif item['sisa_hari'] <= HARI_URGENT:
                print(f"🟠 {item['nama']} - {item['sisa_hari']} hari lagi ({item['deadline']})")
            else:
                print(f"🟡 {item['nama']} - {item['sisa_hari']} hari lagi ({item['deadline']})")
        print("="*60 + "\n")
    
    # Tampilkan countdown detail
    tampilkan_countdown_detail(tugas_list)

def tampilkan_tugas():
    """Menampilkan semua tugas yang tersimpan dengan status deadline"""
    tugas_list = load_tugas()
    
    # Cek dan tampilkan notifikasi deadline hampir tiba
    cek_deadline_hampir_tiba()
    
    if not tugas_list:
        print("\n" + "="*60)
        print("📋 DAFTAR TUGAS ANDA")
        print("="*60)
        print("❌ Tidak ada tugas. Tambahkan tugas baru!")
        print("="*60 + "\n")
        return
    
    print("\n" + "="*60)
    print("📋 DAFTAR TUGAS ANDA (Terupdate)")
    print("="*60 + "\n")
    
    # Membuat data untuk tabel dengan status deadline
    table_data = []
    for idx, tugas in enumerate(tugas_list, 1):
        sisa_hari = hitung_sisa_hari(tugas['deadline'])
        status, _ = get_status_deadline(sisa_hari)
        table_data.append([
            idx,
            tugas['nama_tugas'],
            tugas['mata_pelajaran'],
            tugas['deadline'],
            status
        ])
    
    # Menampilkan tabel
    headers = ["No", "Nama Tugas", "Mata Pelajaran", "Deadline", "Status"]
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
    
    # Membuat data untuk tabel dengan status deadline
    table_data = []
    for idx, tugas in enumerate(tugas_list, 1):
        sisa_hari = hitung_sisa_hari(tugas['deadline'])
        status, _ = get_status_deadline(sisa_hari)
        table_data.append([
            idx,
            tugas['nama_tugas'],
            tugas['mata_pelajaran'],
            tugas['deadline'],
            status
        ])
    
    # Menampilkan tabel
    headers = ["No", "Nama Tugas", "Mata Pelajaran", "Deadline", "Status"]
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

def lihat_countdown():
    """Menampilkan countdown detail untuk semua deadline"""
    tugas_list = load_tugas()
    
    if not tugas_list:
        print("\n" + "="*60)
        print("❌ Tidak ada tugas!")
        print("="*60 + "\n")
        return
    
    tampilkan_countdown_detail(tugas_list)

def lihat_deadline_mendesak():
    """Menampilkan tugas dengan deadline yang mendesak"""
    tugas_list = load_tugas()
    
    if not tugas_list:
        print("\n" + "="*60)
        print("❌ Tidak ada tugas!")
        print("="*60 + "\n")
        return
    
    print("\n" + "="*60)
    print("⚠️  TUGAS DENGAN DEADLINE MENDESAK")
    print("="*60 + "\n")
    
    # Filter tugas dengan deadline mendesak
    tugas_mendesak = []
    for tugas in tugas_list:
        sisa_hari = hitung_sisa_hari(tugas['deadline'])
        if sisa_hari is not None and sisa_hari <= HARI_PERINGATAN:
            tugas_mendesak.append({
                'nama_tugas': tugas['nama_tugas'],
                'mata_pelajaran': tugas['mata_pelajaran'],
                'deadline': tugas['deadline'],
                'sisa_hari': sisa_hari,
                'status': get_status_deadline(sisa_hari)[0]
            })
    
    if not tugas_mendesak:
        print("✅ Tidak ada deadline yang mendesak! Semua tugas masih OK.")
        print("="*60 + "\n")
        return
    
    # Urutkan berdasarkan sisa hari (terdekat dulu)
    tugas_mendesak.sort(key=lambda x: x['sisa_hari'])
    
    # Membuat tabel
    table_data = []
    for idx, tugas in enumerate(tugas_mendesak, 1):
        countdown = f"{tugas['sisa_hari']} hari" if tugas['sisa_hari'] > 0 else "Hari ini"
        table_data.append([
            idx,
            tugas['nama_tugas'],
            tugas['mata_pelajaran'],
            tugas['deadline'],
            countdown,
            tugas['status']
        ])
    
    headers = ["No", "Nama Tugas", "Mata Pelajaran", "Deadline", "Countdown", "Status"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    # Tampilkan countdown detail untuk tugas-tugas mendesak
    print("\n" + "="*60)
    print("⏰ DETAIL COUNTDOWN")
    print("="*60)
    
    for tugas in tugas_mendesak:
        progress = buat_progress_bar(tugas['sisa_hari'])
        
        if tugas['sisa_hari'] == 0:
            emoji = "🔴"
            durasi = "HARI INI!"
        elif tugas['sisa_hari'] == 1:
            emoji = "🟠"
            durasi = f"{tugas['sisa_hari']} HARI LAGI"
        elif tugas['sisa_hari'] <= HARI_URGENT:
            emoji = "🟠"
            durasi = f"{tugas['sisa_hari']} HARI LAGI"
        else:
            emoji = "🟡"
            durasi = f"{tugas['sisa_hari']} HARI LAGI"
        
        print(f"\n{emoji} {tugas['nama_tugas']}")
        print(f"   Progress: {progress}")
        print(f"   Sisa Waktu: {durasi}")
    
    print("\n" + "="*60 + "\n")

def menu_utama():
    """Menampilkan menu utama"""
    while True:
        print("="*60)
        print("📝 APLIKASI TO-DO LIST")
        print("="*60)
        print("1. 📋 Tampilkan Semua Tugas")
        print("2. ➕ Tambah Tugas Baru")
        print("3. 🗑️  Hapus Tugas")
        print("4. ⏰ Lihat Countdown Deadline")
        print("5. ⚠️  Lihat Deadline Mendesak")
        print("6. ❌ Keluar")
        print("="*60)
        
        pilihan = input("Pilih menu (1-6): ").strip()
        
        if pilihan == "1":
            tampilkan_tugas()
        elif pilihan == "2":
            tambah_tugas()
        elif pilihan == "3":
            hapus_tugas()
        elif pilihan == "4":
            lihat_countdown()
        elif pilihan == "5":
            lihat_deadline_mendesak()
        elif pilihan == "6":
            print("\n👋 Terima kasih telah menggunakan aplikasi To-Do List!")
            print("="*60 + "\n")
            break
        else:
            print("\n❌ Pilihan tidak valid! Silakan pilih 1-6.\n")

if __name__ == "__main__":
    menu_utama()
