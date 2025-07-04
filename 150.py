import asyncio
import aiohttp
import time
import os
import sys
from colorama import Fore, Style, init


init(autoreset=True)

def dzi_clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

BANNER = f"""
{Fore.LIGHTMAGENTA_EX + Style.BRIGHT}═════════════════════════════════════════════════════
{Fore.LIGHTBLUE_EX}    ██████╗ ███████╗██╗    ██╗  ██╗
{Fore.LIGHTBLUE_EX}    ██╔══██╗╚════██║██║    ╚██╗██╔╝
{Fore.LIGHTBLUE_EX}    ██║  ██║   ███╔╝██║     ╚███╔╝ 
{Fore.LIGHTBLUE_EX}    ██║  ██║  ██╔╝  ██║     ██╔██╗ 
{Fore.LIGHTBLUE_EX}    ██████╔╝ ███████╗██║    ██╔╝╚██╗
{Fore.LIGHTBLUE_EX}    ╚═════╝  ╚══════╝╚═╝    ╚═╝  ╚═╝
{Fore.LIGHTMAGENTA_EX}    ╚══════╝  TOOL SPAM DISCORD BY NG QUANG HUY
{Fore.LIGHTMAGENTA_EX + Style.BRIGHT}═════════════════════════════════════════════════════
"""

async def dzi_mem_spam(token, link, id_channel, content, n_spam, n_delay):
    token = str(token).strip()
    print(f"{Fore.LIGHTCYAN_EX}[INFO] Token: {token[:10]}... đang khởi động")

    header_data = {
        "Authorization": token,
    }
    message_data = {
        "content": content,
        "tts": False
    }

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False), headers=header_data) as ses:
        while True:
            try:
                print(f"{Fore.LIGHTBLUE_EX}[STATUS] Token {token[:10]}... đang hoạt động")
                for _ in range(n_spam):
                    try:
                        async with ses.post(
                            url=f"https://discord.com/api/v9/channels/{str(id_channel)}/messages",
                            data=message_data
                        ) as resp:
                            if 200 <= resp.status < 350:
                                print(f"{Fore.LIGHTGREEN_EX}[SUCCESS] Gửi tin nhắn thành công - Token: {token[:10]}...")
                            else:
                                print(f"{Fore.LIGHTRED_EX}[ERROR] Lỗi gửi tin nhắn - Status: {resp.status}")
                    except Exception as e:
                        print(f"{Fore.LIGHTRED_EX}[ERROR] Lỗi xảy ra: {str(e)[:50]}...")
            except Exception as e:
                print(f"{Fore.LIGHTRED_EX}[ERROR] Token {token[:10]}... gặp lỗi: {str(e)[:50]}...")
            finally:
                print(f"{Fore.LIGHTYELLOW_EX}[INFO] Token {token[:10]}... tạm dừng {n_delay} giây")
                await asyncio.sleep(n_delay)

async def dzi_action_pool(tokens, link, id_channel, content, n_spam, n_delay):
    print(f"{Fore.LIGHTMAGENTA_EX + Style.BRIGHT}═══════════════════ HỆ THỐNG KHỞI ĐỘNG ═══════════════════")
    tasks = [asyncio.create_task(dzi_mem_spam(token.strip(), link, id_channel, content, n_spam, n_delay)) for token in tokens]
    await asyncio.gather(*tasks)

def dzi_load_file(file_path, file_type="TOKEN"):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = f.read() if file_type == "CONTENT" else f.readlines()
            print(f"{Fore.LIGHTGREEN_EX}[SUCCESS] Đọc file {file_type.lower()} thành công: {file_path}")
            return data
    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}[ERROR] Lỗi đọc file {file_type.lower()}: {str(e)}")
        time.sleep(5)
        sys.exit(1)

if __name__ == '__main__':
    dzi_clear_screen()
    print(BANNER)
    print(f"{Fore.LIGHTCYAN_EX}Developed by Ng Quang Huy | Version 1.0.0")
    print(f"{Fore.LIGHTMAGENTA_EX + Style.BRIGHT}═════════════════════════════════════════════════════")

    LINK_CHANNEL = input(f"{Fore.LIGHTBLUE_EX}[INPUT] Nhập Link Channel: {Style.RESET_ALL}")
    ID_CHANNEL = input(f"{Fore.LIGHTBLUE_EX}[INPUT] Nhập ID Channel: {Style.RESET_ALL}")
    TXT_TOKEN = input(f"{Fore.LIGHTBLUE_EX}[INPUT] Nhập đường dẫn file Tokens.txt: {Style.RESET_ALL}")
    TXT_CONTENT = input(f"{Fore.LIGHTBLUE_EX}[INPUT] Nhập đường dẫn file Content.txt: {Style.RESET_ALL}")
    try:
        N_SPAM = int(input(f"{Fore.LIGHTBLUE_EX}[INPUT] Nhập số lần spam mỗi token: {Style.RESET_ALL}"))
        N_DELAY = int(input(f"{Fore.LIGHTBLUE_EX}[INPUT] Nhập thời gian delay (giây): {Style.RESET_ALL}"))
    except ValueError:
        print(f"{Fore.LIGHTRED_EX}[ERROR] Vui lòng nhập số hợp lệ cho số lần spam và delay!")
        time.sleep(5)
        sys.exit(1)


    TOKENS = dzi_load_file(TXT_TOKEN, "TOKEN")
    CONTENT = dzi_load_file(TXT_CONTENT, "CONTENT").strip()

    print(f"{Fore.LIGHTMAGENTA_EX + Style.BRIGHT}═══════════════════ BẮT ĐẦU SPAM ═══════════════════")
    print(f"{Fore.LIGHTCYAN_EX}[CONFIG] Channel ID: {ID_CHANNEL}")
    print(f"{Fore.LIGHTCYAN_EX}[CONFIG] Số lần spam mỗi token: {N_SPAM}")
    print(f"{Fore.LIGHTCYAN_EX}[CONFIG] Delay: {N_DELAY} giây")
    print(f"{Fore.LIGHTCYAN_EX}[CONFIG] Tổng số token: {len(TOKENS)}")
    print(f"{Fore.LIGHTMAGENTA_EX + Style.BRIGHT}═════════════════════════════════════════════════════")


    while True:
        try:
            asyncio.run(dzi_action_pool(TOKENS, LINK_CHANNEL, ID_CHANNEL, CONTENT, N_SPAM, N_DELAY))
        except (Exception, SystemError) as e:
            print(f"{Fore.LIGHTRED_EX}[ERROR] Hệ thống gặp sự cố: {str(e)[:50]}...")
            print(f"{Fore.LIGHTYELLOW_EX}[INFO] Thử lại sau 5 giây...")
            time.sleep(5)