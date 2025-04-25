from Crypto.Cipher import AES
import base64
import hashlib

# ===== HÀM CHUẨN HÓA KHÓA (16byte cho AES‑128) =====
def get_aes_key_from_input(user_key: str) -> bytes:
    # Dùng SHA‑256 → 32byte, lấy 16byte đầu
    return hashlib.sha256(user_key.encode()).digest()[:16]

# ===== HÀM PAD / UNPAD PKCS#7 =====
def pkcs7_pad(data: bytes, block_size: int = 16) -> bytes:
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len]) * pad_len

def pkcs7_unpad(padded: bytes) -> bytes:
    pad_len = padded[-1]
    if not 1 <= pad_len <= 16:
        raise ValueError("Sai padding")
    return padded[:-pad_len]

# ===== NHẬP TỪ NGƯỜI DÙNG =====
plaintext_input = input("Nhập plaintext: ")
key_input       = input("Nhập key (dưới dạng chuỗi): ")

# ===== XỬ LÝ =====
plaintext = plaintext_input.encode()
key       = get_aes_key_from_input(key_input)

# ===== MÃ HÓA (AES/ECB) =====
cipher     = AES.new(key, AES.MODE_ECB)
ciphertext = cipher.encrypt(pkcs7_pad(plaintext))

# ===== HIỂN THỊ KẾT QUẢ =====
# hiện thị theo hệ thập lục phân
print("\n--- DỮ LIỆU ĐÃ MÃ HÓA ---")
print("---      AES/ECB      ---")
print("Ciphertext:", ciphertext.hex())
print("Key       :", key.hex())

# ===== GIẢI MÃ =====
cipher_dec       = AES.new(key, AES.MODE_ECB)
decrypted_padded = cipher_dec.decrypt(ciphertext)

try:
    decrypted = pkcs7_unpad(decrypted_padded).decode()
    print("\n--- DỮ LIỆU SAU GIẢI MÃ ---")
    print("Đã giải mã:", decrypted)
except (ValueError, UnicodeDecodeError):
    print("Giải mã thất bại hoặc dữ liệu đã bị chỉnh sửa!")
