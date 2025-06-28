import os
import requests

def is_image_file(filename):
    return filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))

def upload_image_catbox(filepath):
    url = "https://catbox.moe/user/api.php"
    with open(filepath, 'rb') as f:
        files = {
            'reqtype': (None, 'fileupload'),
            'fileToUpload': (os.path.basename(filepath), f)
        }
        response = requests.post(url, files=files)
        return response.text if response.status_code == 200 else None

def main():
    folder = input("📁 Nhập đường dẫn thư mục chứa ảnh: ").strip()

    if not os.path.exists(folder):
        print("❌ Thư mục không tồn tại.")
        return

    image_files = [f for f in os.listdir(folder) if is_image_file(f)]
    if not image_files:
        print("❌ Không có ảnh trong thư mục.")
        return

    with open("link.txt", "w", encoding="utf-8") as f_out:
        for img_name in image_files:
            path = os.path.join(folder, img_name)
            print(f"⬆️ Đang upload: {img_name}...")
            link = upload_image_catbox(path)

            if link and "catbox" in link:
                print(f"✅ {img_name} → {link}")
                f_out.write(f"{img_name} → {link}\n")
            else:
                print(f"❌ Lỗi khi upload {img_name}")

    print("\n✅ Tất cả link đã lưu vào link.txt")

if __name__ == "__main__":
    main()