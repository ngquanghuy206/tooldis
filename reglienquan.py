import requests
import json

print("Admin: Nguyễn Quang Huy")
print("Cảnh Báo: Hàng Share Không Bán là Được")

# Hỏi số lượng tài khoản
num_accounts = int(input("Bạn muốn đăng ký bao nhiêu tài khoản Liên Quân? "))

# Tạo URL API
api_url = "https://keyherlyswar.x10.mx/Apidocs/reglq.php"

try:
    for _ in range(num_accounts):
        # Gửi yêu cầu đến API
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        # Kiểm tra trạng thái
        if data.get("status"):
            for account in data.get("result"):
                print("Tài khoản Liên Quân:")
                print(f"Account: {account['account']}")
                print(f"Password: {account['password']}")
        else:
            print("Lỗi: Không thể đăng ký tài khoản.")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        print("-" * 50)

except requests.RequestException as e:
    print(f"Lỗi khi gọi API: {e}")