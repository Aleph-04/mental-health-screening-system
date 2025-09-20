from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route("/login.html")
def login():
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/charts.html")
def charts():
    return render_template("charts.html")

@app.route("/edit-evaluation-form")
def edit_evaluation_form():
    return render_template("edit-evaluation-form.html")

if __name__ == '__main__':
    app.run(debug=True)