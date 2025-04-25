#Các thông tin đã biết:
#1 phần của key
#Bản mã hóa
#Định dạng của bản rõ

from Crypto.Cipher import DES
from itertools import product
from binascii import b2a_uu
from gc import collect
from re import search

if __name__ == "__main__":
    for keyGen in product(range(256), repeat=2):
        try:
            key = bytearray(
                (keyGen[0], 123, keyGen[1], 238, 174, 193, 130, 51)
            )
            print("Try key = ", key.hex())
            cipher = DES.new(key, DES.MODE_ECB)
            plaintext = cipher.decrypt(bytes.fromhex("bae64ae54e2447632089c81790c95dd9"))
            match = search("[A-Z]{1}[0-9]{2}[A-Z]{4}[0-9]{3}", plaintext.decode())

            if match:
                with open("plaintext", "w") as f:
                    f.write(f"Key: {key.hex()}\nPlaintext:{match.group()}\n")
                print("Final. Collected key")
                exit()
        except Exception as e:
            pass
        finally:
            collect()