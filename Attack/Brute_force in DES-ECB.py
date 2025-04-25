#Các thông tin đã biết:
#1 phần của key
#Bản mã hóa
#Định dạng của bản rõ
import os.path

from Crypto.Cipher import DES
from itertools import product
from binascii import b2a_uu
from gc import collect
from re import search
import random


def hex_to_decimal(hex_key):
    # Split the input hex key into 8 segments
    hex_segments = []
    for i in range(1,len(hex_key),2):
        temp = str(hex_key[i-1]) + str(hex_key[i])
        hex_segments.append(temp)
    # Convert each hex segment to decimal
    decimal_numbers = []
    for segment in hex_segments:
        try:
            # Convert hex to decimal
            decimal = int(segment, 16)
            decimal_numbers.append(decimal)
        except ValueError:
            return f"Error: Invalid hex segment '{segment}'"

    return decimal_numbers

if __name__ == "__main__":
    print("Key:",end=' ')
    keyInput = input()
    hex_key, leak_hex_key = [],["***" for i in range(8)]
    decimal_key, leak_deciaml_key = hex_to_decimal(keyInput),["***" for i in range(8)]

    for i in range(1, len(keyInput), 2):
        temp = str(keyInput[i - 1]) + str(keyInput[i])
        hex_key.append(temp)

    print("Số byte bị leak:", end=' ')
    leak_byte_cnt = int(input())

    for i in random.sample(range(0, 8), leak_byte_cnt):
        leak_deciaml_key[i] = decimal_key[i]
        leak_hex_key[i] = hex_key[i]

    print("Key bị leak (hệ 16):", end=' ')
    print(leak_hex_key)
    print("Key bị leak (hệ 10):",end=' ')
    print(leak_deciaml_key)
    print("Tiếp tục:", end=' ')
    continue_process = input()
    match continue_process:
        case "YES"|"yes"|"y"|"Y":
            for keyGen in product(range(256), repeat=8-leak_byte_cnt):
                try:
                    key = bytearray(
                        (0, 0, 0, 0, 0, 0, 0, 0)
                    )
                    j=0
                    for i in range(8):
                        if leak_deciaml_key[i]!="***":
                            key[i] = leak_deciaml_key[i]
                        else:
                            key[i] = keyGen[j]
                            j+=1
                    print("Try key = ", key.hex())
                    cipher = DES.new(key, DES.MODE_ECB)
                    plaintext = cipher.decrypt(bytes.fromhex("bae64ae54e2447632089c81790c95dd9"))
                    match = search("[A-Z]{1}[0-9]{2}[A-Z]{4}[0-9]{3}", plaintext.decode())

                    if match:
                        with open("plaintext", "w") as f:
                            f.write(f"Key: {key.hex()}\nPlaintext:{match.group()}\n")
                        print(f"Final! Collected key: {key.hex()}")
                        print(f"Save key and plaintext to: {os.path.abspath("plaintext")}")
                        exit()
                except Exception as e:
                    pass
                finally:
                    collect()
        case "NO"|"N"|"n"|"no":
            exit()
        case _:
            print("Error")