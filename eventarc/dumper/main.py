import json
import os

from flask import Flask, request


PORT = int(os.environ.get('PORT', '8080'))

app = Flask(__name__)


@app.post("/")
def handle():
    event = {
        "headers": {k: v for k, v in request.headers.items()},
        "body": request.get_json(),
    }
    print(json.dumps(event))
    return "ok", 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=PORT)
