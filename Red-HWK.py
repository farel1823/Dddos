import os
import sys
import time
import random
import hashlib
import urllib.request
import socket

# --- KONFIGURASI WARNA TERMINAL ---
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"

C = Colors()
VERSION = "V2.4"
SCRIPT_NAME = os.path.basename(__file__)
HASH_FILE = ".integrity_hash"

def clear():
    os.system("clear")

def pause(detik=2):
    time.sleep(detik)

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
    
    # Mode Reset Owner: Update hash jika ada argumen khusus
    if '--reset-integrity' in sys.argv:
        with open(HASH_FILE, 'w') as f:
            f.write(current_hash)
        print(f"{C.GREEN}✅ Integrity hash berhasil di-reset untuk {SCRIPT_NAME}.{C.RESET}")
        print(f"{C.YELLOW}Silakan jalankan ulang script tanpa argumen --reset-integrity{C.RESET}")
        sys.exit(0)

    # Cek apakah file hash baseline sudah ada
    if not os.path.exists(HASH_FILE):
        with open(HASH_FILE, 'w') as f:
            f.write(current_hash)
        print(f"{C.GREEN} Baseline integrity dibuat. Script aman.{C.RESET}")
        pause(1)
        return True
    
    # Bandingkan hash saat ini dengan yang tersimpan
    with open(HASH_FILE, 'r') as f:
        stored_hash = f.read().strip()
        
    if current_hash != stored_hash:
        show_tampered_screen()
        sys.exit(1)
    
    return True

def show_tampered_screen():
    clear()
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
    print(f"{C.RED}{C.BOLD}️  PERINGATAN KERAS! ️{C.RESET}")
    print(f"{C.RED}Script telah DIMODIFIKASI oleh pihak tidak sah!{C.RESET}")
    print(f"{C.RED}Versi Asli: {VERSION} | Status: TAMPERED{C.RESET}")
    print("-" * 40)
    print(f"{C.WHITE}TIDAK BISA MENJALANKAN SCRIPT INI!{C.RESET}")
    print(f"{C.WHITE}File integritas rusak. Hubungi pembuat asli.{C.RESET}")
    print("-" * 40)
    print(f"{C.YELLOW}Jika Anda pemilik asli dan baru saja mengedit script,{C.RESET}")
    print(f"{C.YELLOW}jalankan: python {SCRIPT_NAME} --reset-integrity{C.RESET}")
    print()

# --- ASCII ART & BANNER V2.4 ---
BANNER = f"""{C.GREEN}
   _______  _______  _______  _______ 
  (  ____ $  ___  )(  ____ $  ____ \\
  | (    \/| (   ) || (    \/| (    \/
  | |      | (___) || (__    | (_____ 
  | |      |  ___  ||  __)   (_____  )
  | |      | (   ) || (            ) |
  | (____/\| )   ( || (____/\/\____) |
  (_______/|/     \|(_______/\_______)
{C.BOLD}   RED HAWK {VERSION} - LOGIN EDITION
   Author: Farel & Ilham Team
   [ANTI-TAMPER PROTECTED]
{C.RESET}"""

LOGIN_BANNER = f"""{C.CYAN}
========================================
       LOGIN LAGE SYSTEM {VERSION}
========================================
[1] Masuk sebagai Admin
[2] Masuk sebagai Pengguna (Ujian 50 Soal)
[3] Beli Script (WhatsApp Auto)
[4] Keluar
========================================
{C.RESET}"""

# --- FITUR ADMIN ---
def mode_admin():
    clear()
    print(f"{C.CYAN}[MODE ADMIN]{C.RESET}")
    print("Masukkan Kode Pembuat:")
    kode = input("Kode: ").strip()
    
    if kode == "3456":
        print(f"\n{C.GREEN}✅ Akses Admin Diberikan! Selamat datang, Creator.{C.RESET}")
        pause(2)
        run_redhawk()
    else:
        print(f"\n{C.RED}❌ Kode Salah! Akses Ditolak.{C.RESET}")
        pause(2)

# --- FITUR BELI SCRIPT ---
def mode_beli():
    clear()
    print(f"{C.YELLOW}[BELI SCRIPT PREMIUM]{C.RESET}")
    print("-" * 40)
    print("Harga: Rp 5.000")
    print("Kirim bukti TF ke Admin untuk dapat kode login instan.")
    print("-" * 40)
    
    for i in range(50, -1, -1):
        mins, secs = divmod(i, 60)
        print(f"\rWaktu membaca ketentuan: {mins:02d}:{secs:02d}  ", end="", flush=True)
        time.sleep(1)
        
        if i == 0:
            print("\n\n⏰ Waktu Habis! Mengarahkan ke WhatsApp Admin...")
            os.system("termux-open-url 'https://wa.me/6287788240816?text=Halo%20Admin,%20saya%20mau%20beli%20script'")
            pause(3)
            return

    confirm = input("\n\nApakah Anda sudah paham? (ketik 'paham'): ").strip().lower()
    
    if confirm == "paham":
        print("\nMengarahkan ke kontak Admin...")
        os.system("termux-open-url 'https://wa.me/6287788240816?text=Halo%20Admin,%20saya%20mau%20beli%20script'")
        pause(2)
        
        kode_beli = input("\nSudah beli? Masukkan Kode Login Instan: ").strip()
        if kode_beli == "jalan6789":
            print(f"\n{C.GREEN}✅ Kode Valid! Login Berhasil.{C.RESET}")
            pause(2)
            run_redhawk()
        else:
            print(f"\n{C.RED}❌ Kode Salah atau belum membeli.{C.RESET}")
            pause(2)

# --- FITUR UJIAN (FLEKSIBEL JAWABAN SALAH) ---
def generate_soal():
    bank = []
    # 20 Soal Matematika
    for _ in range(20):
        a = random.randint(10, 99)
        b = random.randint(10, 99)
        ans = a + b
        wrong1 = ans + random.randint(1, 10)
        wrong2 = ans - random.randint(1, 10)
        opts = [f"A. {ans}", f"B. {wrong1}", f"C. {wrong2}"]
        random.shuffle(opts)
        
        key = ''
        for opt in opts:
            if str(ans) in opt:
                key = opt[0]
                
        bank.append({
            'type': 'abc',
            'q': f"[Matematika] Berapakah hasil dari {a} + {b}?",
            'opts': opts,
            'key': key
        })
    
    # 30 Soal Esai
    topics = ["Ibukota Indonesia", "Presiden Pertama RI", "Warna Bendera Indonesia"]
    for i in range(30):
        bank.append({
            'type': 'esai',
            'q': f"[Pengetahuan Umum] Sebutkan {topics[i % 3]}!",
        })
        
    random.shuffle(bank)
    return bank[:50]

def mode_pengguna():
    clear()
    print(f"{C.CYAN}[UJIAN WAJIB NILAI 100]{C.RESET}")
    print("Total Soal: 50 (Acak & Anti-Contek)")
    print("Waktu: 10 Menit (Timer Berjalan)")
    print("Catatan: Jawaban salah tetap bisa lanjut, tapi nilai harus 100!")
    
    input("\nTekan Enter untuk memulai ujian...")
    
    soals = generate_soal()
    score = 0
    start_time = time.time()
    duration = 600  # 10 menit
    
    for i in range(50):
        elapsed = time.time() - start_time
        remaining = int(duration - elapsed)
        
        if remaining <= 0:
            print(f"\n{C.RED}⏰ WAKTU HABIS! Ujian Gagal.{C.RESET}")
            pause(3)
            return
            
        clear()
        mins, secs = divmod(remaining, 60)
        print(f"{C.CYAN}[Soal {i+1}/50] | Sisa Waktu: {mins:02d}:{secs:02d}{C.RESET}")
        print("-" * 40)
        print(soals[i]['q'])
        
        if soals[i]['type'] == 'abc':
            for opt in soals[i]['opts']:
                print(opt)
            jawab = input("Pilihan (A/B/C): ").strip().upper()
            
            # Jawaban salah tetap lanjut ke soal berikutnya
            if jawab == soals[i]['key']:
                score += 2
                print(f"{C.GREEN}✅ Benar! (+2 Poin){C.RESET}")
            else:
                print(f"{C.RED}❌ Salah! Kunci: {soals[i]['key']} (Lanjut soal berikutnya...){C.RESET}")
        else:
            print("(Ketik jawaban singkat)")
            jawab = input("Jawaban: ").strip()
            # Jawaban esai asal ketik > 3 huruf dianggap benar untuk fleksibilitas
            if len(jawab) > 3:
                score += 2
                print(f"{C.GREEN}✅ Jawaban tercatat! (+2 Poin){C.RESET}")
            else:
                print(f"{C.RED}❌ Jawaban terlalu pendek! (Lanjut soal berikutnya...){C.RESET}")
                
        pause(1)
    
    print("\nSedang mengambil nilai...")
    pause(2)
    
    final = min(score, 100)
    print(f"\n{C.BOLD}HASIL UJIAN:{C.RESET}")
    print(f"Nilai Akhir: {final}/100")
    
    # SYARAT MUTLAK: HARUS 100
    if final == 100:
        print(f"\n{C.GREEN} SELAMAT! Nilai Anda 100. Akses Diberikan!{C.RESET}")
        pause(2)
        run_redhawk()
    else:
        print(f"\n{C.RED}❌ Nilai Anda: {final}. Wajib 100 untuk masuk!{C.RESET}")
        ulang = input("\nIngin mengulang ujian? (y/n): ").strip().lower()
        if ulang == 'y':
            mode_pengguna()

# --- RED HAWK TOOL (API VERSION) ---
def fetch_api(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode('utf-8')
    except Exception:
        return None

def run_redhawk():
    while True:
        clear()
        print(f"""{C.RED}
---------------------------------------------------------------------------
   RED HAWK ALL IN ONE INFORMATION GATHERING TOOL
   Author : By Farel (Termux Port)
   Team   : Ilham & Farel
   Version: {VERSION} (Python API Edition)
---------------------------------------------------------------------------
{C.RESET}""")

        target = input(f"{C.BLUE}Enter Target Domain (example: google.com) or 'exit': {C.GREEN}").strip()
        
        if target.lower() == 'exit':
            break
        if not target or '.' not in target:
            print(f"{C.RED}Enter A Valid URL{C.RESET}")
            pause(2)
            continue

        domain = target.replace('http://', '').replace('https://', '').replace('www.', '')
        
        print(f"\n{C.BLUE}[i] Scanning Site: {C.GREEN}http://{domain}{C.RESET}")
        print(f"{C.BLUE}[+] Scanning Begins ...{C.RESET}\n")

        try:
            ip = socket.gethostbyname(domain)
            print(f"{C.BLUE}[+] IP address: {C.GREEN}{ip}{C.RESET}")
        except:
            ip = "Could Not Resolve"
            print(f"{C.BLUE}[+] IP address: {C.RED}{ip}{C.RESET}")

        print(f"{C.BLUE}[+] Checking Headers & CMS...{C.RESET}")
        try:
            req = urllib.request.Request(f"http://{domain}", headers={'User-Agent': 'Mozilla/5.0'})
            resp = urllib.request.urlopen(req, timeout=10)
            server = resp.headers.get('Server', 'Unknown')
            content = resp.read().decode('utf-8', errors='ignore')
            
            cms = "Could Not Detect"
            if '/wp-content/' in content: cms = "WordPress"
            elif 'Joomla' in content: cms = "Joomla"
            
            print(f"{C.BLUE}[+] Web Server: {C.GREEN}{server}{C.RESET}")
            print(f"{C.BLUE}[+] CMS Detected: {C.GREEN}{cms}{C.RESET}")
        except:
            print(f"{C.BLUE}[+] Web Server: {C.RED}Connection Failed{C.RESET}")
            print(f"{C.BLUE}[+] CMS Detected: {C.RED}Connection Failed{C.RESET}")

        print(f"{C.BLUE}[+] Checking Cloudflare...{C.RESET}")
        cf_data = fetch_api(f"http://api.hackertarget.com/httpheaders/?q={domain}")
        if cf_data and 'cloudflare' in cf_data.lower():
            print(f"{C.BLUE}[+] Cloudflare: {C.RED}Detected{C.RESET}")
        else:
            print(f"{C.BLUE}[+] Cloudflare: {C.GREEN}Not Detected{C.RESET}")

        print(f"\n{C.BOLD}{C.CYAN}WHOIS & GEO IP LOOKUP{C.RESET}")
        print("=" * 30)
        whois = fetch_api(f"http://api.hackertarget.com/whois/?q={domain}")
        print(whois if whois else f"{C.RED}Failed to fetch Whois{C.RESET}")
        
        geo = fetch_api(f"http://api.hackertarget.com/geoip/?q={ip}")
        print(geo if geo else f"{C.RED}Failed to fetch GeoIP{C.RESET}")

        print(f"\n{C.BOLD}{C.CYAN}SUBDOMAIN FINDER{C.RESET}")
        print("=" * 30)
        subs = fetch_api(f"http://api.hackertarget.com/hostsearch/?q={domain}")
        if subs:
            print(f"{C.GREEN}{subs}{C.RESET}")
        else:
            print(f"{C.RED}Failed to fetch subdomains{C.RESET}")

        input(f"\n{C.BLUE}Press Enter to scan another domain...{C.RESET}")

# --- MENU UTAMA ---
def main_menu():
    while True:
        clear()
        print(BANNER)
        print(LOGIN_BANNER)
        
        pilih = input("Pilih opsi [1-4]: ").strip()
        
        if pilih == "1": mode_admin()
        elif pilih == "2": mode_pengguna()
        elif pilih == "3": mode_beli()
        elif pilih == "4": 
            print(f"\n{C.GREEN}Terima kasih telah menggunakan RedHawk {VERSION}! 👋{C.RESET}")
            sys.exit()
        else:
            print(f"\n{C.RED}Pilihan tidak valid!{C.RESET}")
            pause(2)

if __name__ == "__main__":
    check_integrity()  # Cek integritas SEBELUM menu utama jalan
    main_menu()
