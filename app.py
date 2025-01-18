from flask import Flask, render_template
import os
print("Static folder:", os.path.abspath('static'))
app = Flask(__name__, static_url_path='/static', static_folder='static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html') 

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
