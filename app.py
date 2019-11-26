from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def root():
    return jsonify(['Hello', 'World'])

@app.route('/excerpts')
def list():
    print('Have a Get request from client')
    return jsonify([
        "The enormous room on the ground floor faced"
    ])

if __name__ == "__main__":
    app.run(debug=True)

