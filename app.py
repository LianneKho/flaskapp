import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Render!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))  # Render zal de juiste poort toewijzen
    app.run(debug=True, host='0.0.0.0', port=port)