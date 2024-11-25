from flask import Flask, flash, render_template, request, redirect, session
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mywebsitedb'

app.secret_key = 'nguyenanhduydeptraivocung'

mysql = MySQL(app)

# Registration Page (Root URL)
@app.route('/', methods=['GET', 'POST'])
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
            return redirect('/home')
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html')

@app.route('/users')
def index():
    # Fetch users from MySQL
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.close()
    return render_template('index.html', users=users)

@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        # Insert into MySQL
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        mysql.connection.commit()
        cur.close()
        return redirect('/')
    return render_template('add_user.html')

@app.route('/home')
def home():
    
    return render_template('homepage.html')

if __name__ == '__main__':
    app.run(debug=True)