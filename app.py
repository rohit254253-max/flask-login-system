from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)

app.secret_key = "secret123"


# DATABASE CREATE
def init_db():

    conn = sqlite3.connect('database.db')

    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT

    )
    """)

    conn.commit()
    conn.close()


init_db()


# HOME
@app.route('/')
def home():

    return redirect('/login')


# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        conn = sqlite3.connect('database.db')

        cur = conn.cursor()

        cur.execute(
            "INSERT INTO users(username, password) VALUES(?, ?)",
            (username, password)
        )

        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('register.html')


# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')

        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=? ",
            (username, )
        )

        user = cur.fetchone()

        conn.close()

        if user and check_password_hash(user[2], password):

            session['user'] = username

            return redirect('/dashboard')

        else:

            return "Invalid Username or Password"

    return render_template('login.html')


# DASHBOARD
@app.route('/dashboard')
def dashboard():

    if 'user' in session:

        return render_template(
            'dashboard.html',
            username=session['user']
        )

    return redirect('/login')


# LOGOUT
@app.route('/logout')
def logout():

    session.pop('user', None)

    return redirect('/login')


# RUN APP
if __name__ == "__main__":

    app.run(debug=True)