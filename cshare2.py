import os
import urllib.request
import requests
import json
import time

WEB_KEY_URL = "https://ngquanghuy206.github.io/tooldis/keybotnhac.json"

def get_web_key():
    try:
        response = requests.get(WEB_KEY_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        key = data.get("key")
        print("[✅] Lấy key thành công!")
        return key
    except (requests.RequestException, json.JSONDecodeError) as e:
        print("[❌] Lỗi lấy key. Liên hệ admin.")
        return None

def login_screen() -> bool:
    os.system("clear")

    # === HIỂN THỊ ẢNH ===
    try:
        image_path = os.path.expanduser("~/storage/downloads/22.jpg")
        term_width = os.get_terminal_size().columns
        img_width = 40
        img_height = 15
        pad_left = (term_width - img_width) // 2 + 5  # lệch phải 1 chút

        cmd = f"chafa --size={img_width}x{img_height} '{image_path}'"
        stream = os.popen(cmd)
        for line in stream:
            print(" " * pad_left + line.rstrip())
        stream.close()

    except Exception as e:
        print(f"[⚠️] Không thể hiển thị ảnh: {e}")

    # === BANNER NGAY SAU ẢNH ===
    banner_lines = [
        " ██╗░░░░░░█████╗░░██████╗░██╗███╗░░██╗",
        " ██║░░░░░██╔══██╗██╔════╝░██║████╗░██║",
        " ██║░░░░░██║░░██║██║░░██╗░██║██╔██╗██║",
        " ██║░░░░░██║░░██║██║░░╚██╗██║██║╚████║",
        " ███████╗╚█████╔╝╚██████╔╝██║██║░╚███║",
        " ╚══════╝░╚════╝░░╚═════╝░╚═╝╚═╝░░╚══╝",
        "",
        "🌟 BOT DISCORD BY NGUYỄN QUANG HUY 🌟",
        "🔐 Vui lòng nhập key để đăng nhập",
        "ℹ️ Phiên bản: V2",
        f"⏰ Thời gian: {time.strftime('%I:%M %p, %d/%m/%Y')}",
        "⚠️  Share ko được bán"
    ]

    for line in banner_lines:
        padding = (term_width - len(line)) // 2
        print(" " * padding + line)

    print()
    key = input("🔑 Nhập key xác thực: ")
    web_key = get_web_key()
    if not web_key:
        time.sleep(2)
        return False

    if key == web_key:
        print("[✅] Đăng nhập thành công!")
        time.sleep(1)
        return True
    else:
        print("[❌] Key không hợp lệ! Thử lại.")
        time.sleep(2)
        return False

def banner():
    os.system("clear")
    print("""

██████╗░██╗░██████╗░█████╗░░█████╗░██████╗░██████╗░
██╔══██╗██║██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗
██║░░██║██║╚█████╗░██║░░╚═╝██║░░██║██████╔╝██║░░██║
██║░░██║██║░╚═══██╗██║░░██╗██║░░██║██╔══██╗██║░░██║
██████╔╝██║██████╔╝╚█████╔╝╚█████╔╝██║░░██║██████╔╝
╚═════╝░╚═╝╚═════╝░░╚════╝░░╚════╝░╚═╝░░╚═╝╚═════╝░
╔══════════════════════════════════════════╗
║       BOT DISCORD BY NGUYỄN QUANG HUY     ║
╚══════════════════════════════════════════╝

[✅] Facebook: facebook.com/share/1CJkDWUGBY/
[✅] Zalo: 0904562214
[✅] Gmail: ngquanghuy3027@gmail.com 
[🚨] Lưu Ý Hàng Share Không Mang Bán Hoặc Trao Đổi
    """)

def download_and_run(url, filename):
    try:
        urllib.request.urlretrieve(url, filename)
        print(f"[✓] Đã tải bot, đang chạy...")
        os.system(f"python {filename}")
    except Exception as e:
        print(f"[!] Lỗi: {e}")

def main():
    if not login_screen():
        return
    banner()
    choice = input("Nhập go để vào bot: ")
    if choice == "go":
        download_and_run(
            "https://raw.githubusercontent.com/ngquanghuy206/tooldis/main/app.py",
            "trong.py"
        )
    elif choice == "2":
        download_and_run(
            "https://raw.githubusercontent.com/ngquanghuy206/tooldis/main/app.py",
            "trong.py"
        )
    else:
        print("Lựa chọn không hợp lệ.")

if __name__ == "__main__":
    main()