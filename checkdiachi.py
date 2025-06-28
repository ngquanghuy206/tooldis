import requests
import colorama
from colorama import Fore, Style

def get_ip_location(ip_address):
    response = requests.get(f'http://ip-api.com/json/{ip_address}')
    data = response.json()
    return data

def main():
    print(f"{Fore.GREEN}Get victim's ip location{Style.RESET_ALL}")
    ip_address = input(f"{Fore.CYAN}Nhập Địa Chỉ Ip: {Style.RESET_ALL}")
    location_data = get_ip_location(ip_address)
    print(f"{Fore.YELLOW}Location Data:{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}IP Address:{Style.RESET_ALL} {location_data['query']}")
    print(f"{Fore.MAGENTA}Country:{Style.RESET_ALL} {location_data['country']}")
    print(f"{Fore.MAGENTA}City:{Style.RESET_ALL} {location_data['city']}")
    print(f"{Fore.MAGENTA}Region:{Style.RESET_ALL} {location_data['regionName']}")
    print(f"{Fore.MAGENTA}ISP:{Style.RESET_ALL} {location_data['isp']}")
    print(f"{Fore.MAGENTA}Latitude:{Style.RESET_ALL} {location_data['lat']}")
    print(f"{Fore.MAGENTA}Longitude:{Style.RESET_ALL} {location_data['lon']}")
    print(f"{Fore.MAGENTA}Timezone:{Style.RESET_ALL} {location_data['timezone']}")
    print(f"{Fore.MAGENTA}Organization:{Style.RESET_ALL} {location_data['org']}")

if __name__ == "__main__":
    colorama.init()
    main()