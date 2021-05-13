from flask import Flask, render_template, request, redirect, url_for
from prediction import Predict
import os


app = Flask(__name__)
app.config['DEBUG'] = True


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/process-csv", methods=["POST", "GET"])
def process_dataset():
    if request.method == "POST":
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join(
                "data_files", uploaded_file.filename))
    return render_template("")


@app.route("/result", methods=["POST", "GET"])
def result():
    if request.method == "POST":
        prediction = Predict(**request.form).predict()
        if prediction == 0:
            return render_template('nostroke.html')
        elif prediction == 1:
            return render_template('stroke.html')
        else:
            return redirect(url_for(home))
    if request.method == "GET":
        return redirect(url_for(home))


if __name__ == "__main__":
    app.run(debug=True, port=8000)
