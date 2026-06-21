from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Secure Authentication System Project"

if __name__ == '__main__':
    app.run(debug=True)
