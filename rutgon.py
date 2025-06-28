import requests
import os

banner = """
╔═╗─╔╗───╔═══╗────────────╔╗─╔╗
║║╚╗║║───║╔═╗║────────────║║─║║
║╔╗╚╝╠══╗║║─║╠╗╔╦══╦═╗╔══╗║╚═╝╠╗╔╦╗─╔╗
║║╚╗║║╔╗║║║─║║║║║╔╗║╔╗╣╔╗║║╔═╗║║║║║─║║
║║─║║║╚╝║║╚═╝║╚╝║╔╗║║║║╚╝║║║─║║╚╝║╚═╝║
╚╝─╚═╩═╗║╚══╗╠══╩╝╚╩╝╚╩═╗║╚╝─╚╩══╩═╗╔╝
─────╔═╝║───╚╝────────╔═╝║───────╔═╝║
─────╚══╝─────────────╚══╝───────╚══╝
🔰 Tool Rút Gọn Link | Dev by Quang Huy
📘 Facebook: facebook.com/share/1CJkDWUGBY/
📱 Zalo: 0904562214
📧 Gmail: ngquanghuy3027@gmail.com
────────────────────────────────────────────────────────────
"""
os.system('cls' if os.name == 'nt' else 'clear')
print(banner)


print("Chọn dịch vụ rút gọn:")
print("1. Link4m")
print("2. Yeumoney")
choice = input("Nhập lựa chọn (1 hoặc 2): ").strip()

if choice == '1':
    token = input("🔑 Nhập token link4m của bạn: ").strip()
    def shorten(url):
        try:
            res = requests.get(f'https://link4m.co/api-shorten/v2?api={token}&url={url}').json()
            return res.get('shortenedUrl') if res.get('status') != 'error' else "Lỗi: " + res.get('message')
        except:
            return "Lỗi kết nối"
elif choice == '2':
    token = input("🔑 Nhập token yeumoney của bạn: ").strip()
    def shorten(url):
        try:
            api_url = f"https://yeumoney.com/QL_api.php?token={token}&format=text&url={url}"
            response = requests.get(api_url)
            return response.text.strip() if response.status_code == 200 else "Lỗi khi rút gọn"
        except:
            return "Lỗi kết nối"
else:
    print("❌ Lựa chọn không hợp lệ.")
    exit()


print("\nChọn cách nhập link:")
print("1. Nhập từ file .txt (mỗi dòng 1 link)")
print("2. Nhập thủ công (nhiều link, cách nhau bằng dấu ,)")
link_input_type = input("Nhập lựa chọn (1 hoặc 2): ").strip()

links = []

if link_input_type == '1':
    file_path = input("📄 Nhập đường dẫn file .txt: ").strip()
    if not os.path.isfile(file_path):
        print("❌ Không tìm thấy file.")
        exit()
    with open(file_path, 'r') as f:
        links = [line.strip() for line in f if line.strip()]
elif link_input_type == '2':
    input_links = input("🔗 Nhập các link (cách nhau bằng dấu ,): ").strip()
    links = [link.strip() for link in input_links.split(',') if link.strip()]
else:
    print("❌ Lựa chọn không hợp lệ.")
    exit()


print("\n📥 Kết quả rút gọn:")
for link in links:
    result = shorten(link)
    print(f"- {result}")