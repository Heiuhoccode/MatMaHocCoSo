import binascii as ma_hoa_hex
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

khoa = b"this_is_the_key!"
iv = b"a"*16  # chỉ để test

du_lieu_vi_du = \
    b"toi rat thich xem da bong va toi cung thich da bong rat nhieu" + \
    b" cuoc tan cong vao AES voi khoa 128 bitbitbit  "

def ma_hoa(du_lieu, khoa, iv):
    ma_hoa_obj = AES.new(khoa, AES.MODE_CBC, iv)
    da_pad = pad(du_lieu, 16)
    print("\x1b[92mDu lieu sau khi pad:\x1b[0m")
    print(ma_hoa_hex.hexlify(da_pad).decode())
    return iv + ma_hoa_obj.encrypt(da_pad)

def orac(du_lieu):
    global khoa
    global iv
    ma_hoa_obj = AES.new(khoa, AES.MODE_CBC, iv)
    da_giai_ma = ma_hoa_obj.decrypt(du_lieu)
    ket_qua = None
    try:
        ban_ro = unpad(da_giai_ma, 16)
        ket_qua = {"thanh_cong": True, "da_giai_ma": da_giai_ma}
    except:
        ket_qua = {"thanh_cong": False, "da_giai_ma": da_giai_ma}
    return ket_qua

# --------------------------------------------------------- #

ban_ma = ma_hoa(du_lieu_vi_du, khoa, iv)

cac_khoi = [ban_ma[i:i+16] for i in range(0, len(ban_ma), 16)]

ban_ro = b""
while len(cac_khoi) > 1:
    da_tim_padding = b""

    print("="*30 + " \x1b[1;33m Khoi moi \x1b[0m" + "="*30)

    for gia_tri_padding in range(1, 17):
        tim_duoc = None

        # Tạo block giả mạo dựa trên padding đã biết
        if len(da_tim_padding) > 0:
            tan_cong = b""
            padding_cu = gia_tri_padding - 1
            padding_moi = gia_tri_padding
            da_tim_padding = b"".join(
                [(x ^ padding_cu ^ padding_moi).to_bytes(1, "little") for x in da_tim_padding]
            )

        # Đoán từng byte
        for doan in range(256):
            byte_doan = doan.to_bytes(1, "little")
            khoi_gia = cac_khoi[-2][:16-gia_tri_padding] + byte_doan + da_tim_padding
            ban_ma_gia = b"".join(cac_khoi[:-2]) + khoi_gia + cac_khoi[-1]

            ket_qua_oracle = orac(ban_ma_gia)

            if ket_qua_oracle["thanh_cong"]:
                print((byte_doan + da_tim_padding).hex() + " ▶ \x1b[91m" +
                      ket_qua_oracle["da_giai_ma"][-gia_tri_padding:].hex() + "\x1b[0m")
                if ket_qua_oracle["da_giai_ma"][-gia_tri_padding] != gia_tri_padding:
                    print(hex(ket_qua_oracle["da_giai_ma"][-gia_tri_padding]))
                    continue
                tim_duoc = doan
                break

        if tim_duoc is not None:
            byte_trung_gian = tim_duoc ^ gia_tri_padding
            byte_thuc_te = byte_trung_gian ^ cac_khoi[-2][16-gia_tri_padding]
            ban_ro = byte_thuc_te.to_bytes(1, "little") + ban_ro
            da_tim_padding = (gia_tri_padding ^ byte_trung_gian).to_bytes(1, "little") + da_tim_padding
        else:
            print("Khong tim duoc byte phu hop.")
            exit(-1)

    cac_khoi.pop()

print("="*30 + " \x1b[1;32m Ban ro: \x1b[0m" + "="*30)
print(ban_ro.decode())
print("="*30 + " \x1b[1;32m Ket thuc \x1b[0m" + "="*30)