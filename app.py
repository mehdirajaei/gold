from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import os
import locale
from num2fawords import words  # تبدیل عدد به حروف فارسی

app = Flask(__name__)

# تنظیمات لوکال برای جدا کردن اعداد ۳ رقم ۳ رقم
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# تنظیمات ورود
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['USERNAME'] = 'admin'  # نام کاربری
app.config['PASSWORD'] = generate_password_hash('your_password')  # رمز عبور هش شده

# مسیر ورود
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == app.config['USERNAME'] and check_password_hash(app.config['PASSWORD'], password):
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash('نام کاربری یا رمز عبور اشتباه است!', 'danger')
    return render_template('login.html')

# مسیر محاسبه قیمت طلا
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    final_price = None
    final_price_words = None  # تبدیل مبلغ به حروف فارسی

    if request.method == 'POST':
        try:
            # دریافت مقادیر ورودی
            price_per_gram = float(request.form['price_per_gram'])
            weight = float(request.form['weight'])
            profit = float(request.form['profit'])
            tax = float(request.form['tax'])
            manufacture_cost = float(request.form['manufacture_cost'])

            # فرمول محاسبه قیمت نهایی
            final_price = (price_per_gram / 4.3337) * weight * ((profit + tax + 100 + manufacture_cost) / 100)
            final_price = round(final_price, 2)

            # تبدیل مبلغ به حروف فارسی
            final_price_words = words(int(final_price)) + " تومان"

        except ValueError:
            flash('لطفاً مقادیر معتبر وارد کنید', 'danger')

    return render_template('index.html', final_price=final_price, final_price_words=final_price_words)

# مسیر خروج
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
