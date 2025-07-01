import requests
import json

print("Admin: Nguyễn Quang Huy")
print("Cảnh Báo: Hàng Share Không Bán là Được")

# Tạo URL API
api_url = "https://keyherlyswar.x10.mx/Apidocs/demngay.php"

try:
    # Gửi yêu cầu đến API
    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()

    # In danh sách ngày lễ
    print("Thời gian đếm ngược đến các ngày lễ:")
    print(json.dumps(data, indent=2, ensure_ascii=False))

except requests.RequestException as e:
    print(f"Lỗi khi gọi API: {e}")