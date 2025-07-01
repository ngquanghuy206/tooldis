import requests
import json

print("Admin: Nguyễn Quang Huy")
print("Cảnh Báo: Hàng Share Không Bán là Được")

# Nhập UID Facebook
uid = input("Nhập Link Facebook: ")

# Tạo URL API (giả định dùng cùng API với Tool 11 do lỗi URL)
api_url = f"https://keyherlyswar.x10.mx/Apidocs/getuidfb.php?link={uid}"

try:
    # Gửi yêu cầu đến API
    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()

    # Kiểm tra trạng thái
    if data.get("status") == "success":
        print("UID Facebook:", data.get("uid"))
    else:
        print("Lỗi: Không thể lấy UID.")
        print(json.dumps(data, indent=2, ensure_ascii=False))

except requests.RequestException as e:
    print(f"Lỗi khi gọi API: {e}")