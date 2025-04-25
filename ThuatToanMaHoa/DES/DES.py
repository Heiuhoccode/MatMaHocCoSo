from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
import base64
import hashlib
import textwrap

# ===== HÀM CHUẨN HÓA KHÓA (8 byte cho DES) =====
def get_des_key_from_input(user_key: str) -> bytes:
    """
    DES yêu cầu khoá đúng 8 byte.
    Ta băm bằng SHA‑1 rồi lấy 8 byte đầu.
    """
    hashed = hashlib.sha1(user_key.encode()).digest()
    return hashed[:8]   # 8byte → 56 bit hiệu dụng

# ===== HÀM ĐỆM (PAD) VÀ BỎ ĐỆM (UNPAD) PKCS#5 =====
def pkcs5_pad(data: bytes) -> bytes:
    pad_len = 8 - (len(data) % 8)
    return data + bytes([pad_len]) * pad_len

def pkcs5_unpad(padded: bytes) -> bytes:
    pad_len = padded[-1]
    if not 1 <= pad_len <= 8:
        raise ValueError("Sai padding")
    return padded[:-pad_len]

# ===== NHẬP TỪ NGƯỜI DÙNG =====
plaintext_input = input("Nhập plaintext: ")
key_input = input("Nhập key (chuỗi bất kỳ): ")

# ===== XỬ LÝ =====
plaintext = plaintext_input.encode()
key = get_des_key_from_input(key_input)

# ===== MÃ HÓA =====
cipher = DES.new(key, DES.MODE_ECB)
ciphertext = cipher.encrypt(pkcs5_pad(plaintext))

# ===== HIỂN THỊ KẾT QUẢ =====
print("\n--- DỮ LIỆU ĐÃ MÃ HÓA (DES/ECB) ---")
print("Ciphertext:", ciphertext.hex())
print("Key :", key.hex())

# ===== GIẢI MÃ =====
cipher_dec = DES.new(key, DES.MODE_ECB)
decrypted_padded = cipher_dec.decrypt(ciphertext)

try:
    decrypted = pkcs5_unpad(decrypted_padded).decode()
    print("\n--- DỮ LIỆU SAU GIẢI MÃ ---")
    print("Đã giải mã:", decrypted)
except (ValueError, UnicodeDecodeError):
    print("Giải mã thất bại hoặc dữ liệu đã bị chỉnh sửa!")
