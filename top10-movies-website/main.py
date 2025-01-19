from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from dotenv import load_dotenv
import requests
import os

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

API_KEY = os.getenv("API_KEY")
URL = "https://api.themoviedb.org/3/search/movie"
INFO_URL = "https://api.themoviedb.org/3/movie"
IMG_URL = "https://image.tmdb.org/t/p/w500"

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CREATE DB
class Base(DeclarativeBase):
    pass


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(250), nullable=True)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()


class RateMovieForm(FlaskForm):
    rating = StringField("Your Rating Out of 10 e.g. 7.5")
    review = StringField("Your Review")
    submit = SubmitField("Done")


class MovieTitleForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")


@app.route("/")
def home():
    all_movies = Movie.query.order_by(Movie.rating).all()
    movie_total = Movie.query.count()

    for movie in all_movies:
        movie.ranking = movie_total
        db.session.commit()
        movie_total -= 1

    return render_template("index.html", movies=all_movies)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = MovieTitleForm()

    if form.validate_on_submit():
        movie_title = form.title.data
        response = requests.get(URL, params={"api_key": API_KEY, "query": movie_title})
        data = response.json()["results"]
        return render_template("select.html", options=data)

    return render_template("add.html", form=form)



@app.route("/edit", methods=["GET", "POST"])
def rate_movie():
    form = RateMovieForm()
    movie_id = request.args.get("id")
    movie = db.get_or_404(Movie, movie_id)

    if form.validate_on_submit():
        movie.rating = float(form.rating.data)
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("edit.html", form=form, movie=movie)


@app.route("/delete")
def delete():
    movie_id = request.args.get("id")
    movie_to_delete = db.get_or_404(Movie, movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/find")
def find_movie():
    movie_api_id = request.args.get("id")
    if movie_api_id:
        movie_api_url = f"{INFO_URL}/{movie_api_id}"
        response = requests.get(movie_api_url, params={'api_key': API_KEY, "language": "en-US"})
        data = response.json()

        new_movie = Movie(
            title=data["title"],
            year=data["release_date"].split("-")[0],
            description=data["overview"],
            img_url=f"{IMAGE_URL}/{data['poster_path']}",
        )

        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for("rate_movie", id=new_movie.id))


# with app.app_context():
#     new_movie = Movie(
#         title='Phone Booth',
#         year=2002,
#         description="Publicist Stuart Shepard finds himself trapped in a phone booth, "
#                     "pinned down by an extortionist's sniper rifle. Unable to leave or "
#                     "receive outside help, Stuart's negotiation with the caller leads "
#                     "to a jaw-dropping climax.",
#         rating=7.3,
#         ranking=10,
#         review="My favourite character was the caller.",
#         img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
#     )
#     db.session.add(new_movie)
#     db.session.commit()

# with app.app_context():
#     second_movie = Movie(
#         title="Avatar the Way of Water",
#         year=2022,
#         description="Set more than a decade after the events of the first film, "
#                     "learn the story of the Sully family (Jake, Neytiri, and their kids), "
#                     "the trouble that follows them, the lengths they go to keep each other safe, "
#                     "the battles they fight to stay alive, and the tragedies they endure.",
#         rating=7.3,
#         ranking=9,
#         review="I liked the water.",
#         img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
#     )
#     db.session.add(second_movie)
#     db.session.commit()


# with app.app_context():
#     movie_id = 1
#     movie_to_delete = db.get_or_404(Movie, movie_id)
#     db.session.delete(movie_to_delete)
#     db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
