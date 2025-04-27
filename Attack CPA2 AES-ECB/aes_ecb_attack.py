
import string
from aes_ecb_oracle import oracle
import time

chars = '0123456789!$%&\'()*=+,-./:;?@[\\]^_`{|}~ \t\n\r\x0b\x0cABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

def main():
	Display = True # Display - Hiển thị các bước trung gian

	Walkthru = True # Walkthru - Tạm dừng tại mỗi bước để nguoi dùng theo dõi

	SeeOracle = True # SeeOracle - Hiển thị thông tin oracle (góc nhìn của attack - False)

	Timing =  False # Timing - Làm chậm quá trình để quan sát

	# Phục vụ cho trình bày:    Display = True,
	# 							Walkthru = True, 
	# 							SeeOracle = True/False, 
	# 							Timing = True

	# Phục vụ cho kiểm tra: 	Display = True/False,
	# 							Walkthru = False,
	# 							SeeOracle = True, 
	# 							Timing = False

	attack(Display, Walkthru, SeeOracle,  Timing)

# Attack CPA2
def attack(disp, walkthru=False, see_oracle = False, timing = False):
	first = True
	upper = 32 # Độ dài 2 khối đầu tiên - mỗi khối 16 byte
	secret_len = 24 # Độ dài chuỗi bí mật cần khôi phục
	len_init =  upper - len("data=")
	a_list = 'a' * len_init

	known = a_list # Chuỗi kí tự 'a'

	if walkthru:
		keepgoing = True
		i = 0
		known_list = []
		for i in range(secret_len):
			if first: 
				known = get_next_byte(a_list, known, upper, False, walkthru, see_oracle, timing)
				first = False
			else:
				known = get_next_byte(a_list, known, upper, disp, walkthru, see_oracle, timing)
			a_list = a_list[0:-1]

			if keepgoing:
				if"skip" == input("Tiếp tục hoặc bỏ qua (skip) ? "):
					keepgoing = False
					disp = False
			known_list += [known]

		print("Tóm tắt:\n")
		for i in known_list: 
			if timing: time.sleep(.05)
			print("Chuỗi đã biết: ", i)

	else:
		for i in range(secret_len):
			known = get_next_byte(a_list, known, upper, disp, walkthru, see_oracle, timing)
			a_list = a_list[0:-1]

	len_fin = len(a_list) +1
	result = known[len_fin:]
	print("\nKết Quả\n------------------------------\n", result,"\n")
	res =  result.strip("X")
	print(res, "\n\n")
	return res


def get_next_byte(a_list, known, upper, disp, walkthru, see_oracle, timing=False):
	D = {} # Từ điển ánh xạ kí tự sang ciphertext
	for c in chars:
		print(f'Thử chuỗi: {known} {c}')
		curr = known[1:] + c
		encrypted = oracle(curr, disp, see_oracle, timing)
		second_block = encrypted[16:upper]
		D[second_block] = c

	correct_curr = oracle(a_list, disp, see_oracle, timing)[16:upper]

	if correct_curr in D.keys():
		true_char = D[correct_curr]
		result = known[1:] + true_char

	if walkthru:
		if timing: time.sleep(.3)
		display_round(known, true_char, result)
	return result


def display_round(known, true_char, result):
	print("\n\nGọi oracle cho mỗi kí tự '?':",known[1:], "?")
	print(f"Kết quả: {result}")
	print(f"Kí tự đúng: {true_char}\n")


if __name__ == "__main__":
	main()
