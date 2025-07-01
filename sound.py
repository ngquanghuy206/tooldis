import requests
import json
import os

print("Admin: Nguyễn Quang Huy")
print("Cảnh Báo: Hàng Share Không Bán là Được")

# Nhập URL SoundCloud
soundcloud_url = input("Nhập URL SoundCloud: ")

# Tạo URL API
api_url = f"https://keyherlyswar.x10.mx/Apidocs/scldl.php?url={soundcloud_url}"

try:
    # Gửi yêu cầu đến API
    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()

    # Kiểm tra trạng thái
    if data.get("status"):
        result = data.get("result")
        mp3_url = result.get("mp3")
        thumbnail_url = result.get("info", {}).get("thumbnail")
        title = result.get("info", {}).get("title", "soundcloud_track")
        print("Thông tin bài nhạc:")
        print(json.dumps(result.get("info"), indent=2, ensure_ascii=False))

        # Hỏi tải MP3
        if mp3_url:
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

        # Hỏi tải ảnh thumbnail
        if thumbnail_url:
            download = input("Bạn có muốn tải ảnh thumbnail về máy không? (y/n): ").lower()
            if download == 'y':
                thumb_response = requests.get(thumbnail_url, stream=True)
                thumb_response.raise_for_status()
                thumb_name = f"{title[:50]}_thumbnail.jpg".replace("/", "_").replace("\\", "_")
                with open(thumb_name, 'wb') as f:
                    for chunk in thumb_response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                print(f"Ảnh thumbnail đã được tải về: {thumb_name}")
            else:
                print("Không tải ảnh thumbnail.")
    else:
        print("Lỗi: Không thể lấy thông tin.")
        print(json.dumps(data, indent=2, ensure_ascii=False))

except requests.RequestException as e:
    print(f"Lỗi khi gọi API: {e}")