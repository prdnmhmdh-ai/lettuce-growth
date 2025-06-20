from flask import Flask, send_from_directory
import os

app = Flask(__name__, static_folder='assets')

@app.route("/")
def index():
    return send_from_directory(os.getcwd(), "index.html")

if __name__ == '__main__':
    app.run(debug=True)