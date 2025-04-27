import requests
from rc4 import rc4

# === Cấu hình ===
TARGET_URL = "http://127.0.0.1:5000"  # URL đến server Flask của bạn
KEY = "my_very_weak_key"
USERNAME = "admin"

# === Tạo cookie hợp lệ ===
ciphertext = rc4(KEY, USERNAME)
cookie_hex = ciphertext.encode('latin1').hex()

# === Gửi yêu cầu với cookie giả mạo ===
cookies = {'auth': cookie_hex}
response = requests.get(TARGET_URL, cookies=cookies)

# === In ra kết quả ===
print("===== PHẢN HỒI TỪ SERVER =====")
print(response.text)
