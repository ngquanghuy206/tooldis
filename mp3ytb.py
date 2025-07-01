import requests
import json
import os

print("Admin: Nguyễn Quang Huy")
print("Cảnh Báo: Hàng Share Không Bán là Được")

# Nhập URL YouTube
youtube_url = input("Nhập URL YouTube: ")

# Tạo URL API
api_url = f"https://keyherlyswar.x10.mx/Apidocs/ytmp3.php?url={youtube_url}"

try:
    # Gửi yêu cầu đến API
    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()

    # Kiểm tra trạng thái
    if data.get("status") == "ok":
        mp3_url = data.get("link")
        title = data.get("title", "youtube_audio")
        print("Thông tin bài nhạc:")
        print(json.dumps(data, indent=2, ensure_ascii=False))

        # Hỏi tải MP3
        download = input("Bạn có muốn tải file MP3 về máy không? (y/n): ").lower()
        if download == 'y':
            mp3_response = requests.get(mp3_url, stream=True)
            mp3_response.raise_for_status()
            mp3_name = f"{title[:50]}.mp3".replace("/", "_").replace("\\", "_")
            with open(mp3_name, 'wb') as f:
                for chunk in mp3_response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"File MP3 đã được tải về: {mp3_name}")
        else:
            print("Không tải file MP3.")
    else:
        print("Lỗi: Không thể lấy link MP3.")
        print(json.dumps(data, indent=2, ensure_ascii=False))

except requests.RequestException as e:
    print(f"Lỗi khi gọi API: {e}")