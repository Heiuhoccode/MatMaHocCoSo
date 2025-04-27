
from Crypto.Cipher import AES
import binascii
import time
from Crypto.Random import get_random_bytes

# keey dùng để mã hóa (16 bytes)
key = get_random_bytes(16)
print("Khóa = ", key.hex())
# Secret information (<= 16 chars)
secretInfo = "Matmahoccoso1234"

cipher = AES.new(key, AES.MODE_ECB)

def encrypt(message): 
	return cipher.encrypt(message)

def oracle(target, display = False, see_oracle = False, timing = False):
	message = getPadding("data=" + target + secretInfo)
	message_encoded = message.encode()
	encrypted = encrypt(message_encoded)
	if display:
		if timing: time.sleep(.05)
		disp(message, target, encrypted, see_oracle)
	encrypted_decoded = byte_to_hex(encrypted)
	print("Ciphertext dạng hex:", encrypted_decoded, "\n")
	return encrypted 


# Padding
def getPadding(secret):
    pl = len(secret)
    mod = pl % 16
    if mod != 0:
        padding = 16 - mod
        secret += 'X' * padding
    return secret

def byte_to_hex(elt): return binascii.hexlify(elt)

def disp(message, target, encrypted, see_oracle):
	if see_oracle: print("\nThông điệp cần mã hóa: ", message)
	else: print("\nThông điệp cần mã hóa: ?")
	print("Target given: ", target)
	if see_oracle:
		print("Chia khối thông điệp", message[0:16], " ", message[16:32], " ", message[32:48], " ", message[48:64], " ", message[64:80], " ", message[80:96], " ")
		print("Chuỗi bí mật không biết:", secretInfo)
		print("\tMã hóa bằng AES-ECB.... \n\tkhóa =", key)
	else: print("Chia khối thông điệp", message[0:16], " ", message[16:32], " ", 16 * "?", " ", 16 * "?", " ", "?" * 16, " ", "?" *16, " ")
	print("Ciphertext dạng hex:", byte_to_hex(encrypted), "\n")
