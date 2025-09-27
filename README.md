# MatMaHocCoSo

**MatMaHocCoSo** — Dự án môn *Mật mã học cơ sở* minh họa và đánh giá một số hệ mã cổ điển và hiện đại (DES, AES, RC4, A5/1...), kèm mô phỏng tấn công cơ bản và so sánh hiệu năng.

---

## Mô tả ngắn
Dự án này cài đặt các thuật toán mã hóa/giải mã phục vụ mục tiêu học tập và thí nghiệm:
- Thực hành nguyên lý AES (ECB/CBC), DES, RC4, A5/1.
- Thực hiện thử nghiệm tấn công đơn giản (ví dụ brute-force trên DES nhỏ / khảo sát điểm yếu).
- So sánh hiệu năng và phân tích an toàn của từng hệ mã.

Mục tiêu: hiểu sâu cơ chế hoạt động, hiện tượng lộ thông tin, và cách đánh giá độ an toàn thực nghiệm.

---

## Tính năng chính
- Cài đặt/triển khai: `aes_ecb.py`, `aes_cbc.py`, `des.py`, `rc4.py`, `a51.py` (mẫu tên).
- Module kiểm tra/benchmark: đo thời gian mã hóa / giải mã.
- Mô-đun mô phỏng tấn công cơ bản: `des_bruteforce.py` (ví dụ).
- Notebook minh họa (nếu có): `notebooks/analysis.ipynb` hiển thị so sánh kết quả.
- Test cơ bản cho từng module trong thư mục `tests/`.

---

## Yêu cầu
- Python 3.8+
