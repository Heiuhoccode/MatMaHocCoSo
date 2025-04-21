from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import hashlib

# ===== HÀM CHUẨN HÓA KHÓA =====
def get_aes_key_from_input(user_key):
    # Dùng SHA-256 để chuyển chuỗi nhập vào thành 32 byte (AES-256)
    hashed_key = hashlib.sha256(user_key.encode()).digest()
    return hashed_key[:16]  # Lấy 16 byte đầu để dùng AES-128

# ===== NHẬP TỪ NGƯỜI DÙNG =====
plaintext_input = input("Nhập plaintext: ")
key_input = input("Nhập key (dưới dạng chuỗi): ")

# ===== XỬ LÝ =====
plaintext = plaintext_input.encode()
key = get_aes_key_from_input(key_input)

# ===== MÃ HÓA =====
cipher = AES.new(key, AES.MODE_EAX)
ciphertext, tag = cipher.encrypt_and_digest(plaintext)
nonce = cipher.nonce

# ===== IN MÃ HÓA =====
print("\n--- DỮ LIỆU ĐÃ MÃ HÓA ---")
print("Ciphertext:", base64.b64encode(ciphertext).decode())
print("Key:", base64.b64encode(key).decode())
print("Nonce:", base64.b64encode(nonce).decode())
print("Tag:", base64.b64encode(tag).decode())

# ===== GIẢI MÃ =====
cipher_dec = AES.new(key, AES.MODE_EAX, nonce=nonce)
try:
    decrypted = cipher_dec.decrypt_and_verify(ciphertext, tag)
    print("\n--- DỮ LIỆU SAU GIẢI MÃ ---")
    print("Đã giải mã:", decrypted.decode())
except ValueError:
    print("Giải mã thất bại hoặc dữ liệu đã bị chỉnh sửa!")
