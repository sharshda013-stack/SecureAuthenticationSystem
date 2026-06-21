import bcrypt
import jwt
import datetime
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Secret Key (JWT ke liye)
app.config['SECRET_KEY'] = 'mysecretkey123'

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ---------------- DATABASE MODEL ----------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


# ---------------- HOME ----------------
@app.route('/')
def home():
    return "Secure Authentication System Running ✔️"


# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            return "Username already exists!"

        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        )

        new_user = User(
            username=username,
            password=hashed_password.decode('utf-8')
        )

        db.session.add(new_user)
        db.session.commit()

        return f"User {username} registered successfully ✔️"

    return render_template('register.html')


# ---------------- LOGIN (JWT) ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.checkpw(
            password.encode('utf-8'),
            user.password.encode('utf-8')
        ):

            token = jwt.encode(
                {
                    'username': username,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
                },
                app.config['SECRET_KEY'],
                algorithm='HS256'
            )

            return f"Login Successful ✔️ Token: {token}"

        return "Invalid Username or Password ❌"

    return render_template('login.html')


# ---------------- RUN APP ----------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
