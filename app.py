from flask import Flask, flash, render_template, request, redirect, session
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mywebsitedb'

app.secret_key = 'ThrillOfTheHunt'

mysql = MySQL(app)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        fullname = request.form['fullname']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, email, password, fullname) VALUES (%s, %s, %s, %s)", (username, email, password, fullname))
        mysql.connection.commit()
        cur.close()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchall()
        cur.close()

        if user:
            session['user_id'] = user[0]
            flash('Login successful!', 'success')
            return redirect('/')
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html')

@app.route('/')
def home():
    return render_template('homepage.html')

if __name__ == '__main__':
    app.run(debug=False)