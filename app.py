from flask import Flask, render_template, request, redirect
from prediction import predict
import os


app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        prediction = predict(**request.form)
        if prediction == 0:
            return redirect("nostroke")
        elif prediction == 1:
            return redirect("stroke")
        else:
            return render_template("home.html")
    if request.method == "GET":
        return render_template("home.html")


@app.route("/nostroke")
def result():
    return render_template('nostroke.html')


@app.route("/stroke")
def results():
    return render_template('stroke.html')


if __name__ == "__main__":
    app.run(debug=True, port=8000)
