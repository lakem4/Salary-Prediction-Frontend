import os
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

api_url = os.environ.get(
    "API_URL",
    "http://127.0.0.1:5002/predict"
)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", predicted_salary=None, error=None, form_data={})

@app.route("/predict", methods=["POST"])
def predict():
    try:
        form_data = {
            "age": request.form.get("age"),
            "gender": request.form.get("gender"),
            "country": request.form.get("country"),
            "highest_deg": request.form.get("highest_deg"),
            "coding_exp": request.form.get("coding_exp"),
            "title": request.form.get("title"),
            "company_size": request.form.get("company_size"),
        }

        response = requests.post(api_url, json=form_data, timeout=10)
        response.raise_for_status()

        result = response.json()
        predicted_salary = result.get("predicted_salary")

        return render_template(
            "index.html",
            predicted_salary=predicted_salary,
            error=None,
            form_data=form_data
        )

    except requests.exceptions.RequestException as e:
        return render_template(
            "index.html",
            predicted_salary=None,
            error=f"API connection error: {str(e)}",
            form_data=request.form
        )