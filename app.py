from flask import Flask, render_template, request, redirect, session
from os import getenv, urandom
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = "1234" #getenv("SECRET_KEY") # Sensitive data exposure?

def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id' not in session:
            return redirect('/login')
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (session['id'],)).fetchone()
        conn.close()
        
        if user['role'] != 'admin':
                return redirect('/')
        
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'username' in session:
        return render_template('/index.html')
    return render_template('/index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #hashed_password = generate_password_hash(password) # Sensitive data exposure, uncomment to add hashed password back


        conn = get_db_connection()

        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if user:
            if username==user['username']:
                return render_template("register.html", message="Username already exists.")

        conn.executescript('INSERT INTO users (username, password) VALUES ("'+username+'","'+password+'")')  # SQL Injection
        # Comment the line above to hide sql injection
        
        # Using the injection below user is able to create an admin account
        # password"); INSERT INTO users (username, password, role) VALUES ("username", "password", "admin
        
        # Uncomment the line below for fix sql injection and add hashed password back
        #conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))  # Sensitive data exposure, missing hashed password
        
        conn.commit()
        conn.close()

        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("/login.html")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user:
            if  user['password'] == password or user['role']=="admin": 
            #if check_password_hash(user['password'], password) or user['role']=="admin":
                session['id'] = user['id']            # Sensitive data exposure, comment the if statement above and uncomment the commented one to add hashed password back
                session['username'] = user['username']
                if user['role']=="admin":
                    session['role'] = "admin"
                #session["csrf_token"] = urandom(16).hex()     # Missing CSRF, uncomment to add it back
                return redirect('/')
        return render_template("/login.html", message="Wrong username or password")
    
    return render_template('/login.html')

@app.route('/admin')
#@admin_required         # Broken access control, admin panel can be reached by anyone just by adding /admin to the address
def admin_panel():
    conn = get_db_connection()
    users = conn.execute('SELECT id, username, password, role FROM users').fetchall()
    conn.close()
    return render_template('/admin.html', users=users)

@app.route('/button', methods=['GET', 'POST'])
def button():
    if request.method == "GET":
        return render_template("/button.html")

    if request.method == "POST":
        #if check_csrf():           # Missing CSRF on method that needs one, uncomment both lines to add it back
        #    return render_template('/index.html', message="Invalid CSRF_TOKEN")
        return render_template('/index.html', message="Valid CSRF_TOKEN")

@app.route('/logout')
def logout():
    session.clear()      # Broken authentication if I was to comment this line out, but it currently affects the usability of the app by little bit
    return render_template('/index.html', message="You logged out")

#def check_csrf():       # Missing CSRF, uncomment to add it back
    if session:
        if session["csrf_token"] != request.form["csrf_token"]:
            return True
        return False
    return True