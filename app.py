from flask import Flask, render_template, request, redirect, url_for, flash, session
import psycopg2
import pyotp
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secret key

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.example.com'  # Replace with your mail server
app.config['MAIL_PORT'] = 587  # Port number
app.config['MAIL_USE_TLS'] = True  # Use TLS
app.config['MAIL_USERNAME'] = 'your_email@example.com'  # Your email
app.config['MAIL_PASSWORD'] = 'your_password'  # Your email password
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@example.com'

mail = Mail(app)

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
        # Generate an OTP
        otp = pyotp.random_base32()  # Generate a random OTP secret
        session['otp'] = otp  # Store OTP in the session
        session['username'] = username  # Store username for later use

        # Send OTP to user's email (assuming email is stored in the database)
        email = user[2]  # Assuming email is the third column in your table
        send_otp(email, otp)

        return render_template('verify_otp.html')  # Show OTP verification page
    else:
        flash('Login failed. Please check your credentials.', 'error')
        return redirect(url_for('index'))

def send_otp(email, otp):
    msg = Message('Your OTP Code', recipients=[email])
    msg.body = f'Your OTP code is: {otp}'
    mail.send(msg)

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    entered_otp = request.form['otp']
    generated_otp = session.get('otp')

    if entered_otp == generated_otp:
        flash('Login successful!', 'success')  # Flash success message
        session.pop('otp', None)  # Clear the OTP from the session
        return redirect(url_for('index'))
    else:
        flash('Invalid OTP. Please try again.', 'error')
        return render_template('verify_otp.html')

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
