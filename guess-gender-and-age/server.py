from flask import Flask, render_template
import requests


app = Flask(__name__)

def guess_gender(name):
    response = requests.get(url=f"https://api.genderize.io?name={name}")
    data = response.json()
    gender = data["gender"]
    return gender


def guess_age(name):
    response = requests.get(url=f"https://api.agify.io?name={name}")
    data = response.json()
    years = data['age']
    return years


@app.route("/guess/<string:searched_name>")
def guess(searched_name):
    predicted_gender = guess_gender(searched_name)
    predicted_age = guess_age(searched_name)

    return render_template(
        "index.html",
        name=searched_name,
        gender=predicted_gender,
        age=predicted_age
    )


if __name__ == "__main__":
    app.run(debug=True)