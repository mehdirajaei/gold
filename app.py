import os
import locale
from flask import Flask, render_template, request, redirect, url_for, session, flash
from babel.numbers import format_decimal
from num2words import num2words

# رفع مشکل locale در محیط‌های غیر GUI مانند Render
try:
    locale.setlocale(locale.LC_ALL, 'fa_IR.UTF-8')  # تنظیم زبان فارسی
except locale.Error:
    locale.setlocale(locale.LC_ALL, 'C')  # مقدار پیش‌فرض در صورت عدم پشتیبانی

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # کلید امنیتی برای نشست‌ها

# اطلاعات ورود (می‌توانید تغییر دهید)
USERNAME = "admin"
PASSWORD = "1234"

# تابع جدا کردن سه رقم سه رقم اعداد
def format_number(number):
    return format_decimal(number, locale='fa_IR')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('calculator'))
        else:
            flash('نام کاربری یا رمز عبور اشتباه است!', 'danger')

    return render_template('login.html')

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    final_price = None
    final_price_words = ""

    if request.method == 'POST':
        try:
            price_per_gram = float(request.form['price_per_gram'])
            wage = float(request.form['wage'])
            weight = float(request.form['weight'])
            profit = float(request.form['profit'])
            tax = float(request.form['tax'])

            # فرمول محاسبه قیمت نهایی
            base_price = price_per_gram / 4.3337
            total_price = base_price * weight * ((profit + tax + wage + 100) / 100)

            # فرمت‌دهی عدد و تبدیل به حروف
            final_price = format_number(total_price)
            final_price_words = num2words(int(total_price), lang='fa') + " تومان"

        except ValueError:
            flash('لطفاً مقادیر عددی معتبر وارد کنید!', 'danger')

    return render_template('calculator.html', final_price=final_price, final_price_words=final_price_words)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=10000)
