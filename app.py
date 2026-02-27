from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET")

client = MongoClient(os.getenv("MONGO_URI"))
db = client.studyspots
collection = db.spots

@app.route("/")
def index():
    spots = list(collection.find())
    return render_template("index.html", spots=spots)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        spot = {
            "name": request.form["name"],
            "location": request.form["location"],
            "noise": request.form["noise"]
        }
        collection.insert_one(spot)
        return redirect(url_for("index"))
    return render_template("add.html")

@app.route("/clear", methods=["POST"])
def clear_all():
    collection.delete_many({})
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)