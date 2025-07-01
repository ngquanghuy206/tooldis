import requests
import os

print("Admin: Nguyễn Quang Huy")
print("Cảnh Báo: Hàng Share Không Bán là Được")

# Nhập UID Facebook
uid = input("Nhập UID Facebook: ")

# Tạo URL API
api_url = f"https://keyherlyswar.x10.mx/Apidocs/avtfb.php?uid={uid}"

try:
    # Gửi yêu cầu đến API
    response = requests.get(api_url, stream=True)
    response.raise_for_status()

    # Kiểm tra nếu phản hồi là ảnh
    if 'image' in response.headers.get('content-type', '').lower():
        # Hỏi tải ảnh
        download = input("Bạn có muốn tải ảnh đại diện về máy không? (y/n): ").lower()
        if download == 'y':
            avatar_name = f"facebook_avatar_{uid}.jpg"
            with open(avatar_name, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"Ảnh đại diện đã được tải về: {avatar_name}")
        else:
            print("Không tải ảnh đại diện.")
    else:
        print("Lỗi: Phản hồi không phải là ảnh.")
        print(response.text)

except requests.RequestException as e:
    print(f"Lỗi khi gọi API: {e}")