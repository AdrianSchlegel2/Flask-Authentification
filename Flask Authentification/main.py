from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from sqlalchemy import Column, Integer, String

app = Flask(__name__)

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True)
    password = Column(String(100))
    name = Column(String(1000))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    return render_template("index.html", logged_in=current_user.is_authenticated)


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        if not User.query.filter_by(email=email).first():
            password = request.form.get("password")
            hashed_password = generate_password_hash(password=password, method="pbkdf2:sha256", salt_length=8)
            new_user = User(
                email=email,
                password=hashed_password,
                name=name,
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("login"))
        else:
            return render_template("register.html", reason="email")
    else:
        return render_template("register.html")


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    elif request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()

        if email == "":
            pass

        elif user is not None:
            hashed_password = user.password

            if check_password_hash(pwhash=hashed_password, password=password):
                login_user(user)
                return redirect(url_for("secrets"))

            else:
                return render_template("login.html", reason="password")

        else:
            return render_template("login.html", reason="email")


@app.route('/secrets')
@login_required
def secrets():
    return render_template("secrets.html", logged_in=current_user.is_authenticated, user=current_user)


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))


@app.route('/download')
@login_required
def download():
    return send_from_directory(directory="static", filename="files/cheat_sheet.pdf")


if __name__ == "__main__":
    app.run(debug=True)
