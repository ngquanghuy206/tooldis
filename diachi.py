import requests
import json

print("Admin: Nguyễn Quang Huy")
print("Cảnh Báo: Hàng Share Không Bán là Được")

# Nhập địa chỉ cần tìm
address = input("Nhập địa chỉ cần tìm trên Google Maps: ")

# Tạo URL API
api_url = f"https://keyherlyswar.x10.mx/Apidocs/ggmap.php?text={address}"

try:
    # Gửi yêu cầu đến API
    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()

    # Kiểm tra trạng thái
    if data.get("status") == "OK":
        print("Thông tin địa chỉ:")
        print(json.dumps(data.get("candidates"), indent=2, ensure_ascii=False))
    else:
        print("Lỗi: Không thể tìm địa chỉ.")
        print(json.dumps(data, indent=2, ensure_ascii=False))

except requests.RequestException as e:
    print(f"Lỗi khi gọi API: {e}")