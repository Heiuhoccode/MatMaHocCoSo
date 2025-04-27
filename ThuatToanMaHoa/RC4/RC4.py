from Crypto.Cipher import ARC4
from Crypto.Random import get_random_bytes
import hashlib
import base64

# ===== HÀM CHUẨN HÓA KHÓA (cho RC4) =====
def get_rc4_key_from_input(user_key: str) -> bytes:
    """
    RC4 chấp nhận khóa từ 1 đến 256 byte.
    Ta băm bằng SHA-256 rồi lấy 16 byte (128 bit) để đảm bảo độ dài phù hợp.
    """
    hashed = hashlib.sha256(user_key.encode()).digest()
    return hashed[:16]  # Lấy 16 byte đầu

# ===== NHẬP TỪ NGƯỜI DÙNG =====
plaintext_input = input("Nhập plaintext: ")
key_input = input("Nhập key (chuỗi bất kỳ): ")

# ===== XỬ LÝ =====
plaintext = plaintext_input.encode()
key = get_rc4_key_from_input(key_input)

# ===== MÃ HÓA =====
cipher = ARC4.new(key)
# RC4 không cần padding vì là hệ mã luồng
ciphertext = cipher.encrypt(plaintext)

# ===== HIỂN THỊ KẾT QUẢ =====
print("\n--- DỮ LIỆU ĐÃ MÃ HÓA ---")
print("---      RC4      ---")
print("Ciphertext:", ciphertext.hex())
print("Key       :", key.hex())

# ===== GIẢI MÃ =====
cipher_dec = ARC4.new(key)
decrypted = cipher_dec.decrypt(ciphertext)

try:
    decrypted_text = decrypted.decode()
    print("\n--- DỮ LIỆU SAU GIẢI MÃ ---")
    print("Đã giải mã:", decrypted_text)
except UnicodeDecodeError:
    print("Giải mã thất bại hoặc dữ liệu đã bị chỉnh sửa!")