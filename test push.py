from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import os
import itertools, binascii

def encrypt_des(plaintext, key):
    cipher = DES.new(key, DES.MODE_ECB)
    return cipher.encrypt(pad(plaintext, DES.block_size))

def decrypt_des(ciphertext, key):
    cipher = DES.new(key, DES.MODE_ECB)
    return unpad(cipher.decrypt(ciphertext), DES.block_size)

def generate_padded_combinations(n):
    chars = "0123456789abcdef"
    for comb in itertools.product(chars, repeat=n):
        yield "".join(comb).zfill(16)

# Giả sử ta biết một phần của plaintext
known_plaintext = b"HelloDES"
key_space = 2**22  # Giảm phạm vi thử nghiệm
print("Tổng số khóa thử nghiệm:", key_space)

# Nhập khóa từ người dùng (16 ký tự hex)
user_input = input("Nhập khóa DES (16 ký tự hex): ").strip()

# Kiểm tra độ dài và chuyển đổi sang bytes
if len(user_input) != 16 or not all(c in "0123456789abcdefABCDEF" for c in user_input):
    print("❌ Lỗi: Khóa phải có đúng 16 ký tự hex!")
    exit()

print("✅ Khóa đã nhập:", user_input)  # In lại để kiểm tr

ciphertext = encrypt_des(known_plaintext, user_input.encode("utf-8"))

print("Thử tấn công brute-force...")

count = 0  # Bộ đếm số lần thử
for temp_key in generate_padded_combinations(2):
    print(temp_key)
    temp_key = temp_key.encode("utf-8")  # Chỉ lấy 8 byte cho DES
    # print(temp_key.hex())
    try:
        decrypted = decrypt_des(ciphertext, temp_key)
        if decrypted == known_plaintext:
            print("🔑 Khóa tìm được:", temp_key.hex())
            break
    except:
        pass  # Bỏ qua lỗi giải mã (nếu có)

    # count += 1
    # if count % 10000 == 0:
    #     print(f"🔄 Đã thử {count} khóa...")  # In sau mỗi 10,000 lần thử

print("🚀 Kết thúc brute-force.")
