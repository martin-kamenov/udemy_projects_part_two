from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

# CREATE DATABASE


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Configure Flask-Login's Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

# Create a user_loader callback
@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


# CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template("index.html", logged_in=current_user.is_authenticated)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        password = request.form.get("password")
        hashed_and_salted_password = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)
        new_user = User(
            email=request.form.get("email"),
            name=request.form.get("name"),
            password=hashed_and_salted_password
        )

        new_user_email_is_in_db = db.session.execute(db.select(User).where(User.email == new_user.email)).scalar()
        if new_user_email_is_in_db:
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for("login"))
        else:
            db.session.add(new_user)
            db.session.commit()

            # Log in and authenticate user after adding details to database.
            login_user(new_user)

            return redirect(url_for("secrets"))

    return render_template("register.html", logged_in=current_user.is_authenticated)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = db.session.execute(db.select(User).where(User.email == email)).scalar()

        if not user:
            flash("This email does not exist, please try again.")
            return redirect(url_for("login"))

        # Check stored password hash against entered password hashed.
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("secrets"))
        else:
            flash("Password incorrect, please try again")
            return redirect(url_for("login"))

    return render_template("login.html", logged_in=current_user.is_authenticated)


@app.route('/secrets')
@login_required
def secrets():
    print(current_user.name)
    # Passing the name from the current_user
    return render_template("secrets.html", name=current_user.name, logged_in = True)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route('/download', methods=["GET"])
@login_required
def download():
    return send_from_directory(
        directory="static",
        path="files/cheat_sheet.pdf",

    )


# @app.route("/delete")
# def delete():
#     all_users = db.session.execute(db.select(User)).scalars()
#     [db.session.delete(user) for user in all_users if user.email == "martenceto@abv.bg"]
#     db.session.commit()
#
#     return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
