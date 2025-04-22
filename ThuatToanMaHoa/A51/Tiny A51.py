import random
import wave
import os


class TinyA51:
    def __init__(self, key_x, key_y, key_z):
        self.X = [int(b) for b in key_x]
        self.Y = [int(b) for b in key_y]
        self.Z = [int(b) for b in key_z]

    def get_majority(self, x, y, z):
        return 1 if (x + y + z) > 1 else 0

    def step(self):
        majority = self.get_majority(self.X[1], self.Y[3], self.Z[3])
        if self.X[1] == majority:
            new_x = self.X[2] ^ self.X[4] ^ self.X[5]
            self.X = [new_x] + self.X[:-1]
        if self.Y[3] == majority:
            new_y = self.Y[6] ^ self.Y[7]
            self.Y = [new_y] + self.Y[:-1]
        if self.Z[3] == majority:
            new_z = self.Z[2] ^ self.Z[7] ^ self.Z[8]
            self.Z = [new_z] + self.Z[:-1]

    def get_keystream(self, length):
        keystream = []
        for _ in range(length):
            self.step()
            keystream.append(self.X[5] ^ self.Y[7] ^ self.Z[8])
        return keystream

    def encrypt_decrypt(self, binary_data):
        keystream = self.get_keystream(len(binary_data))
        return [b ^ k for b, k in zip(binary_data, keystream)]


# Chuyển file WAV thành chuỗi nhị phân
def wav_to_binary(input_wav):
    with wave.open(input_wav, 'rb') as wav:
        frames = wav.readframes(wav.getnframes())
        binary_data = ''.join(format(byte, '08b') for byte in frames)
    return binary_data


# Lưu chuỗi nhị phân vào file
def save_binary_file(binary_data, output_file):
    with open(output_file, "w") as f:
        f.write(binary_data)


# Đọc file nhị phân từ file
def read_binary_file(input_file):
    with open(input_file, "r") as f:
        return f.read().strip()


# Chuyển chuỗi nhị phân về file WAV
def binary_to_wav(binary_data, output_wav, params):
    byte_data = bytearray(int(binary_data[i:i + 8], 2) for i in range(0, len(binary_data), 8))
    with wave.open(output_wav, 'wb') as wav:
        wav.setparams(params)
        wav.writeframes(byte_data)


# Mã hóa file WAV và lưu file nhị phân
def encrypt_wav(input_wav, output_wav, bin_file, cipher):
    with wave.open(input_wav, 'rb') as wav:
        params = wav.getparams()
    binary_data = [int(b) for b in wav_to_binary(input_wav)]
    encrypted_data = cipher.encrypt_decrypt(binary_data)

    # Lưu file nhị phân của quá trình mã hóa
    save_binary_file(''.join(map(str, encrypted_data)), bin_file)

    binary_to_wav(''.join(map(str, encrypted_data)), output_wav, params)
    print(f"Ma haa file {input_wav} -> {output_wav} ({bin_file})")


# Giải mã file WAV và lưu file nhị phân
def decrypt_wav(input_wav, output_wav, bin_file, cipher):
    with wave.open(input_wav, 'rb') as wav:
        params = wav.getparams()
    binary_data = [int(b) for b in wav_to_binary(input_wav)]
    decrypted_data = cipher.encrypt_decrypt(binary_data)

    # Lưu file nhị phân của quá trình giải mã
    save_binary_file(''.join(map(str, decrypted_data)), bin_file)

    binary_to_wav(''.join(map(str, decrypted_data)), output_wav, params)
    print(f"Giai ma file {input_wav} -> {output_wav} ({bin_file})")


# ----------- Chạy Tiny A5/1 với file WAV -----------
if __name__ == "__main__":
    key_x = "100101"
    key_y = "01001100"
    key_z = "100110000"

    cipher = TinyA51(key_x, key_y, key_z)

    input_wav = r"D:\VSCodePython\A5\A5\input.wav"  # Doc file am thanh goc .wav
    encrypted_wav = "encrypted.wav"
    decrypted_wav = "decrypted.wav"
    encrypted_bin = "encrypted.bin"  # Lưu file nhị phân mã hóa
    decrypted_bin = "decrypted.bin"  # Lưu file nhị phân giải mã

    print()
    # Neu khong su dung chuc nang ma hoa co the ghi chu!
    encrypt_wav(input_wav, encrypted_wav, encrypted_bin, cipher)
    # Vi tri cua file ma hoa
    print("File ma haa:", os.path.abspath(encrypted_wav))
    print("File nhi phan ma haa:", os.path.abspath(encrypted_bin))
    print()

    cipher = TinyA51(key_x, key_y, key_z)  # Reset lại bộ sinh khóa
    # Neu khong su dung chuc nang giai ma co the ghi chu!
    decrypt_wav(encrypted_wav, decrypted_wav, decrypted_bin, cipher)
    # Vi tri cua file giai ma
    print("File giai ma:", os.path.abspath(decrypted_wav))
    print("File nhi phan giai ma:", os.path.abspath(decrypted_bin))
