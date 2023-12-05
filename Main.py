from flask import Flask, render_template, url_for, request, flash, redirect
from form import RegistrationForm, LoginForm, BankerlogForm
import pandas as pd
import os

app = Flask(__name__,template_folder='ProjectTemplate')

app.config['SECRET_KEY']='6c4448ffb775aa1831b04ef0a9a1b4df'

@app.route("/")
@app.route("/Home")
def HomePage():
    return render_template('Home.html')

@app.route("/")
@app.route("/About")
def AboutPage():
    return render_template('about.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit() and request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        save_to_file(first_name, last_name, email)	
        flash(f'Account created for {reg_form.first_name.data}!', 'success')
        return redirect(url_for('HomePage'))
    return render_template('register.html', title='Register', form=reg_form)

def save_to_file(first_name, last_name, email):
    file_path = 'customers.txt'
    if not os.path.exists(file_path):
        with open(file_path, 'w'):
            pass
    with open(file_path, 'a') as file:
        file.write(f'{first_name}, {last_name}, {email}\n')

@app.route("/login", methods=['GET', 'POST'])
def login():
    log_form = LoginForm()
    if log_form.validate_on_submit():
        if log_form.email.data == 'admin@blog.com' and log_form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('HomePage'))
        else:
            flash('Login Unsuccessful. Please check username and password.', 'danger')
    return render_template('login.html', title='Login Customer', form=log_form)

@app.route("/bankerLog", methods=['GET', 'POST'])
def LoginBankerPage():
    banker_log = BankerlogForm()
    if banker_log.submit.data == True:
        if banker_log.password.data == 'A1234':
            flash('You have been logged in!', 'success')
            return redirect(url_for('HomePage'))
        else:
            flash('Login Unsuccessful. Please check password.', 'danger')
    return render_template('loginBanker.html', title='Login Banker', form=banker_log)

if __name__ == '__main__':
	app.run(debug=True)