import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

GEMINI_KEY = os.environ.get('GEMINI_API_KEY', '')
GEMINI_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent'


@app.route('/ping')
def ping():
    return jsonify({'ok': True})


@app.route('/gemini', methods=['POST'])
def gemini_proxy():
    if not GEMINI_KEY:
        return jsonify({'error': 'GEMINI_API_KEY no configurada en el servidor'}), 500
    try:
        body = request.get_json()
        r = requests.post(f'{GEMINI_URL}?key={GEMINI_KEY}', json=body, timeout=90)
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
