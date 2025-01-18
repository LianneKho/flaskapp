from flask import Flask, render_template
import os
print("Static folder:", os.path.abspath('static'))
app = Flask(__name__, static_url_path='/static', static_folder='static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/FAQ')
def FAQ():
    return render_template('FAQ.html')

@app.route('/contact')
def contact():
    return render_template('contact.html') 

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
