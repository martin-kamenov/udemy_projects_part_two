import os
import requests
from datetime import datetime

GENDER = "male"
AGE = "32"
WEIGHT_KG = 100
HEIGHT_CM = 168

USER_NAME = os.environ["USER_NAME"]
PASSWORD = os.environ["PASSWORD"]
TOKEN = os.environ["TOKEN"]
APP_ID = os.environ["APP_ID"]
APP_KEY = os.environ["APP_KEY"]
SHEET_ENDPOINT = os.environ["SHEET_ENDPOINT"]

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

exercise_text = input("Tell me which exercises you did today: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": APP_KEY,
}

exercise_json = {
    "query": exercise_text,
    "gender": GENDER,
    "age": AGE,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
}

response = requests.post(url=exercise_endpoint, json=exercise_json, headers=headers)
result = response.json()

today = datetime.now()
today_date = today.strftime("%d/%m/%Y")
time_now = today.strftime("%X")

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "exercise": exercise["user_input"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
            "date": today_date,
            "time": time_now,
        }
    }

    #No Authentication
    # sheet_response = requests.post(url=workout_endpoint, json=sheet_inputs)

    #Basic Authentication
    sheet_response = requests.post(
        SHEET_ENDPOINT,
        json=sheet_inputs,
        auth=(
            USER_NAME,
            PASSWORD
        )
    )

    #Bearer Token Authentication
    # bearer_headers = {
    #     "Authorization": f"Bearer {TOKEN}"
    # }
    # sheet_response = requests.post(
    #     workout_endpoint,
    #     json=sheet_inputs,
    #     headers=bearer_headers
    # )

    print(sheet_response.text)