from flask import Flask, render_template, url_for, request, flash, redirect, jsonify, Response
from form import RegistrationForm, LoginForm, BankerlogForm, History
import pandas as pd
import os
alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

app = Flask(__name__, template_folder='ProjectTemplate')

app.config['SECRET_KEY']='6c4448ffb775aa1831b04ef0a9a1b4df'

@app.route("/")
@app.route("/Home")
def HomePage():
    return render_template('Home.html')

@app.route("/")
@app.route("/About")
def AboutPage():
    return render_template('about.html')

def save_to_file(first_name, last_name, email, password):
    file_path = 'customers.txt'
    if not os.path.exists(file_path):
        with open(file_path, 'w'):
            pass
    with open(file_path, 'a') as file:
        file.write(f'{first_name}, {last_name}, {email}, {password}\n')

def Find_file_name(first_name,last_name):
    count=1
    countf1=0
    countf2=0
    for i in alphabet:
        if str.upper(first_name[0]) == i:
            countf1=count
        if str.upper(last_name[0]) == i:
            countf2=count
        count+=1
        return f"{str.upper(first_name[0])}{str.upper(last_name[0])}-{len(first_name)+len(last_name)}-{countf1}-{countf2}.txt"

def Create_Perso_File_Customer(first_name, last_name, email, password):
    count=1
    countf1=0
    countf2=0
    for i in alphabet:
        if str.upper(first_name[0]) == i:
            countf1=count
        if str.upper(last_name[0]) == i:
            countf2=count
        count+=1
    file_path = f'PoubelleDepatel\{str.upper(first_name[0])}{str.upper(last_name[0])}-{len(first_name)+len(last_name)}-{countf1}-{countf2}.txt'
    if not os.path.exists(file_path):
        with open(file_path, 'w'):
            pass
        with open(file_path, 'a') as file:
            file.write(f'{first_name}, {last_name}, {email}, {password};\n')

@app.route("/register", methods=['GET', 'POST'])
def register():
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit() and request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        save_to_file(first_name, last_name, email, password)
        Create_Perso_File_Customer(first_name, last_name, email,password)	
        flash(f'Account created for {reg_form.first_name.data}!', 'success')
        return redirect(url_for('HomePage'))
    return render_template('register.html', title='Register', form=reg_form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    log_form = LoginForm()
    if log_form.validate_on_submit():
        if log_form.email.data == 'admin@blog.com' and log_form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('CustomerviewPage'))
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

@app.route('/custumerview', methods=['GET', 'POST'])
def CustomerviewPage():
    if request.method == 'POST':
        action = request.form.get('action')
        account_type = request.form.get('account_type')
        amount = float(request.form.get('amount'))

        if account_type not in ('current', 'savings'):
            flash('Invalid account type', 'danger')
            return redirect(url_for('CustomerviewPage'))

        if action == 'withdraw':
            success, message = withdraw(account_type, amount)
            if not success:
                flash(message, 'danger')
            else:
                flash(message, 'success')
        elif action == 'deposit':
            deposit(account_type, amount)
            flash(f'Deposited {amount} into {account_type} account', 'success')

    # Charger les informations du compte
    accounts = load_accounts()

    return render_template('CustomerView.html', accounts=accounts)

def load_accounts():
    file_path = 'user_accounts.txt'
    accounts = {'current': 0.0, 'savings': 0.0}

    if file_path and os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                elements = line.strip().split(',')
                if len(elements) >= 2:
                    account_type, balance = map(str.strip, elements[:2])
                    accounts[account_type] = float(balance)
                else:
                    flash(f'Invalid line in file: {line}', 'error')

    return accounts

def save_accounts(accounts):
    file_path = 'user_accounts.txt'

    with open(file_path, 'w') as file:
        for account_type, balance in accounts.items():
            file.write(f'{account_type},{balance}\n')

def withdraw(account_type, amount):
    accounts = load_accounts()
    if amount > accounts[account_type]:
        return False, 'Insufficient funds'
    else:
        accounts[account_type] -= amount
        save_accounts(accounts)
        record_transaction(account_type, 'withdraw', amount)
        return True, f'Withdrew {amount} from {account_type} account'

def deposit(account_type, amount):
    accounts = load_accounts()
    accounts[account_type] += amount
    save_accounts(accounts)
    record_transaction(account_type, 'deposit', amount)

def record_transaction(account_type, action, amount):
    file_path = 'transaction_history.txt'

    with open(file_path, 'a') as file:
        file.write(f'{account_type},{action},{amount}\n')

def load_transactions():
    file_path = 'transaction_history.txt'
    transactions = []

    with open(file_path, 'r') as file:
        for line in file:
            account, action, amount = line.strip().split(',')
            transaction = {
                'account': account,
                'action': action,
                'amount': float(amount)  # Assurez-vous de convertir le montant en nombre si nécessaire
            }
            transactions.append(transaction)

    return transactions

def stream():
    def generate():
        while True:
            transactions = load_transactions()
            for transaction in transactions:
                yield f'data: {transaction}\n\n'
            time.sleep(1)  # Ajoutez un délai d'attente pour éviter une boucle infinie rapide

    return Response(generate(), content_type='text/event-stream')

@app.route('/get_transactions')
def get_transactions():
    transactions = load_transactions()
    return jsonify(transactions)


if __name__ == '__main__':
	app.run(debug=True)