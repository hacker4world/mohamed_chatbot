from ai_assistant import ai_assistant

from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    return ai_assistant(data['prompt'])

if __name__ == '__main__':
    app.run(debug=True)