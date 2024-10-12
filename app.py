from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# PostgreSQL database connection
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="login_database",
        user="user1",
        password="password1",
        port="5433"  # PostgreSQL's default port
    )
    return conn

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    cur = conn.cursor()

    # Check if user exists in the register_users table
    cur.execute("SELECT * FROM register_users WHERE username = %s AND password = %s", (username, password))
    user = cur.fetchone()

    cur.close()
    conn.close()

    if user:
        flash('Login successful!', 'success')  # Flash success message
        return redirect(url_for('index'))
    else:
        flash('Login failed. Please check your credentials.', 'error')  # Flash error message
        return redirect(url_for('index'))

# Route to render the registration page
@app.route('/register', methods=['GET'])
def show_register_form():
    return render_template('register.html')

# Route to handle the registration form submission
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # Insert new user details into the register_users table
        cur.execute("INSERT INTO register_users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        conn.commit()
        flash('Registration successful!', 'success')  # Flash success message
    except Exception as e:
        conn.rollback()  # Rollback in case of error
        flash('Registration failed. User may already exist.', 'error')  # Flash error message
    finally:
        cur.close()
        conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
