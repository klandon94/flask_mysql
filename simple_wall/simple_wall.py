from flask import Flask, render_template,session,request,redirect,flash
from flask_bcrypt import Bcrypt
from mysqlconnection import connectToMySQL
from datetime import date,datetime,timedelta

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "ThisIsSecret"

mysql = connectToMySQL('simple_wall')

@app.route('/')
def index():
    if 'logged_in' not in session:
        session['logged_in'] = False
    if 'justloggedout' in session and session['justloggedout'] == True:
        flash ('You have been successfully logged out', 'logout')
        session['justloggedout'] = False
    if 'forced' in session and session['forced'] == True:
        session.clear()
        flash('You have been forcibly logged out!','logoutbad')
    return render_template('wall_login.html')

@app.route('/login', methods=['POST'])
def login():
    login_data = request.form
    session['username'] = login_data['username']

    newquery = "select * from users where username = %(username)s;"
    logindata = {'username':login_data['username']}
    result = mysql.query_db(newquery, logindata)

    if not login_data['username'] or not login_data['password']:
        flash('Please fill out all fields', 'login')
    elif result:
        if result[0]['password'] == login_data['password']:
            session['logged_in'] = True
            session['name'] = result[0]['first_name']
            session['id'] = result[0]['id']
            return redirect('/mainpage')
        else:
            flash('You could not be logged in...','login')
    else:
        flash("You aren't in our database!", 'login')
    
    return redirect('/')

@app.route('/mainpage')
def mainpage():
    if 'logged_in' in session:
        if session['logged_in'] == True:

            allusers = mysql.query_db("select id, first_name from users")
            otherusers = mysql.query_db(f"select id as ider, first_name from users where users.id != {session['id']}")
            sentmessages = mysql.query_db(f"select messages.id, users.id as sender, messages.sent_user_id as sent_to, messages.content as content, messages.date_sent as date from messages join users on messages.user_id=users.id where users.id={session['id']} order by date_sent desc;")
            incomingmessages = mysql.query_db(f"select messages.id, messages.user_id as sent_from, messages.content as content, messages.date_sent as date from messages join users on messages.sent_user_id=users.id where users.id={session['id']} order by messages.id desc;")

            return render_template('wall_messages.html', allusers=allusers, otherusers=otherusers, sentmessages=sentmessages, incomingmessages=incomingmessages)
    session.clear()
    flash('You must be logged in to enter this webpage','logoutbad')
    return redirect('/')

@app.route('/sendmessage/<id>', methods=['POST'])
def send(id):
    outmsg = request.form['outmessage']
    sendmsgquery = 'insert into messages (user_id, sent_user_id, content, date_sent) values (%(user_id)s, %(sent_user_id)s, %(content)s, %(date_sent)s);'
    sendmsgdata = {'user_id':session['id'], 'sent_user_id':id, 'content':outmsg, 'date_sent':datetime.now()}
    mysql.query_db(sendmsgquery,sendmsgdata)
    flash('Message sent!', 'msgsent')
    return redirect('/mainpage')

@app.route('/delete/<id>')
def delete(id):
    deletesearch = mysql.query_db(f"select messages.id, messages.content from messages join users on messages.sent_user_id=users.id where users.id={session['id']} order by messages.id desc;")
    if any(x['id'] == int(id) for x in deletesearch):
        mysql.query_db(f"delete from messages where id={id}")
        flash('Message deleted!', 'msgsent')
        return redirect('/mainpage')
    else:
        if 'timesdangered' not in session:
            session['timesdangered'] = 1
        else:
            session['timesdangered'] += 1
        session['badnum'] = int(id)
        return redirect('/danger')

@app.route('/danger')
def dangerzone():
    if session['timesdangered'] == 2:
        session['forced'] = True
        return redirect('/logout')
    session['ip'] = request.environ['REMOTE_ADDR']
    return render_template('danger.html')

@app.route('/logout')
def logout():
    if 'forced' in session:
        return redirect('/')
    session.clear()
    session['justloggedout'] = True
    return redirect('/')

@app.route('/reset')
def reset():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)