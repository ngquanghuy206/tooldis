import requests
import json
import os

print("Admin: Nguyễn Quang Huy")
print("Cảnh Báo: Hàng Share Không Bán là Được")

# Nhập URL Twitter
twitter_url = input("Nhập URL Twitter (X): ")

# Tạo URL API
api_url = f"https://keyherlyswar.x10.mx/Apidocs/twitterdl.php?url={twitter_url}"

try:
    # Gửi yêu cầu đến API
    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()

    # Kiểm tra trạng thái
    if data.get("status"):
        video_url = data.get("result", {}).get("video")
        print("Link video:", video_url)

        # Hỏi tải video
        download = input("Bạn có muốn tải video về máy không? (y/n): ").lower()
        if download == 'y':
            video_response = requests.get(video_url, stream=True)
            video_response.raise_for_status()
            video_name = "twitter_video.mp4"
            with open(video_name, 'wb') as f:
                for chunk in video_response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"Video đã được tải về: {video_name}")
        else:
            print("Không tải video.")
    else:
        print("Lỗi: Không thể lấy link video.")
        print(json.dumps(data, indent=2, ensure_ascii=False))

except requests.RequestException as e:
    print(f"Lỗi khi gọi API: {e}")