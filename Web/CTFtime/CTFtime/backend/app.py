import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/env/<name>')
def get_flag(name):
    return jsonify({"name": os.getenv(name, 'null')})

@app.route('/team/<int:id>')
def get_team(id):
    try:
        response = requests.get(f"https://ctftime.org/api/v1/teams/{id}/", headers={"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17"})
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({"error": f"Unable to fetch team data: {e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
