from flask import Flask, render_template, request, redirect, url_for, session
import os
# Dummy gebruikersgegevens (je kunt deze later vervangen door een database)
users = {
    "emp1": "password123",
    "emp2": "welcome2025"
}


app = Flask(__name__, static_url_path='/static', static_folder='static')
app.secret_key = os.urandom(24)

# Homepagina route
@app.route('/')
def home():
    return render_template('index.html')

# Loginpagina route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Controleer of de gebruikersgegevens kloppen
        if username in users and users[username] == password:
            session['username'] = username  # Sla de gebruikersnaam op in de sessie
            return redirect(url_for('voortgang'))  # Redirect naar het voortgang
        else:
            error = "Invalid username or password. Please try again."
            return render_template('login.html', error=error)

    return render_template('login.html')

# voortgang route
@app.route('/voortgang')
def voortgang():
    # Controleer of de gebruiker is ingelogd
    if 'username' in session:
        username = session['username']
        return render_template('voortgang.html', username=username)
    else:
        return redirect(url_for('login'))

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)  # Verwijder de gebruiker uit de sessie
    return redirect(url_for('home'))  # Redirect naar de homepagina

# FAQ route
@app.route('/FAQ')
def FAQ():
    return render_template('FAQ.html')

# Contact route
@app.route('/contact')
def contact():
    return render_template('contact.html') 

# training route
@app.route('/training')
def training():
    return render_template('training.html') 

# Events route
@app.route('/events')
def events():
    return render_template('events.html') 

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)