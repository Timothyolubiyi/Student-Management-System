# Store this code in 'app.py'
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = 'your secret key'

# MySQL config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Super7898$$#'
app.config['MYSQL_DB'] = 'college'

mysql = MySQL(app)

# ---------------------------------------
# LOGIN
# ---------------------------------------
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM accounts WHERE username = %s AND password = %s',
            (username, password)
        )
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account['id']          # id now exists in table
            session['username'] = account['username']
            msg = 'Logged in successfully!'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect username or password!'
    return render_template('login.html', msg=msg)

# ---------------------------------------
# LOGOUT
# ---------------------------------------
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

# ---------------------------------------
# REGISTER
# ---------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''

    required_fields = ['username', 'password', 'email', 'address', 'city',
                       'country', 'postalcode', 'organisation', 'state']

    if request.method == 'POST' and all(field in request.form for field in required_fields):

        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        organisation = request.form['organisation']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        postalcode = request.form['postalcode']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Check if username exists
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only letters and numbers!'
        else:
            # Insert new user → correctly matches database columns
            cursor.execute("""
                INSERT INTO accounts 
                (username, password, email, organisation, address, city, state, country, postalcode)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (username, password, email, organisation, address, city, state, country, postalcode))

            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out all fields!'

    return render_template('register.html', msg=msg)

# ---------------------------------------
# HOME PAGE
# ---------------------------------------
@app.route('/index')
def index():
    if 'loggedin' in session:
        return render_template("index.html")
    return redirect(url_for('login'))

# ---------------------------------------
# DISPLAY USER DETAILS
# ---------------------------------------
@app.route("/display")
def display():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        return render_template("display.html", account=account)
    return redirect(url_for('login'))

# ---------------------------------------
# UPDATE USER DETAILS
# ---------------------------------------
@app.route("/update", methods=['GET', 'POST'])
def update():
    msg = ''

    if 'loggedin' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Fetch current account to prefill form
    cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
    account = cursor.fetchone()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        organisation = request.form['organisation']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        postalcode = request.form['postalcode']

        # Validate
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only letters and numbers!'
        else:
            # Update record
            cursor.execute("""
                UPDATE accounts SET
                    username = %s,
                    password = %s,
                    email = %s,
                    organisation = %s,
                    address = %s,
                    city = %s,
                    state = %s,
                    country = %s,
                    postalcode = %s
                WHERE id = %s
            """, (username, password, email, organisation, address, city,
                  state, country, postalcode, session['id']))
            mysql.connection.commit()
            msg = 'Update successful!'

            # Refresh account data to prefill again
            cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
            account = cursor.fetchone()

    return render_template("update.html", account=account, msg=msg)


# ---------------------------------------
# DELETE USER ACCOUNT
# ---------------------------------------
@app.route("/delete_account", methods=['POST'])
def delete_account():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Delete account based on logged-in user's id
    cursor.execute('DELETE FROM accounts WHERE id = %s', (session['id'],))
    mysql.connection.commit()

    # Clear session after deletion
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)

    return redirect(url_for('register'))  # Redirect to register page after deletion


# ---------------------------------------
# RUN APP
# ---------------------------------------
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
