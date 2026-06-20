#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RedHawk Tool v6.1 - Ultimate Justice Edition
By Farel | Team Pandawa & Ilham
Features: Advanced IP Tracking, Geo-Location with Maps, Self-Trace
"""

import sys
import os
import socket
import time
import hashlib
import json
import webbrowser
import urllib.parse
from datetime import datetime, timedelta
import requests 
from colorama import Fore, Style, init

# Inisialisasi Colorama
init(autoreset=True)

# ==========================================
# KONFIGURASI RAHASIA
# ==========================================
SECRET_SIGNATURE = "FAREL_MASTER_KEY_2026_XYZ" 
SCRIPT_VERSION = "v6.1"
ADMIN_EMAIL = "farellbahtiarr06@gmail.com"
ADMIN_PASSWORD = "werquOnickairi-onic kairi"

# File Database
MASTER_DB_FILE = "master_lock_db.json" 
USER_DATA_FILE = "user_session_redhawk.json"
KEY_POOL_FILE = "key_pool_redhawk.json"
ACTIVE_KEYS_FILE = "active_keys_redhawk.json"
ONLINE_USERS_FILE = "online_users_log.json"
BANNED_KEYS_FILE = "banned_keys.json"
HACKER_LOG_FILE = "hacker_attempts.log"
HASH_FILE = ".integrity_hash_redhawk"

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

host = ""
thr = 0
SCRIPT_NAME = os.path.basename(__file__)

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def print_logo():
    clear_screen()
    logo = (
        f"{C.RED}   ██████╗██╗   ██╗███████╗████████╗\n"
        f"{C.MAGENTA}   ██╔═══╝██║   ██║██╔════╝╚══██╔══╝\n"
        f"{C.PURPLE}   ██║    ██║   ██║███████╗   ██║   \n"
        f"{C.BLUE}   ██║    ██║   ██║╚════██║   ██║   \n"
        f"{C.CYAN}   ╚██████╗╚██████╔╝███████║   ██║   \n"
        f"{C.GREEN}    ╚═════╝ ╚═════╝ ╚══════╝   ╚═╝   \n"
        f"{C.WHITE}{C.BOLD}        [ JUSTICE EDITION v6.1 ]\n"
    )
    print(logo)

# --- FUNGSI ANTI-TAMPER / INTEGRITY CHECK ---
def calculate_hash(filepath):
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                sha256.update(chunk)
        return sha256.hexdigest()
    except FileNotFoundError:
        return None

def check_integrity():
    current_hash = calculate_hash(SCRIPT_NAME)
    
    if '--reset-integrity' in sys.argv:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        session = load_user_session()
        key_id = session['key'] if session and isinstance(session, dict) else "ADMIN_RESET"
        
        log_entry = f"[{timestamp}] | KEY: {key_id} | SCRIPT: REDHAWK TOOL | RESET INTEGRITY BY OWNER\n"
        with open(HACKER_LOG_FILE, "a") as f:
            f.write(log_entry)
            
        with open(HASH_FILE, 'w') as f:
            f.write(current_hash)
        print(f"{C.GREEN}✅ Integrity hash berhasil di-reset untuk {SCRIPT_NAME}.{C.RESET}")
        sys.exit(0)

    if not os.path.exists(HASH_FILE):
        with open(HASH_FILE, 'w') as f:
            f.write(current_hash)
        return True
    
    with open(HASH_FILE, 'r') as f:
        stored_hash = f.read().strip()
        
    if current_hash != stored_hash:
        show_tampered_screen()
        sys.exit(1)
    
    return True

def show_tampered_screen():
    clear_screen()
    session = load_user_session()
    key_id = "UNKNOWN_HACKER"
    if session and isinstance(session, dict):
        key_id = session.get('key', 'UNKNOWN_HACKER')
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] | KEY: {key_id} | SCRIPT: REDHAWK TOOL | TERDETEKSI MODIFIKASI ILEGAL\n"
    try:
        with open(HACKER_LOG_FILE, "a") as f:
            f.write(log_entry)
    except: pass

    skull = f"""{C.RED}{C.BOLD}
      ████████████████████████████
      ██                        ██
      ██   ░░░░░░░░░░░░░░░░░░   ██
      ██   ░░▓▓▓▓▓▓▓▓▓▓▓▓░░   ██
      ██   ░░▓▒▒▒▒▒▒▒▒▒▓░░   ██
      ██   ░░▓▓▒▒░░░░▒▒▒▓▓░░   ██
      ██   ░░▓▒▒░░░░▒▒▒▒▓░░   ██
      ██   ░░▓▓▒▒▒▒▒▒▒▒▓▓░░   ██
      ██   ░░▓▓▓▓▓▓▓▓▓▓▓▓▓░░   ██
      ██   ░░░░░░░░░░░░░░░░░░   ██
      ██                        ██
      ████████████████████████████
    """
    print(skull)
    print(f"{C.RED}{C.BOLD}☠️ PERINGATAN KERAS! ☠️{C.RESET}")
    print(f"{C.RED}Script REDHAWK telah DIMODIFIKASI oleh pihak tidak sah!{C.RESET}")
    print(f"{C.RED}Key Pelaku: {key_id}{C.RESET}")
    print("-" * 40)
    print(f"{C.WHITE}Laporan telah dikirim ke Pusat Admin Farel.{C.RESET}")
    while True: time.sleep(0.5)

def check_master_status():
    try:
        with open(MASTER_DB_FILE, 'r') as f:
            db = json.load(f)
        if db.get('status') == 'maintenance':
            return False
        return True
    except:
        return True 

def report_online_user(user_id, role):
    online_data = {}
    if os.path.exists(ONLINE_USERS_FILE):
        with open(ONLINE_USERS_FILE, 'r') as f:
            online_data = json.load(f)
    online_data[user_id] = {
        "role": role,
        "last_seen": datetime.now().isoformat(),
        "ip": "Local/Unknown"
    }
    with open(ONLINE_USERS_FILE, 'w') as f:
        json.dump(online_data, f)

def save_user_session(key, expiry_date):
    session_data = {
        "key": key,
        "expiry": expiry_date.isoformat(),
        "login_time": datetime.now().isoformat()
    }
    with open(USER_DATA_FILE, "w") as f:
        json.dump(session_data, f)

def load_user_session():
    if not os.path.exists(USER_DATA_FILE):
        return None
    try:
        with open(USER_DATA_FILE, "r") as f:
            content = f.read().strip()
            if not content: return None
            return json.loads(content)
    except:
        return None

def register_active_key(key, days, type_name):
    expiry = datetime.now() + timedelta(days=days)
    active_db = {}
    if os.path.exists(ACTIVE_KEYS_FILE):
        with open(ACTIVE_KEYS_FILE, 'r') as f:
            active_db = json.load(f)
    active_db[key] = {
        "expiry": expiry.isoformat(),
        "type": type_name
    }
    with open(ACTIVE_KEYS_FILE, 'w') as f:
        json.dump(active_db, f)
    return expiry

def buy_key_menu():
    print(f"\n{C.YELLOW}•============================•{C.RESET}")
    print(f"{C.WHITE}  DAFTAR HARGA KEY RESMI{C.RESET}")
    print(f"{C.YELLOW}•============================•{C.RESET}")
    print(f"{C.GREEN}[1] Key Harian (1 Hari) ... Rp 2.000{C.RESET}")
    print(f"{C.GREEN}[2] Key 3 Hari ............ Rp 3.000{C.RESET}")
    print(f"{C.GREEN}[3] Key 5 Hari ............ Rp 4.000{C.RESET}")
    print(f"{C.GREEN}[4] Key Permanen .......... Rp 7.000{C.RESET}")
    print(f"{C.YELLOW}•============================•{C.RESET}")
    
    choice = input(f"{C.BOLD}Pilih nomor untuk beli (1-4) atau 0 kembali: {C.RESET}")
    if choice == "0": return
    
    prices = {"1": "2000", "2": "3000", "3": "4000", "4": "7000"}
    names = {"1": "Harian", "2": "3 Hari", "3": "5 Hari", "4": "Permanen"}
    
    if choice in prices:
        subject = f"Beli Key REDHAWK {names[choice]}"
        body = f"Halo Admin Farel,\n\nSaya ingin membeli Key REDHAWK tipe: {names[choice]}.\nHarga: Rp {prices[choice]}\n\nMohon segera diproses."
        safe_subject = urllib.parse.quote(subject)
        safe_body = urllib.parse.quote(body)
        url = f"mailto:{ADMIN_EMAIL}?subject={safe_subject}&body={safe_body}"
        print(f"{C.CYAN}Sedang membuka aplikasi Email...{C.RESET}")
        try: webbrowser.open(url)
        except: pass
        print(f"\n{C.YELLOW}Jika email tidak terbuka otomatis:{C.RESET}")
        print(f"{C.WHITE}Silakan kirim pesan ke: {ADMIN_EMAIL}{C.RESET}")
        input(f"\n{C.GREEN}Tekan Enter setelah mengirim email...{C.RESET}")
    else:
        print(f"{C.RED}Pilihan tidak valid.{C.RESET}")
        time.sleep(1)

def login_system():
    if not check_integrity(): show_tampered_screen()
    if not check_master_status():
        print_logo()
        print(f"\n{C.YELLOW}{C.BOLD}🛑 SABAR! SEDANG DILAKUKAN UPDATE SISTEM... 🛑{C.RESET}")
        while True: time.sleep(1) 

    while True:
        print_logo()
        print(f"{C.BOLD}{C.WHITE}   MENU LOGIN 🔐{C.RESET}\n")
        print(f"{C.GREEN}[1] Masuk Sebagai Pengguna{C.RESET}")
        print(f"{C.MAGENTA}[2] Masuk Sebagai Admin{C.RESET}")
        print(f"{C.RED}[3] Keluar{C.RESET}")
        
        choice = input(f"\n{C.BOLD}Pilihan »{C.RESET} ").strip()
        
        if choice == "1":
            handle_user_login()
            break
        elif choice == "2":
            pw = input(f"{C.MAGENTA}Masukkan Password Admin »{C.RESET} ").strip()
            if pw == ADMIN_PASSWORD:
                print(f"{C.GREEN}✅ Akses Admin Diberikan!{C.RESET}")
                report_online_user("ADMIN_FAREL", "SUPER_ADMIN")
                time.sleep(1)
                show_main_menu("ADMIN_MODE")
                break
            else:
                print(f"{C.RED}❌ Password Salah!{C.RESET}")
                time.sleep(1)
        elif choice == "3":
            sys.exit(0)

def handle_user_login():
    session = load_user_session()
    if session:
        banned_list = []
        if os.path.exists(BANNED_KEYS_FILE):
            with open(BANNED_KEYS_FILE, 'r') as f:
                banned_data = json.load(f)
                banned_list = [item['key'] for item in banned_data]
        
        if session['key'] in banned_list:
            print(f"{C.RED}{C.BOLD}☠️ AKSES DITOLAK! ☠️{C.RESET}")
            print(f"{C.RED}Key Anda ({session['key']}) telah diblokir permanen oleh Admin Farel.{C.RESET}")
            if os.path.exists(USER_DATA_FILE): os.remove(USER_DATA_FILE)
            input(f"\n{C.BOLD}Tekan Enter untuk keluar...{C.RESET}")
            sys.exit(0)

        expiry = datetime.fromisoformat(session['expiry'])
        now = datetime.now()
        if now < expiry:
            print(f"{C.GREEN}✅ Sesi Aktif Terdeteksi.{C.RESET}")
            report_online_user(session['key'], "USER")
            time.sleep(1)
            show_main_menu(session['key'])
            return
        else:
            print(f"{C.RED}⚠️ Masa aktif key habis. Silakan login ulang.{C.RESET}")
            if os.path.exists(USER_DATA_FILE): os.remove(USER_DATA_FILE)
            time.sleep(2)

    while True:
        print_logo()
        print(f"{C.BOLD}{C.WHITE}   LOGIN PENGGUNA 🔐{C.RESET}\n")
        print(f"{C.GREEN}[1] Masukkan Key{C.RESET}")
        print(f"{C.YELLOW}[2] Beli Key Baru{C.RESET}")
        print(f"{C.RED}[3] Kembali{C.RESET}")
        
        choice = input(f"\n{C.BOLD}Pilihan »{C.RESET} ").strip()
        
        if choice == "1":
            key_input = input(f"{C.GREEN}Masukkan Key »{C.RESET} ").strip()
            banned_list = []
            if os.path.exists(BANNED_KEYS_FILE):
                with open(BANNED_KEYS_FILE, 'r') as f:
                    banned_data = json.load(f)
                    banned_list = [item['key'] for item in banned_data]
            
            if key_input in banned_list:
                print(f"{C.RED}{C.BOLD}☠️ MAAF, KEY INI TELAH DI-BAN! ☠️{C.RESET}")
                time.sleep(3)
                continue

            active_db = {}
            if os.path.exists(ACTIVE_KEYS_FILE):
                with open(ACTIVE_KEYS_FILE, 'r') as f:
                    active_db = json.load(f)
            
            pool_db = []
            if os.path.exists(KEY_POOL_FILE):
                with open(KEY_POOL_FILE, 'r') as f:
                    pool_db = json.load(f)

            if key_input in active_db or key_input in pool_db:
                days = 1 
                type_name = "Harian (Auto)"
                
                if key_input in active_db:
                    k_info = active_db[key_input]
                    expiry = datetime.fromisoformat(k_info['expiry'])
                    type_name = k_info.get('type', 'Harian')
                else:
                    expiry = datetime.now() + timedelta(days=1)
                    
                now = datetime.now()
                
                if now < expiry:
                    save_user_session(key_input, expiry)
                    report_online_user(key_input, "USER")
                    print(f"{C.GREEN}✅ Key Valid! Akses Diberikan.{C.RESET}")
                    print(f"{C.CYAN}Masa aktif: {type_name}{C.RESET}")
                    
                    if key_input not in active_db:
                        register_active_key(key_input, 1, "Harian (Dari Pool)")
                        
                    time.sleep(1.5)
                    show_main_menu(key_input)
                    break
                else:
                    print(f"{C.RED}❌ Key ini sudah kadaluarsa.{C.RESET}")
                    if key_input in active_db:
                        del active_db[key_input]
                        with open(ACTIVE_KEYS_FILE, 'w') as f:
                            json.dump(active_db, f)
                    time.sleep(1.5)
            else:
                print(f"{C.RED}❌ Key Tidak Dikenal/Salah.{C.RESET}")
                time.sleep(1.5)
                
        elif choice == "2":
            buy_key_menu()
        elif choice == "3":
            break

def show_main_menu(current_key):
    while True:
        clear_screen()
        hammer_ascii = (
            f"{C.RED}  ██╗   ██╗███████╗██╗   ██╗\n"
            f"{C.ORANGE}  ██║   ██║██╔════╝██║   ██║\n"
            f"{C.YELLOW}  ██║   ██║█████╗  ██║   ██║\n"
            f"{C.GREEN}  ██║   ██║██╔══╝  ██║   ██║\n"
            f"{C.BLUE}  ╚██████╔╝███████╗╚██████╔╝\n"
            f"{C.PURPLE}   ╚═════╝ ╚══════╝ ╚═════╝ \n"
            f"        {C.WHITE}{C.BOLD}BY FAREL | {SCRIPT_VERSION}{C.RESET}\n"
        )
        print(hammer_ascii)
        
        if current_key == "ADMIN_MODE":
            print(f"{C.MAGENTA}{C.BOLD}   MODE ADMIN AKTIF (UNLIMITED POWER){C.RESET}\n")
        else:
            session = load_user_session()
            time_left = "Unknown"
            if session:
                expiry = datetime.fromisoformat(session['expiry'])
                delta = expiry - datetime.now()
                if delta.days > 1000: time_left = "PERMANEN"
                else: time_left = f"{delta.days} Hari {delta.seconds // 3600} Jam"
            print(f"{C.CYAN} Status Key : {current_key}\n Sisa Waktu : {time_left}{C.RESET}\n")

        menu_box = (
            f"{C.CYAN}•==================================•\n"
            f"{C.GREEN}[1.] Mode 1: Lacak IP & Domain (Full Info)\n"
            f"{C.BLUE}[2.] Mode 2: Lacak Lokasi Akurat (Maps)\n"
            f"{C.YELLOW}[3.] Laporkan Masalah\n"
            f"{C.RED}[4.] Logout\n"
            f"{C.CYAN}•==================================•\n"
        )
        print(menu_box)
        
        choice = input(f"{C.BOLD}masukan pilihan mu 》♤¥~€£◇ {C.RESET}").strip()
        
        if choice == "1":
            start_tracking_mode_1()
        elif choice == "2":
            start_tracking_mode_2()
        elif choice == "3":
            report_issue()
        elif choice == "4":
            if os.path.exists(USER_DATA_FILE): os.remove(USER_DATA_FILE)
            print(f"{C.GREEN}Logout berhasil.{C.RESET}")
            time.sleep(1)
            login_system()
            break
        else:
            print(f"{C.RED}Pilihan tidak valid!{C.RESET}")
            time.sleep(1)

def report_issue():
    print(f"\n{C.YELLOW}Mengarahkan ke email pelaporan...{C.RESET}")
    mailto_link = f"mailto:{ADMIN_EMAIL}?subject=Laporan REDHAWK v6.1"
    webbrowser.open(mailto_link)
    input(f"\n{C.CYAN}Tekan Enter untuk kembali...{C.RESET}")

def clean_url(url):
    """Membersihkan URL dari http, https, dan slash di akhir"""
    url = url.lower().strip()
    if url.startswith("http://"):
        url = url[7:]
    if url.startswith("https://"):
        url = url[8:]
    if url.endswith("/"):
        url = url[:-1]
    return url

def fetch_api_data(api_url, title):
    """Fungsi umum untuk mengambil data dari API Hackertarget"""
    print(f"\n{C.BOLD}{C.BLUE}{title}{C.RESET}")
    print("=" * 40)
    try:
        response = requests.get(api_url, timeout=15)
        if response.status_code == 200:
            print(response.text)
        else:
            print(f"{C.RED}Gagal mengambil data (Status: {response.status_code}){C.RESET}")
    except Exception as e:
        print(f"{C.RED}Error: {e}{C.RESET}")

# ==========================================
# MODE 1: LACAK IP & DOMAIN (FULL INFO)
# ==========================================
def start_tracking_mode_1():
    clear_screen()
    print(f"{C.RED}{C.BOLD}  🕵️  MODE 1: FULL INFORMATION TRACKING 🕵️{C.RESET}\n")
    print(f"{C.YELLOW}[!] Support: Domain (www.site.com) atau IP Address{C.RESET}\n")
    
    raw_host = input(f"{C.GREEN}  Masukkan Target »{C.RESET} ").strip()
    target = clean_url(raw_host)
    
    if not target:
        print(f"{C.RED}❌ Target tidak boleh kosong!{C.RESET}")
        input(f"\n{C.CYAN}Tekan Enter untuk kembali...{C.RESET}")
        return

    print(f"\n{C.YELLOW}  [+] Scanning Begins ...{C.RESET}")
    print(f"{C.BLUE}  [i] Scanning Site: {C.GREEN}{target}{C.RESET}\n")

    try:
        # 1. Basic Info (IP & Server)
        ip_address = socket.gethostbyname(target)
        print(f"{C.BOLD}{C.BLUE}B A S I C   I N F O{C.RESET}")
        print("=" * 40)
        print(f"{C.BLUE}[+] IP Address: {C.GREEN}{ip_address}{C.RESET}")
        
        # Cek Webserver
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            r = requests.get(f"http://{target}", headers=headers, timeout=5)
            server = r.headers.get('Server', 'Could Not Detect')
            print(f"{C.BLUE}[+] Web Server: {C.GREEN}{server}{C.RESET}")
        except:
            print(f"{C.BLUE}[+] Web Server: {C.RED}Could Not Detect{C.RESET}")

        # 2. Whois Lookup
        fetch_api_data(f"http://api.hackertarget.com/whois/?q={target}", "W H O I S   L O O K U P")

        # 3. Geo IP Lookup
        fetch_api_data(f"http://api.hackertarget.com/geoip/?q={ip_address}", "G E O  I P  L O O K U P")

        # 4. HTTP Headers
        fetch_api_data(f"http://api.hackertarget.com/httpheaders/?q={target}", "H T T P   H E A D E R S")

        # 5. DNS Lookup
        fetch_api_data(f"http://api.hackertarget.com/dnslookup/?q={target}", "D N S   L O O K U P")

        # 6. Nmap Port Scan
        fetch_api_data(f"http://api.hackertarget.com/nmap/?q={target}", "N M A P   P O R T   S C A N")

        # 7. Subdomain Finder
        fetch_api_data(f"http://api.hackertarget.com/hostsearch/?q={target}", "S U B - D O M A I N   F I N D E R")

        # 8. Reverse IP Lookup
        fetch_api_data(f"http://api.hackertarget.com/reverseiplookup/?q={ip_address}", "R E V E R S E   I P   L O O K U P")

        print(f"\n{C.GREEN}  ✅ PELACAKAN SELESAI!{C.RESET}")
        
    except socket.gaierror:
        print(f"{C.RED}  ❌ Gagal! Domain/IP '{target}' tidak ditemukan.{C.RESET}")
    except Exception as e:
        print(f"{C.RED}  ❌ Terjadi kesalahan: {e}{C.RESET}")

    input(f"\n{C.CYAN}Tekan Enter untuk kembali ke menu...{C.RESET}")

# ==========================================
# MODE 2: LACAK LOKASI AKURAT (MAPS)
# ==========================================
def start_tracking_mode_2():
    clear_screen()
    print(f"{C.RED}{C.BOLD}  💀 MODE 2: ACCURATE GEO-LOCATION TRACKER 💀{C.RESET}\n")
    print(f"{C.RED}⚠️ WARNING: GUNAKAN DENGAN BIJAK. SAYA TIDAK BERTANGGUNG JAWAB ATAS PENYALAHGUNAAN HUKUM.{C.RESET}\n")
    
    target_input = input(f"{C.GREEN}  Masukkan IP / Ketik 'lacak saya' untuk IP sendiri »{C.RESET} ").strip()
    
    if not target_input:
        print(f"{C.RED}❌ Input kosong!{C.RESET}")
        input(f"\n{C.CYAN}Tekan Enter untuk kembali...{C.RESET}")
        return

    # Fitur Lacak Sendiri
    if target_input.lower() in ["lacak saya", "me", "saya", "myip"]:
        print(f"\n{C.YELLOW}[*] Mendeteksi IP Publik Anda...{C.RESET}")
        try:
            my_ip_req = requests.get("https://api.ipify.org/", timeout=10)
            target_ip = my_ip_req.text.strip()
            print(f"{C.GREEN}[+] IP Anda: {target_ip}{C.RESET}")
        except:
            print(f"{C.RED}[-] Gagal mendeteksi IP sendiri. Cek koneksi internet.{C.RESET}")
            input(f"\n{C.CYAN}Tekan Enter untuk kembali...{C.RESET}")
            return
    else:
        target_ip = target_input

    print(f"\n{C.YELLOW}[*] Sedang menembus database lokasi global...{C.RESET}")
    time.sleep(1)
    
    # Menggunakan API ip-api.com untuk akurasi koordinat
    url = f"http://ip-api.com/json/{target_ip}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data['status'] == 'fail':
            print(f"\n{Fore.RED}☠️ Gagal lacak target! Pastikan IP bener ☠️{Style.RESET_ALL}")
            print(f"{Fore.RED}[!] Error: {data['message']}{Style.RESET_ALL}")
            input(f"\n{C.CYAN}Tekan Enter untuk kembali...{C.RESET}")
            return

        lat = data['lat']
        lon = data['lon']
        city = data['city']
        region = data['regionName']
        country = data['country']
        isp = data['isp']
        
        print(f"\n{Fore.GREEN}💀 SUKSES LACAK TARGET 💀{Style.RESET_ALL}")
        print(f"{Fore.WHITE}----------------------------------------{Style.RESET_ALL}")
        print(f"  Target IP    : {data['query']}")
        print(f"  Provider     : {isp}")
        print(f"  Lokasi Asli  : {city}, {region}, {country}")
        print(f"  Koordinat    : {lat}, {lon}")
        print(f"{Fore.WHITE}----------------------------------------{Style.RESET_ALL}\n")
        
        # Membuat Link Google Maps
        maps_link = f"https://www.google.com/maps?q={lat},{lon}"
        
        print(f"{Fore.CYAN}[+] SALIN LINK INI UNTUK LACAK LOKASI DI CHROME:{Style.RESET_ALL}")
        print(f"{Fore.BLUE}{maps_link}{Style.RESET_ALL}\n")
        print(f"{Fore.YELLOW}[!] Tips: Tekan lama pada link untuk menyalin (Copy).{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}[-] Koneksi terputus atau error: {str(e)}{Style.RESET_ALL}")

    input(f"\n{C.CYAN}Tekan Enter untuk kembali ke menu...{C.RESET}")

if __name__ == '__main__':
    try:
        login_system()
    except KeyboardInterrupt:
        sys.exit(0)
