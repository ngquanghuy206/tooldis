import requests
import os

print("Admin: Nguyễn Quang Huy")
print("Cảnh Báo: Hàng Share Không Bán là Được")

# Nhập URL website
website_url = input("Nhập URL website cần chụp: ")

# Tạo URL API
api_url = f"https://keyherlyswar.x10.mx/Apidocs/cap.php?url={website_url}"

try:
    # Gửi yêu cầu đến API
    response = requests.get(api_url, stream=True)
    response.raise_for_status()

    # Kiểm tra nếu phản hồi là ảnh
    if 'image' in response.headers.get('content-type', '').lower():
        # Hỏi tải ảnh
        download = input("Bạn có muốn tải ảnh chụp website về máy không? (y/n): ").lower()
        if download == 'y':
            screenshot_name = "website_screenshot.jpg"
            with open(screenshot_name, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"Ảnh chụp website đã được tải về: {screenshot_name}")
        else:
            print("Không tải ảnh chụp website.")
    else:
        print("Lỗi: Phản hồi không phải là ảnh.")
        print(response.text)

except requests.RequestException as e:
    print(f"Lỗi khi gọi API: {e}")