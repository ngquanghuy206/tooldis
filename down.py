import os
import requests
import uuid
from datetime import datetime
import re
import json

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    banner = """

██████╗░░█████╗░░██╗░░░░░░░██╗███╗░░██╗
██╔══██╗██╔══██╗░██║░░██╗░░██║████╗░██║
██║░░██║██║░░██║░╚██╗████╗██╔╝██╔██╗██║
██║░░██║██║░░██║░░████╔═████║░██║╚████║
██████╔╝╚█████╔╝░░╚██╔╝░╚██╔╝░██║░╚███║
╚═════╝░░╚════╝░░░░╚═╝░░░╚═╝░░╚═╝░░╚══╝

██╗░░░██╗██╗██████╗░███████╗░█████╗░
██║░░░██║██║██╔══██╗██╔════╝██╔══██╗
╚██╗░██╔╝██║██║░░██║█████╗░░██║░░██║
░╚████╔╝░██║██║░░██║██╔══╝░░██║░░██║
░░╚██╔╝░░██║██████╔╝███████╗╚█████╔╝
░░░╚═╝░░░╚═╝╚═════╝░╚══════╝░╚════╝░    
    ╔════════════════════════════════════════════════════════════╗
    ║        TOOL TẢI VIDEO ĐA NỀN TẢNG BY NGUYEN QUANG HUY      ║
    ╠════════════════════════════════════════════════════════════╩
    ║ Admin: Nguyen Quang Huy                                    ║
    ║ Facebook: https://www.facebook.com/share/1CJkDWUGBY/       ║
    ║ Zalo: 0904562214                                           ║
    ║ Gmail: ngquanghuy3027@gmail.com                            ║
    ║ Last Update: 8h25 28/6/2025                                ║
    ╚════════════════════════════════════════════════════════════╝
    """
    print(banner)

def download_file(url, filename):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            return True
        else:
            return False
    except Exception as e:
        print(f"Lỗi khi tải file: {e}")
        return False

def sanitize_filename(filename):
    return re.sub(r'[^\w\s.-]', '', filename).replace(' ', '_')

def download_youtube(url):
    api_url = f"https://subhatde.id.vn/youtube/download?url={url}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            for media in data['media']:
                if media['type'] == 'video' and media['quality'] == '360p':
                    title = sanitize_filename(data['title'][:50])  
                    filename = f"youtube_{data['id']}_{title}.mp4"
                    print(f"Đang tải: {data['title']}")
                    if download_file(media['url'], filename):
                        print(f"Tải thành công: {filename}")
                    else:
                        print(f"Tải thất bại: {data['title']}")
                    return
            print("Không tìm thấy video chất lượng 360p")
        else:
            print("Lỗi khi gọi API YouTube")
    except Exception as e:
        print(f"Lỗi: {e}")

def download_facebook(url):
    api_url = f"https://subhatde.id.vn/fb/download?url={url}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            for media in data['medias']:
                if media['type'] == 'video' and media['quality'] == 'SD':
                    title = sanitize_filename(data['title'][:50] if data['title'] else f"fb_video_{uuid.uuid4()}")
                    filename = f"facebook_{uuid.uuid4()}_{title}.mp4"
                    print(f"Đang tải: {data['title']}")
                    if download_file(media['url'], filename):
                        print(f"Tải thành công: {filename}")
                    else:
                        print(f"Tải thất bại: {data['title']}")
                    return
            print("Không tìm thấy video chất lượng SD")
        else:
            print("Lỗi khi gọi API Facebook")
    except Exception as e:
        print(f"Lỗi: {e}")

def download_instagram(url):
    api_url = f"https://subhatde.id.vn/instagram/download?link={url}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            for attachment in data['attachments']:
                if attachment['type'] == 'Video':
                    caption = sanitize_filename(data['caption'][:50] if data['caption'] else f"ig_video_{uuid.uuid4()}")
                    filename = f"instagram_{data['id']}_{caption}.mp4"
                    print(f"Đang tải: {data['caption']}")
                    if download_file(attachment['url'], filename):
                        print(f"Tải thành công: {filename}")
                    else:
                        print(f"Tải thất bại: {data['caption']}")
                    return
            print("Không tìm thấy video")
        else:
            print("Lỗi khi gọi API Instagram")
    except Exception as e:
        print(f"Lỗi: {e}")

def download_tiktok(url):
    api_url = f"https://subhatde.id.vn/tiktok/downloadvideo?url={url}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            if data['code'] == 0:
                title = sanitize_filename(data['data']['title'][:50] if data['data']['title'] else f"tiktok_video_{uuid.uuid4()}")
                filename = f"tiktok_{data['data']['id']}_{title}.mp4"
                print(f"Đang tải: {data['data']['title']}")
                if download_file(data['data']['play'], filename):
                    print(f"Tải thành công: {filename}")
                else:
                    print(f"Tải thất bại: {data['data']['title']}")
            else:
                print("Lỗi: Không tìm thấy video TikTok")
        else:
            print("Lỗi khi gọi API TikTok")
    except Exception as e:
        print(f"Lỗi: {e}")

def process_links(links, platform):
    download_functions = {
        '1': download_youtube,
        '2': download_facebook,
        '3': download_instagram,
        '4': download_tiktok
    }
    for link in links:
        link = link.strip()
        if link:
            download_functions[platform](link)

def main_menu():
    while True:
        clear_screen()
        display_banner()
        print("Chọn nền tảng để tải video:")
        print("1. YouTube")
        print("2. Facebook")
        print("3. Instagram")
        print("4. TikTok")
        print("5. Thoát")
        choice = input("[NGQUANGHUY] Nhập lựa chọn (1-5): ").strip()

        if choice == '5':
            print("Cảm ơn bạn đã sử dụng công cụ!")
            break

        if choice not in ['1', '2', '3', '4']:
            print("Lựa chọn không hợp lệ, vui lòng chọn lại!")
            input("Nhấn Enter để tiếp tục...")
            continue

        print("\nChọn phương thức nhập link:")
        print("1. Nhập file txt (mỗi dòng 1 link)")
        print("2. Nhập link thủ công (cách nhau bằng dấu phẩy)")
        input_method = input("Nhập lựa chọn (1-2): ").strip()

        links = []
        if input_method == '1':
            file_path = input("Nhập đường dẫn file txt: ").strip()
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    links = file.readlines()
            except Exception as e:
                print(f"Lỗi khi đọc file: {e}")
                input("Nhấn Enter để tiếp tục...")
                continue
        elif input_method == '2':
            links_input = input("Nhập các link (cách nhau bằng dấu phẩy): ").strip()
            links = links_input.split(',')
        else:
            print("Lựa chọn không hợp lệ!")
            input("Nhấn Enter để tiếp tục...")
            continue

        process_links(links, choice)

        while True:
            continue_choice = input("\nBạn muốn tiếp tục sử dụng công cụ? (y/n): ").strip().lower()
            if continue_choice in ['y', 'n']:
                if continue_choice == 'n':
                    print("Cảm ơn bạn đã sử dụng công cụ!")
                    return
                break
            print("Vui lòng nhập 'y' hoặc 'n'!")
            input("Nhấn Enter để tiếp tục...")

if __name__ == "__main__":
    main_menu()