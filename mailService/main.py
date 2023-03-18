from flask import Flask,jsonify,abort



app= Flask(__name__)


@app.route('/mailservice')
def index():
    return "HELLO"


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
    