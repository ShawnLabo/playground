import json
import os

from flask import Flask, request, jsonify


APP_NAME = os.environ['APP_NAME']
DEBUG = os.environ.get('DEBUG', 'false') == 'true'
PORT = int(os.environ.get('PORT', '8080'))

app = Flask(__name__)


@app.post("/")
def handle():
    body = json.loads(request.data)
    output = f'{APP_NAME}/{body["input"]}'
    return jsonify({'output': output})


if __name__ == '__main__':
    app.run(debug=DEBUG, host='0.0.0.0', port=PORT)
