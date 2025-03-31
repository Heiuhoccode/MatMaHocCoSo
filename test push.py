from Crypto.Cipher import DES
import itertools
import os
import binascii
from Crypto.Util.Padding import *


def encrypt_des(plaintext, key):
    cipher = DES.new(key, DES.MODE_ECB)
    return cipher.encrypt(pad(plaintext, DES.block_size))

def decrypt_des(ciphertext, key):
    cipher = DES.new(key, DES.MODE_ECB)
    return unpad(cipher.decrypt(ciphertext), DES.block_size)

# Giả sử ta biết một phần của plaintext
known_plaintext = b"HelloDES"
key_space = 2**22  # Giảm phạm vi thử nghiệm để tiết kiệm thời gian



# Nhập khóa từ người dùng (16 ký tự hex)
user_input = input("Nhập khóa DES (16 ký tự hex): ").strip()

# Kiểm tra độ dài và định dạng hợp lệ
if len(user_input) != 16 or not all(c in "0123456789abcdefABCDEF" for c in user_input):
    print("❌ Lỗi: Khóa phải có đúng 16 ký tự hex!")
    exit()

# Chuyển đổi từ hex sang bytes
true_key = bytes.fromhex(user_input)

# Hiển thị khóa đã nhập
print("✅ Khóa đã nhập:", true_key.hex())

# Mã hóa với khóa đã nhập
ciphertext = encrypt_des(known_plaintext, true_key)

# Hiển thị ciphertext
print("Ciphertext:", ciphertext.hex())


print("Thử tấn công brute-force...")
count=0
for i in range(key_space):
    brute_key = i.to_bytes(8, byteorder='big')  # Chuyển số thành khóa 8 byte
    try:
        decrypted = decrypt_des(ciphertext, brute_key)
        if decrypted == known_plaintext:
            print("🔑 Khóa tìm được:", brute_key.hex())
            break
        # print(brute_key.hex())
    except:
        continue
    count += 1
    if count % 1000 == 0:
        print(f"🔄 Đã thử {count} khóa...")  # In sau mỗi 10,000 lần thử
