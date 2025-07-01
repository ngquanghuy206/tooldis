import requests
import json

print("Admin: Nguyễn Quang Huy")
print("Cảnh Báo: Hàng Share Không Bán là Được")

# Nhập username GitHub
username = input("Nhập username GitHub: ")

# Tạo URL API
api_url = f"https://keyherlyswar.x10.mx/Apidocs/getinfogithub.php?username={username}"

try:
    # Gửi yêu cầu đến API
    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()

    # In thông tin
    print("Thông tin người dùng GitHub:")
    print(json.dumps(data, indent=2, ensure_ascii=False))

except requests.RequestException as e:
    print(f"Lỗi khi gọi API: {e}")