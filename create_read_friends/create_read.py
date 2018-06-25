from flask import Flask, render_template, request, session, redirect
from mysqlconnection import connectToMySQL

app = Flask(__name__)

mysql = connectToMySQL('friendsdb')

@app.route('/')
def index():
    all_friends = mysql.query_db('select * from friends')
    return render_template('friends.html', friends = all_friends)

@app.route('/create_friend', methods=['POST'])
def create():
    query = "insert into friends (first_name, last_name, occupation) values (%(first_name)s, %(last_name)s, %(occupation)s);"
    data = {'first_name':request.form['first_name'], 'last_name':request.form['last_name'], 'occupation':request.form['occupation']}
    mysql.query_db(query, data)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)