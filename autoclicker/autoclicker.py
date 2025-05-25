import pyautogui #butuh instal package ini
import time
import threading
import json
import os
import keyboard  # butuh install package ini, harus run sbg admin

click_interval = 1.0 #ubah sesuai kebutuhan
positions = []
running = False
max_loops = 0

def click_loop():
    global running
    loop_count = 0
    print("Tekan F8 kapan saja untuk menghentikan autoclicker.")
    while running:
        for pos in positions:
            if not running:
                break
            if keyboard.is_pressed('f8'):
                running = False
                print("F8 ditekan. Autoclicker dihentikan.")
                break
            x, y = pos
            pyautogui.click(x, y)
            print(f"Klik di ({x}, {y})")
            time.sleep(click_interval)

        loop_count += 1
        if max_loops > 0 and loop_count >= max_loops:
            print(f"Selesai {loop_count} perulangan.")
            running = False
            break

def start_clicker():
    global running
    if not positions:
        print("Daftar posisi kosong. Tambahkan posisi dulu!")
        return
    if max_loops == 0:
        confirm = input("Jumlah perulangan tidak diatur (akan berjalan terus). Lanjutkan? (y/n): ")
        if confirm.lower() != 'y':
            print("Dibatalkan.")
            return
    if not running:
        running = True
        thread = threading.Thread(target=click_loop)
        thread.start()
        print("Autoclicker dimulai...")

def stop_clicker():
    global running
    running = False
    print("Autoclicker dihentikan.")

def add_click_position():
    print("Arahkan kursor ke lokasi yang ingin ditambahkan dan tunggu 5 detik...")
    time.sleep(5)
    x, y = pyautogui.position()
    positions.append((x, y))
    print(f"Posisi ({x}, {y}) ditambahkan.")

def list_positions():
    if positions:
        print("Daftar posisi klik:")
        for i, (x, y) in enumerate(positions):
            print(f"{i+1}. ({x}, {y})")
    else:
        print("Belum ada posisi yang ditambahkan.")

def clear_positions():
    positions.clear()
    print("Semua posisi telah dihapus.")

def set_max_loops():
    global max_loops
    try:
        loops = int(input("Masukkan jumlah perulangan (0 untuk tak terbatas): "))
        if loops < 0:
            print("Jumlah perulangan tidak boleh negatif.")
        else:
            max_loops = loops
            if loops == 0:
                print("Klik akan berjalan terus tanpa henti.")
            else:
                print(f"Klik akan diulang sebanyak {loops} kali.")
    except ValueError:
        print("Input tidak valid.")

def save_positions_to_file(filename="positions.json"):
    with open(filename, "w") as f:
        json.dump(positions, f)
    print(f"Posisi klik disimpan ke '{filename}'.")

def load_positions_from_file(filename="positions.json"):
    global positions
    if os.path.exists(filename):
        with open(filename, "r") as f:
            positions = json.load(f)
        print(f"Posisi klik dimuat dari '{filename}'.")
    else:
        print(f"File '{filename}' tidak ditemukan.")

def menu():
    while True:
        print("\n=== MULTI-POINT AUTOCLICKER MENU ===")
        print("1. Tambahkan posisi klik")
        print("2. Lihat posisi klik")
        print("3. Atur jumlah perulangan klik")
        print("4. Mulai autoclicker")
        print("5. Hentikan autoclicker")
        print("6. Hapus semua posisi")
        print("7. Simpan posisi ke file")
        print("8. Muat posisi dari file")
        print("9. Keluar")
        choice = input("Pilih opsi: ")

        if choice == '1':
            add_click_position()
        elif choice == '2':
            list_positions()
        elif choice == '3':
            set_max_loops()
        elif choice == '4':
            start_clicker()
        elif choice == '5':
            stop_clicker()
        elif choice == '6':
            clear_positions()
        elif choice == '7':
            save_positions_to_file()
        elif choice == '8':
            load_positions_from_file()
        elif choice == '9':
            stop_clicker()
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    load_positions_from_file()
    menu()
