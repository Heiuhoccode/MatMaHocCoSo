import wave
import os
import random

class A51:
    def __init__(self, key, frame_number):
        """
        Initializes the A5/1 cipher with the given key and frame number.

        Args:
            key (str): The 64-bit key as a binary string.
            frame_number (str): The 22-bit frame number as a binary string.
        """
        if len(key) != 64 or any(c not in '01' for c in key):
            raise ValueError("Key must be a 64-bit binary string")
        if len(frame_number) != 22 or any(c not in '01' for c in frame_number):
            raise ValueError("Frame number must be a 22-bit binary string")

        self.key = [int(bit) for bit in key]
        self.frame_number = [int(bit) for bit in frame_number]

        # Initialize registers
        self.r1 = [0] * 19  # 19 bits
        self.r2 = [0] * 22  # 22 bits
        self.r3 = [0] * 23  # 23 bits

        self._initialize_registers()

    def _clock_register(self, register, taps, feedback_bits):
        """
        Clocks a register based on the given taps and feedback bits.

        Args:
            register (list): The register to clock.
            taps (list): The tap positions (indices) for majority function.
            feedback_bits (list): The tap positions (indices) for feedback calculation.

        Returns:
            int: The output bit.
        """
        majority = self._majority([register[i] for i in taps])
        if register[taps[0]] == majority:
            feedback = 0
            for bit_index in feedback_bits:
                feedback ^= register[bit_index]
            new_bit = feedback
            register[:] = [new_bit] + register[:-1]  # Shift with new bit
        return register[-1]

    def _majority(self, bits):
        """Calculates the majority bit."""
        return 1 if sum(bits) >= len(bits) / 2 else 0

    def _initialize_registers(self):
        """Initializes the registers with the key and frame number."""

        # 1. Load key into registers
        self.r1 = [int(bit) for bit in self.key[:19]]
        self.r2 = [int(bit) for bit in self.key[19:19 + 22]]
        self.r3 = [int(bit) for bit in self.key[19 + 22:]]

        # 2. Mix key bits into registers
        for i in range(64):
            self._clock_registers_all()

        # 3. Mix frame number into registers
        for i in range(22):
            feedback = self.frame_number[i] ^ self.r1[18] ^ self.r2[21] ^ self.r3[22]
            self.r1[:] = [feedback] + self.r1[:-1]
            self.r2[:] = [feedback] + self.r2[:-1]
            self.r3[:] = [feedback] + self.r3[:-1]
            self._clock_registers_all()

    def _clock_registers_all(self):
        """Clocks all three registers based on the majority function."""

        majority = self._majority([self.r1[8], self.r2[10], self.r3[10]])
        if self.r1[8] == majority:
            feedback = self.r1[13] ^ self.r1[16] ^ self.r1[17] ^ self.r1[18]
            self.r1[:] = [feedback] + self.r1[:-1]
        if self.r2[10] == majority:
            feedback = self.r2[20] ^ self.r2[21]
            self.r2[:] = [feedback] + self.r2[:-1]
        if self.r3[10] == majority:
            feedback = self.r3[20] ^ self.r3[21] ^ self.r3[22]
            self.r3[:] = [feedback] + self.r3[:-1]

    def generate_keystream(self, length):
        """
        Generates the keystream of the specified length.

        Args:
            length (int): The length of the keystream to generate (in bits).

        Returns:
            list: The generated keystream as a list of integers (0 or 1).
        """
        keystream = []
        for _ in range(length):
            self._clock_registers_all()
            keystream.append(self.r1[18] ^ self.r2[21] ^ self.r3[22])
        return keystream

    def encrypt_decrypt(self, data):
        """
        Encrypts or decrypts the given binary data.

        Args:
            data (list): The binary data to encrypt/decrypt (list of integers 0 or 1).

        Returns:
            list: The encrypted/decrypted data.
        """
        keystream = self.generate_keystream(len(data))
        return [bit ^ keystream[i] for i, bit in enumerate(data)]


# Utility functions (similar to your original code)
def wav_to_binary(input_wav):
    with wave.open(input_wav, 'rb') as wav:
        frames = wav.readframes(wav.getnframes())
        binary_data = ''.join(format(byte, '08b') for byte in frames)
    return binary_data

def binary_to_wav(binary_data, output_wav, params):
    byte_data = bytearray(int(binary_data[i:i + 8], 2) for i in range(0, len(binary_data), 8))
    with wave.open(output_wav, 'wb') as wav:
        wav.setparams(params)
        wav.writeframes(byte_data)

def save_binary_file(binary_data, output_file):
    with open(output_file, "w") as f:
        f.write(binary_data)

def encrypt_wav(input_wav, output_wav, bin_file, cipher):
    with wave.open(input_wav, 'rb') as wav:
        params = wav.getparams()
    binary_data = [int(b) for b in wav_to_binary(input_wav)]
    encrypted_data = cipher.encrypt_decrypt(binary_data)
    save_binary_file(''.join(map(str, encrypted_data)), bin_file)
    binary_to_wav(''.join(map(str, encrypted_data)), output_wav, params)
    print(f"Encrypt WAV: {input_wav} -> {output_wav} ({bin_file})")

def decrypt_wav(input_wav, output_wav, bin_file, cipher):
    with wave.open(input_wav, 'rb') as wav:
        params = wav.getparams()
    binary_data = [int(b) for b in wav_to_binary(input_wav)]
    decrypted_data = cipher.encrypt_decrypt(binary_data)
    save_binary_file(''.join(map(str, decrypted_data)), bin_file)
    binary_to_wav(''.join(map(str, decrypted_data)), output_wav, params)
    print(f"Decrypt WAV: {input_wav} -> {output_wav} ({bin_file})")

if __name__ == "__main__":
    key_length = 64
    key_bin = ''.join(random.choice(['0', '1']) for _ in range(key_length))
    frame_number_bin = ''.join(random.choice(['0', '1']) for _ in range(22))

    cipher = A51(key_bin, frame_number_bin)

    input_wav = r"G:\Nam3_Ki2\Mật mã học\MatMaHocCoSo\ThuatToanMaHoa\A51\scifi-ping-86790.wav"
    encrypted_wav = "encrypted.wav"
    decrypted_wav = "decrypted.wav"
    encrypted_bin = "encrypted.bin"
    decrypted_bin = "decrypted.bin"

    print()
    encrypt_wav(input_wav, encrypted_wav, encrypted_bin, cipher)
    print("Encrypted WAV:", os.path.abspath(encrypted_wav))
    print("Encrypted BIN:", os.path.abspath(encrypted_bin))
    print()

    cipher = A51(key_bin, frame_number_bin)  # Re-initialize for decryption
    decrypt_wav(encrypted_wav, decrypted_wav, decrypted_bin, cipher)
    print("Decrypted WAV:", os.path.abspath(decrypted_wav))
    print("Decrypted BIN:", os.path.abspath(decrypted_bin))