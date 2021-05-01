from flask import Flask, render_template, request, redirect
from prediction import predict
import os


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/result", methods=["POST", "GET"])
def result():
    if request.method == "POST":
        prediction = predict(**request.form)
        if prediction == 0:
            return render_template('nostroke.html')
        elif prediction == 1:
            return render_template('stroke.html')
        else:
            return redirect("/")
    if request.method == "GET":
        return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=8000)
