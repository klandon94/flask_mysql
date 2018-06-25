from flask import Flask, render_template,session,request,redirect,flash
from flask_bcrypt import Bcrypt
from mysqlconnection import connectToMySQL
from datetime import date,datetime,timedelta
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-z0-9._-]+\.[a-zA-z]+$')
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "ThisIsSecret"

mysql = connectToMySQL('login_registration')

@app.route('/')
def index():
    if 'logged_in' not in session:
        session['logged_in'] = False
    if 'just_reg' not in session:
        session['just_reg'] = False
    if 'justloggedout' in session:
        if session['justloggedout'] == True:
            flash ('You have been successfully logged out', 'logout')
            session['justloggedout'] = False
    return render_template('log_register.html')

@app.route('/register_user', methods=['POST'])
def register():
    data = request.form 

    session['first_name'] = data['first_name']
    session['last_name'] = data['last_name']
    session['email'] = data['email']
    session['birthday'] = data['birthday']

    if not data['first_name']:
        flash('Please enter your first name', 'first_name')
    elif len(data['first_name']) < 2 or not data['first_name'].isalpha():
        flash('First name must contain at least two letters and contain only letters', 'first_name')
    
    if not data['last_name']:
        flash('Please enter your last name', 'last_name')
    elif len(data['last_name']) < 2 or not data['last_name'].isalpha():
        flash('Last name must contain at least two letters and contain only letters', 'last_name')

    if not data['email']:
        flash('Please enter your email', 'email')
    elif not EMAIL_REGEX.match(data['email']):
        flash('Invalid email address', 'email')
    
    if not data['password']:
        flash('Please enter a password', 'password')
    elif len(data['password']) < 8:
        flash('Password must be at least 8 characters', 'password')
    elif not (any(x.isupper() for x in data['password'])) or not (any(x.isdigit() for x in data['password'])):
        flash('Password must contain at least 1 number and 1 uppercase letter', 'password')
    
    if not data['confirm_password']:
        flash('Please confirm your password', 'confirm_password')
    elif data['confirm_password'] != data['password']:
        flash('Passwords do not match', 'confirm_password')
    
    if not data['birthday']:
        flash('Please enter your birth date', 'birthday')
    elif (datetime.strptime(str(date.today()), '%Y-%m-%d') - datetime.strptime(data['birthday'], '%m/%d/%Y')) // timedelta (days=365.2) < 10:
        flash('You must be 10 years old to register', 'birthday')
    
    if '_flashes' in session.keys():
        return redirect('/')
    else:
        query = "insert into users (first_name, last_name, email, password, birthday) values (%(first_name)s, %(last_name)s, %(email)s, %(password_hash)s, %(birthday)s);"
        newdata = {'first_name':data['first_name'], 'last_name':data['last_name'], 'email': data['email'], 'password_hash':bcrypt.generate_password_hash(data['password']), 'birthday':data['birthday']}
        mysql.query_db(query,newdata)
        session['just_reg'] = True
        session['logged_in'] = True
        return redirect('/loggedin')

@app.route('/login', methods=['POST'])
def login():
    if session['logged_in'] == False:
        login_data = request.form
        session['login_email'] = login_data['login_email']

        newquery = "select * from users where email = %(login_email)s;"
        logindata = {'login_email':login_data['login_email']}
        result = mysql.query_db(newquery, logindata)
        
        if not login_data['login_email'] or not login_data['login_password']:
            flash('Please fill out all fields', 'login')

        elif result:
            if bcrypt.check_password_hash(result[0]['password'],login_data['login_password']):
                session['first_name'] = result[0]['first_name']
                session['logged_in'] = True
                return redirect('/loggedin')
            else:
                flash('You could not be logged in...', 'login')
        else:
            flash('You have not registered', 'login')
        return redirect('/')

    else:
        flash("You're already logged in!!",'logout')
        return redirect('/')

@app.route('/loggedin')
def loggedin():
    if 'just_reg' in session:
        if session['just_reg'] == True:
            flash("You've been successfully registered", 'registered')
            session['just_reg'] = False
            return render_template('loggeduser.html')
    if 'logged_in' in session:
        if session['logged_in'] == True:
            return render_template('loggeduser.html')
    session.clear()
    flash("You must be logged in to enter this website", 'logout')
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    session['justloggedout'] = True
    return redirect('/')

@app.route('/reset')
def reset():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)