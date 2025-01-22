from flask import Flask, render_template, request, redirect, url_for, session
import os
import sqlite3
from datetime import timedelta

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.secret_key = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # Sessie duurt 7 dagen
def save_registration(name):
    # Je kunt hier de naam opslaan in een database of bestand
    print(f"Registered {name}")
    return True

# Functie om te controleren of de gebruiker is ingelogd
def is_logged_in():
    if 'username' in session:
        return True
    else:
        return False
# Functie om gebruikers te controleren
def validate_user(username, password):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    connection.close()
    return user is not None

# Functie om nieuwe gebruikers toe te voegen
def add_user(username, password):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    connection.commit()
    connection.close()

# Homepagina route
@app.route('/')
def home():
    return render_template('index.html')

# Loginpagina route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if is_logged_in():  # Controleer of de gebruiker al ingelogd is
        return redirect(url_for('voortgang'))  # Stuur de gebruiker naar de voortgang pagina

    # Verkrijg de 'next' parameter uit de URL of stel de voortgangpagina in als default
    next_page = request.args.get('next', url_for('voortgang'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Controleer de inloggegevens
        if validate_user(username, password):
            session.permanent = True
            session['username'] = username
            return redirect(next_page)  # Redirect naar de 'next' pagina (bijv. voortgang)

        else:
            error = "Invalid username or password. Please try again."
            return render_template('login.html', error=error)

    return render_template('login.html')
# Voortgang route
@app.route('/voortgang')
def voortgang():
    if is_logged_in():
        username = session['username']
        return render_template('voortgang.html', username=username)
    else:
        return redirect(url_for('login', next=request.url))


# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)  # Verwijder de gebruiker uit de sessie
    print("User logged out.")  # Debugging log
    return redirect(url_for('home'))  # Redirect naar de homepagina


# FAQ route
@app.route('/FAQ')
def FAQ():
    if is_logged_in():  # Controleer of de gebruiker is ingelogd
        return render_template('FAQ.html', username=session['username'])
    else:
        return redirect(url_for('login', next=request.url))

# Succesvol route
@app.route('/succesvol')
def succesvol():
    return render_template('succesvol.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if not is_logged_in():  # Controleer of de gebruiker ingelogd is
        return redirect(url_for('login'))  # Redirect naar loginpagina als niet ingelogd

    if request.method == 'POST':
        print("POST request received")  # Debugging print
        # Verwerk formuliergegevens
        return redirect(url_for('succesvol'))  # Redirect naar succesvol pagina na formulierverwerking

    # Als de gebruiker ingelogd is, toon de contactpagina
    return render_template('contact.html')
# training route
@app.route('/training')
def training():
    if is_logged_in():
        return render_template('training.html', username=session['username'])
    else:
        # Stuur de 'next' parameter mee naar de loginpagina
        return redirect(url_for('login', next=request.url))

# Events route
@app.route('/events')
def events():
    if is_logged_in():  # Controleer of de gebruiker is ingelogd
        return render_template('events.html', username=session['username'])
    else:
        return redirect(url_for('login', next=request.url))
@app.route('/eventssuccesful', methods=['GET', 'POST'])
def eventssuccesful():
    if is_logged_in():  # Controleer of de gebruiker is ingelogd
        if request.method == 'POST':
            # Verwerk de POST-verzoek (bijvoorbeeld registratie)
            return render_template('eventssuccesful.html', success=True, username=session['username'])
        return render_template('eventssuccesful.html', username=session['username'])  # Standaard GET
    else:
        return redirect(url_for('login', next=request.url))  # Redirect naar login als niet ingelogd

# Registratiepagina route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Controleer of de gebruikersnaam al bestaat in de database
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()
        connection.close()

        if existing_user:
            error = "Username already exists. Please choose another one."
            return render_template('register.html', error=error)

        # Voeg de nieuwe gebruiker toe aan de database
        add_user(username, password)

        # Log de gebruiker direct in na registratie
        session.permanent = True
        session['username'] = username
        return redirect(url_for('voortgang'))

    return render_template('register.html')
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
