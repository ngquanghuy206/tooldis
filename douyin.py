import requests
import json

print("Admin: Nguyễn Quang Huy")
print("Cảnh Báo: Hàng Share Không Bán là Được")

# Nhập URL Douyin
douyin_url = input("Nhập URL Douyin: ")

# Tạo URL API
api_url = f"https://keyherlyswar.x10.mx/Apidocs/getinfodouyin.php?url={douyin_url}"

try:
    # Gửi yêu cầu đến API
    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()

    # Kiểm tra trạng thái
    if data.get("status_code") == 0:
        print("Thông tin người dùng Douyin:")
        print(json.dumps(data.get("user"), indent=2, ensure_ascii=False))
    else:
        print("Lỗi: Không thể lấy thông tin.")
        print(json.dumps(data, indent=2, ensure_ascii=False))

except requests.RequestException as e:
    print(f"Lỗi khi gọi API: {e}")