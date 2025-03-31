import binascii

# Nhập khóa từ người dùng (16 ký tự hex)
user_input = input("Nhập khóa DES (16 ký tự hex): ").strip()

# Kiểm tra độ dài và chuyển đổi sang bytes
if len(user_input) != 16 or not all(c in "0123456789abcdefABCDEF" for c in user_input):
    print("❌ Lỗi: Khóa phải có đúng 16 ký tự hex!")
    exit()

true_key = bytes.fromhex(user_input)  # Chuyển đổi chuỗi hex sang bytes

print("✅ Khóa đã nhập:", true_key.hex())  # In lại để kiểm tra
