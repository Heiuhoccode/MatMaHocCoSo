from flask import Flask, request, redirect, make_response, render_template
from rc4 import rc4

app = Flask(__name__)
STATIC_KEY = "my_very_weak_key"  # ⚠️ KHÔNG ĐƯỢC DÙNG TRONG THỰC TẾ

# Tài khoản hợp lệ (để kiểm tra)
valid_user = "admin"
valid_password = "123456"

@app.route('/')
def index():
    cookie = request.cookies.get('auth')
    if cookie:
        try:
            decrypted = rc4(STATIC_KEY, bytes.fromhex(cookie).decode('latin1'))
            return f"<h2>Xin chào {decrypted}!</h2>"
        except Exception as e:
            return "<h2>Cookie không hợp lệ!</h2>"
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Kiểm tra thông tin đăng nhập
        if username == valid_user and password == valid_password:
            encrypted = rc4(STATIC_KEY, username)
            hex_cookie = encrypted.encode('latin1').hex()

            resp = make_response(redirect('/'))
            resp.set_cookie('auth', hex_cookie)
            return resp
        else:
            return "<h2>Tên người dùng hoặc mật khẩu không đúng!</h2>"

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
