import requests
import json

print("Admin: Nguyễn Quang Huy")
print("Cảnh Báo: Hàng Share Không Bán là Được")

# Nhập username Roblox
username = input("Nhập username Roblox: ")

# Tạo URL API
api_url = f"https://keyherlyswar.x10.mx/Apidocs/getinforoblox.php?username={username}"

try:
    # Gửi yêu cầu đến API
    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()

    # Kiểm tra trạng thái
    if data.get("status") == "success":
        print("Thông tin người dùng Roblox:")
        print(json.dumps(data.get("data"), indent=2, ensure_ascii=False))
    else:
        print("Lỗi: Không thể lấy thông tin.")
        print(json.dumps(data, indent=2, ensure_ascii=False))

except requests.RequestException as e:
    print(f"Lỗi khi gọi API: {e}")