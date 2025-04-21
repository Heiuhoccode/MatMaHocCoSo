from Crypto.Cipher import DES
import wave
import os
from PIL import Image
import random
import string
class DES_Cipher:
    def __init__(self, key):
        if len(key) != 8:
            raise ValueError("Key must be exactly 8 bytes long.")
        self.key = key
        self.cipher = DES.new(self.key, DES.MODE_ECB)

    def pad(self, data):
        pad_len = 8 - (len(data) % 8)
        return data + bytes([pad_len] * pad_len)

    def unpad(self, data):
        return data[:-data[-1]]

    def encrypt(self, data):
        padded_data = self.pad(data)
        return self.cipher.encrypt(padded_data)

    def decrypt(self, data):
        return self.unpad(self.cipher.decrypt(data))

# Đọc file và chuyển thành nhị phân
def file_to_binary(file_path):
    with open(file_path, 'rb') as f:
        return f.read()

# Lưu nhị phân vào file
def binary_to_file(binary_data, output_path):
    with open(output_path, 'wb') as f:
        f.write(binary_data)

# Xử lý file WAV
def encrypt_wav(input_wav, output_wav, cipher):
    with wave.open(input_wav, 'rb') as wav:
        params = wav.getparams()
        frames = wav.readframes(wav.getnframes())

    encrypted_data = cipher.encrypt(frames)
    with wave.open(output_wav, 'wb') as wav:
        wav.setparams(params)
        wav.writeframes(encrypted_data)

    print(f"Đã mã hóa WAV: {input_wav} -> {output_wav}")

def decrypt_wav(input_wav, output_wav, cipher):
    with wave.open(input_wav, 'rb') as wav:
        params = wav.getparams()
        frames = wav.readframes(wav.getnframes())

    decrypted_data = cipher.decrypt(frames)
    with wave.open(output_wav, 'wb') as wav:
        wav.setparams(params)
        wav.writeframes(decrypted_data)

    print(f"Đã giải mã WAV: {input_wav} -> {output_wav}")

# Xử lý file ảnh
def encrypt_image(input_image, output_image, cipher):
    img_data = file_to_binary(input_image)
    encrypted_data = cipher.encrypt(img_data)
    binary_to_file(encrypted_data, output_image)
    print(f"Đã mã hóa ảnh: {input_image} -> {output_image}")

def decrypt_image(input_image, output_image, cipher):
    img_data = file_to_binary(input_image)
    decrypted_data = cipher.decrypt(img_data)
    binary_to_file(decrypted_data, output_image)
    print(f"Đã giải mã ảnh: {input_image} -> {output_image}")

# Xử lý file văn bản
def encrypt_text(input_text, output_text, cipher):
    text_data = file_to_binary(input_text)
    encrypted_data = cipher.encrypt(text_data)
    binary_to_file(encrypted_data, output_text)
    print(f"Đã mã hóa văn bản: {input_text} -> {output_text}")

def decrypt_text(input_text, output_text, cipher):
    text_data = file_to_binary(input_text)
    decrypted_data = cipher.decrypt(text_data)
    binary_to_file(decrypted_data, output_text)
    print(f"Đã giải mã văn bản: {input_text} -> {output_text}")

# Chạy DES với nhiều loại file 

# key = b"12345678"  # Khóa DES phải có độ dài 8 byte
key = ''.join(random.choices(string.ascii_letters + string.digits, k=8)).encode('utf-8')
cipher = DES_Cipher(key)

# Xử lý file âm thanh WAV
encrypt_wav("HappyBirthday.wav", "encrypted.wav", cipher)
decrypt_wav("encrypted.wav", "decrypted.wav", cipher)

# Xử lý file ảnh PNG
encrypt_image("input.png", "encrypted.png", cipher)
decrypt_image("encrypted.png", "decrypted.png", cipher)

# Xử lý file văn bản TXT
encrypt_text("input.txt", "encrypted.txt", cipher)
decrypt_text("encrypted.txt", "decrypted.txt", cipher)
