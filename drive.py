import requests
import json
import os

print("Admin: Nguyễn Quang Huy")
print("Cảnh Báo: Hàng Share Không Bán là Được")

# Nhập link Google Drive
drive_url = input("Nhập link Google Drive: ")

# Tạo URL API
api_url = f"https://keyherlyswar.x10.mx/Apidocs/downdriver.php?link={drive_url}"

try:
    # Gửi yêu cầu đến API
    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()

    # Kiểm tra trạng thái
    if data.get("status") == "success":
        file_url = data.get("data")
        print("Link tải file:", file_url)

        # Hỏi người dùng có muốn tải file không
        download = input("Bạn có muốn tải file về máy không? (y/n): ").lower()
        if download == 'y':
            file_response = requests.get(file_url, stream=True)
            file_response.raise_for_status()
            # Lấy tên file từ URL hoặc đặt tên mặc định
            file_name = file_url.split("/")[-1] if "/" in file_url else "downloaded_file"
            with open(file_name, 'wb') as f:
                for chunk in file_response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"File đã được tải về: {file_name}")
        else:
            print("Không tải file.")
    else:
        print("Lỗi: Không thể lấy link tải.")
        print(json.dumps(data, indent=2, ensure_ascii=False))

except requests.RequestException as e:
    print(f"Lỗi khi gọi API: {e}")