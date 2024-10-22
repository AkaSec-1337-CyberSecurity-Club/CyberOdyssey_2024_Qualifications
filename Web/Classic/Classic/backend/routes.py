import os
from flask import Flask, request, jsonify

app = Flask(__name__)

users = {}
current_secret = os.getenv('FLAG_SECRET', '')

@app.route('/register', methods=['POST'])
def register():
    if len(users) > 300:
        users.clear()
    data = request.json
    username = data.get('username')
    isAdmin = data.get('isAdmin', False)
    note = data.get('note')

    if username in users:
        return "Username already registered.", 200
    print(f"username: {username}, users: {users}")
    users[username] = {"isAdmin": isAdmin, "note": note}
    return "User registered successfully!", 200

@app.route('/users', methods=['GET'])
def list_users():
    return jsonify(users), 200

@app.route('/flag.txt', methods=['GET'])
def get_flag():
    secret_param = request.args.get('secret')
    if secret_param == current_secret:
        return os.getenv('FLAG', 'FLAG{TEST}'), 200
    return "Invalid secret.", 200
