def rc4_encrypt_decrypt(key, data):
    """
    Encrypts or decrypts data using the RC4 algorithm.

    Args:
        key (bytes): The encryption key (1 to 256 bytes).
        data (bytes): The data to encrypt or decrypt.

    Returns:
        bytes: The encrypted or decrypted data.
    """

    S = list(range(256))
    T = []
    key_length = len(key)

    # Key Scheduling Algorithm (KSA)
    for i in range(256):
        T.append(key[i % key_length])

    j = 0
    for i in range(256):
        j = (j + S[i] + T[i]) % 256
        S[i], S[j] = S[j], S[i]  # Swap

    # Pseudo-Random Generation Algorithm (PRGA)
    i = 0
    j = 0
    result = bytearray()

    for char in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]  # Swap
        t = (S[i] + S[j]) % 256
        k = S[t]
        result.append(char ^ k)

    return bytes(result)


if __name__ == '__main__':
    key = b'SecretKey'  # Key must be bytes
    plaintext = b'This is a secret message.'  # Data must be bytes

    ciphertext = rc4_encrypt_decrypt(key, plaintext)
    print(f"Plaintext: {plaintext}")
    print(f"Ciphertext: {ciphertext}")

    decrypted_text = rc4_encrypt_decrypt(key, ciphertext)  # Decrypting with the same key
    print(f"Decrypted text: {decrypted_text}")