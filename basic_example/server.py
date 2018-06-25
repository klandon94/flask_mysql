from flask import Flask
from mysqlconnection import connectToMySQL

app = Flask(__name__)
# invoke the connectToMySQL function and pass it the name of the databse we're using
# connectToMySQL returns an instance of MySQLConnection, which we will store in the variable 'mysql'
mysql = connectToMySQL('mydb')
# now we can invoke the query_db method from the MySQLConnection class
print('\n\nall the users', mysql.query_db('SELECT name FROM users;'))

if __name__ == '__main__':
    app.run(debug=True)