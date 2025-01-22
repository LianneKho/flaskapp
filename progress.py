from flask import Flask, request, jsonify

app = Flask(__name__)

# Mock data om de voortgang op te slaan
user_progress = {
    "tasks_done": []
}


@app.route('/api/progress', methods=['GET', 'POST'])
def progress():
    if request.method == 'POST':
        # Ontvang JSON-gegevens van de client
        data = request.get_json()
        user_progress['tasks_done'] = data.get('tasks_done', [])
        return jsonify({"message": "Progress saved successfully"}), 200

    # Bij GET: Stuur de voortgang terug
    return jsonify(user_progress), 200


if __name__ == '__main__':
    app.run(debug=True)