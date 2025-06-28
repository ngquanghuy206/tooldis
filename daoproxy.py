import requests
import os
import time
from datetime import datetime

def cls():
    linux = 'clear'
    windows = 'cls'
    os.system([linux,windows][os.name == 'nt'])

def welcome():
    print(fr"""

(`\ .-') /`   ('-.                                  _   .-')       ('-.        
`.( OO ),' _(  OO)                                ( '.( OO )_   _(  OO)       
,--./  .--.  (,------.,--.       .-----.  .-'),-----. ,--.   ,--.)(,------.      
|      |  |   |  .---'|  |.-')  '  .--./ ( OO'  .-.  '|   `.'   |  |  .---'      
|  |   |  |,  |  |    |  | OO ) |  |('-. /   |  | |  ||         |  |  |          
|  |.'.|  |_)(|  '--. |  |`-' |/_) |OO  )\_) |  |\|  ||  |'.'|  | (|  '--.       
|         |   |  .--'(|  '---.'||  |`-'|   \ |  | |  ||  |   |  |  |  .--'       
|   ,'.   |   |  `---.|      |(_'  '--'\    `'  '-'  '|  |   |  |  |  `---.      
'--'   '--'   `------'`------'   `-----'      `-----' `--'   `--'  `------'                                                    
                                                                                                                    """)
    print(fr"                              Tool Đào Proxy v1.0")
    print(fr"                              Coder by Ng Quang Huy")
    print(fr"                              Facebook: facebook.com/share/1CJkDWUGBY/")
    print(fr"                              Zalo: 0904562214")
    print(fr"                              Gmail: ngquanghuy3027@gmail.com")
    print(fr"                              Ngày giờ: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(fr"============================================================================")
    print(fr"[0] Thoát")
    print(fr"[1] Đào proxy cho Windows")
    print(fr"[2] Đào proxy cho Kali Linux, Parrot OS,...")

def bannerW():
    print(fr"""
    
██████╗ ██████╗  ██████╗ ██╗  ██╗██╗   ██╗████████╗ ██████╗  ██████╗ ██╗     
██╔══██╗██╔══██╗██╔═══██╗╚██╗██╔╝╚██╗ ██╔╝╚══██╔══╝██╔═══██╗██╔═══██╗██║     
██████╔╝██████╔╝██║   ██║ ╚███╔╝  ╚████╔╝    ██║   ██║   ██║██║   ██║██║     
██╔═══╝ ██╔══██╗██║   ██║ ██╔██╗   ╚██╔╝     ██║   ██║   ██║██║   ██║██║     
██║     ██║  ██║╚██████╔╝██╔╝ ██╗   ██║      ██║   ╚██████╔╝╚██████╔╝███████╗
╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝      ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝
                                                                                                                        """)
    print(fr"================================================================================")
    print("\n")
    print(fr"[0] Quay lại Menu")
    print(fr"[1] Proxy Socks5")
    print(fr"[2] Proxy Socks4")
    print(fr"[3] Proxy HTTP")
    print(fr"[4] Lấy tất cả Proxy: Socks5, Socks4 và HTTP")

def get_proxyW():
    cls()
    bannerW()
    you = int(input("\n >>>  "))
    path = os.getcwd()

    if you==1:
        filename = input("\nNhập tên file txt để lưu proxy (ví dụ: socks5.txt): ")
        url = 'https://openproxylist.xyz/socks5.txt'
        url_1 = 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=1250&country=all&simplified=true'
        a = requests.get(url, allow_redirects=True)
        b = requests.get(url_1, allow_redirects=True)
        with open(os.path.join(path, filename),'wb') as file1:
            file1.write(a.content)
            file1.write(b.content)
            time.sleep(1)
        line = open(os.path.join(path, filename))
        lines = line.readlines()
        line.close()
        for socks5 in lines:
            socks5 = socks5.strip()
            print(socks5)
        print("\n[+] Thành công!")
        print(f"\n---> File đã được lưu với tên {filename} trong thư mục hiện tại")

    elif you==2:
        filename = input("\nNhập tên file txt để lưu proxy (ví dụ: socks4.txt): ")
        url2 = 'https://openproxylist.xyz/socks4.txt'
        url_2 = 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=1250&country=all&simplified=true'
        a = requests.get(url2, allow_redirects=True)
        b = requests.get(url_2, allow_redirects=True)
        with open(os.path.join(path, filename),'wb') as file2:
            file2.write(a.content)
            file2.write(b.content)
            time.sleep(1)
        line2 = open(os.path.join(path, filename))
        lines2 = line2.readlines()
        line2.close()
        for socks4 in lines2:
            socks4 = socks4.strip()
            print(socks4)
        print("\n[+] Thành công!")
        print(f"\n---> File đã được lưu với tên {filename} trong thư mục hiện tại")

    elif you==3:
        filename = input("\nNhập tên file txt để lưu proxy (ví dụ: http.txt): ")
        url3 = 'https://openproxylist.xyz/http.txt'
        url_3 = 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=1250&country=all&simplified=true'
        a = requests.get(url3, allow_redirects=True)
        b = requests.get(url_3, allow_redirects=True)
        with open(os.path.join(path, filename),'wb') as file3:
            file3.write(a.content)
            file3.write(b.content)
            time.sleep(1)
        line3 = open(os.path.join(path, filename))
        lines3 = line3.readlines()
        line3.close()
        for http in lines3:
            http = http.strip()
            print(http)
        print("\n[+] Thành công!")
        print(f"\n---> File đã được lưu với tên {filename} trong thư mục hiện tại")

    elif you==4:
        filename = input("\nNhập tên file txt để lưu proxy (ví dụ: all_proxy.txt): ")
        url_socks5 = 'https://openproxylist.xyz/socks5.txt'
        url_socks5_1 = 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=1250&country=all&simplified=true'
        url_socks4 = 'https://openproxylist.xyz/socks4.txt'
        url_socks4_1 = 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=1250&country=all&simplified=true'
        url_http = 'https://openproxylist.xyz/http.txt'
        url_http_1 = 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=1250&country=all&simplified=true'
        all1 = requests.get(url_socks5, allow_redirects=True)
        all2 = requests.get(url_socks5_1, allow_redirects=True)
        all3 = requests.get(url_socks4, allow_redirects=True)
        all4 = requests.get(url_socks4_1, allow_redirects=True)
        all5 = requests.get(url_http, allow_redirects=True)
        all6 = requests.get(url_http_1, allow_redirects=True)
        with open(os.path.join(path, filename),'wb') as file4:
            file4.write(all1.content)
            file4.write(all2.content)
            file4.write(all3.content)
            file4.write(all4.content)
            file4.write(all5.content)
            file4.write(all6.content)
            time.sleep(1)
        line4 = open(os.path.join(path, filename))
        lines4 = line4.readlines()
        line4.close()
        for all_proxy in lines4:
            all_proxy = all_proxy.strip()
            print(all_proxy)
        print("\n[+] Thành công!")
        print(f"\n---> File đã được lưu với tên {filename} trong thư mục hiện tại")
    elif you == 0:
       select()
    else:
        print('LỖI!!!')

def get_proxyLinux():
    cls()
    bannerW()
    you = int(input("\n >>>  "))
    path = os.getcwd()

    if you==1:
        filename = input("\nNhập tên file txt để lưu proxy (ví dụ: socks5.txt): ")
        url = 'https://openproxylist.xyz/socks5.txt'
        url_1 = 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=1250&country=all&simplified=true'
        a = requests.get(url, allow_redirects=True)
        b = requests.get(url_1, allow_redirects=True)
        with open(os.path.join(path, filename),'wb') as file1:
            file1.write(a.content)
            file1.write(b.content)
            time.sleep(1)
        line = open(os.path.join(path, filename))
        lines = line.readlines()
        line.close()
        for socks5 in lines:
            socks5 = socks5.strip()
            print(socks5)
        print("\n[+] Thành công!")
        print(f"\n---> File đã được lưu với tên {filename} trong thư mục hiện tại")

    elif you==2:
        filename = input("\nNhập tên file txt để lưu proxy (ví dụ: socks4.txt): ")
        url2 = 'https://openproxylist.xyz/socks4.txt'
        url_2 = 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=1250&country=all&simplified=true'
        a = requests.get(url2, allow_redirects=True)
        b = requests.get(url_2, allow_redirects=True)
        with open(os.path.join(path, filename),'wb') as file2:
            file2.write(a.content)
            file2.write(b.content)
            time.sleep(1)
        line2 = open(os.path.join(path, filename))
        lines2 = line2.readlines()
        line2.close()
        for socks4 in lines2:
            socks4 = socks4.strip()
            print(socks4)
        print("\n[+] Thành công!")
        print(f"\n---> File đã được lưu với tên {filename} trong thư mục hiện tại")

    elif you==3:
        filename = input("\nNhập tên file txt để lưu proxy (ví dụ: http.txt): ")
        url3 = 'https://openproxylist.xyz/http.txt'
        url_3 = 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=1250&country=all&simplified=true'
        a = requests.get(url3, allow_redirects=True)
        b = requests.get(url_3, allow_redirects=True)
        with open(os.path.join(path, filename),'wb') as file3:
            file3.write(a.content)
            file3.write(b.content)
            time.sleep(1)
        line3 = open(os.path.join(path, filename))
        lines3 = line3.readlines()
        line3.close()
        for http in lines3:
            http = http.strip()
            print(http)
        print("\n[+] Thành công!")
        print(f"\n---> File đã được lưu với tên {filename} trong thư mục hiện tại")

    elif you==4:
        filename = input("\nNhập tên file txt để lưu proxy (ví dụ: all_proxy.txt): ")
        url_socks5 = 'https://openproxylist.xyz/socks5.txt'
        url_socks5_1 = 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=1250&country=all&simplified=true'
        url_socks4 = 'https://openproxylist.xyz/socks4.txt'
        url_socks4_1 = 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=1250&country=all&simplified=true'
        url_http = 'https://openproxylist.xyz/http.txt'
        url_http_1 = 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=1250&country=all&simplified=true'
        all1 = requests.get(url_socks5, allow_redirects=True)
        all2 = requests.get(url_socks5_1, allow_redirects=True)
        all3 = requests.get(url_socks4, allow_redirects=True)
        all4 = requests.get(url_socks4_1, allow_redirects=True)
        all5 = requests.get(url_http, allow_redirects=True)
        all6 = requests.get(url_http_1, allow_redirects=True)
        with open(os.path.join(path, filename),'wb') as file4:
            file4.write(all1.content)
            file4.write(all2.content)
            file4.write(all3.content)
            file4.write(all4.content)
            file4.write(all5.content)
            file4.write(all6.content)
            time.sleep(1)
        line4 = open(os.path.join(path, filename))
        lines4 = line4.readlines()
        line4.close()
        for all_proxy in lines4:
            all_proxy = all_proxy.strip()
            print(all_proxy)
        print("\n[+] Thành công!")
        print(f"\n---> File đã được lưu với tên {filename} trong thư mục hiện tại")
    elif you == 0:
       select()
    else:
        print('LỖI!!!')

def select():
    while True:
        cls()
        welcome()
        you = int(input("\n>>> "))
        if you==1:
            get_proxyW()
            exit()
        elif you==2:
            get_proxyLinux()
            exit()
        elif you == 0:
            print("\nHẹn gặp lại nhé!")
            break
        else:
            print("\nSai rồi, vui lòng chọn lại!")
select()