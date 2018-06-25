from flask import Flask, render_template,session,request,redirect,flash
from mysqlconnection import connectToMySQL
from datetime import datetime,date
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-z0-9._-]+\.[a-zA-z]+$')
app = Flask(__name__)
app.secret_key = "ThisIsSecret"

mysql = connectToMySQL('emailval')

@app.route('/')
def index():
    if 'wrong' not in session:
        session['wrong'] = ''
    if 'deleted' not in session:
        session['deleted'] = ''
    print(datetime.strptime(str(datetime.now()),'%Y-%m-%d %H:%M:%S.%f').strftime('%m/%d/%Y %I:%M %p'))
    return render_template('submit.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.form
    errors = 0 
    testquery = mysql.query_db(f'select * from table1 where email="{data["email"]}"')
    if not data['email']:
        flash(u'Please enter an email address', 'error')
        errors += 1
    elif not EMAIL_REGEX.match(data['email']):
        flash(u'Invalid email address','invalid')
        errors += 1
    elif testquery:
        flash(u'Email has already been used!', 'invalid')
        errors += 1
    
    if errors == 0:
        session['correct'] = data['email']
        return redirect('/success')

    session['wrong'] = data['email']
    return redirect('/')

@app.route('/success')
def success():
    if session['deleted'] != 'true':
        flash(f'The email address you entered ({session["correct"]}) is a valid email address! Thank you!', 'success')
        newquery = 'insert into table1 (email, time_entered) values(%(email)s, %(time_entered)s);'
        newdata = {'email':session['correct'], 'time_entered':datetime.now()}
        mysql.query_db(newquery,newdata)
    emails = mysql.query_db('select * from table1')
    return render_template('success.html', emails=emails)

@app.route('/delete/<id>')
def delete(id):
    deletequery = 'delete from table1 where id=%(ider)s'
    deletedata = {'ider':id}
    mysql.query_db(deletequery, deletedata)
    session['deleted'] = 'true'
    return redirect('/success')

@app.route('/reset')
def reset():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)