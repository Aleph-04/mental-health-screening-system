from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("login.html")
    
@app.route("/login.html")
def login():
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/user_take_evaluation")
def user_take_evaluation():
    return render_template("user_take_evaluation.html")

@app.route("/charts.html")
def charts():
    return render_template("charts.html")

@app.route("/edit-evaluation-form")
def edit_evaluation_form():
    return render_template("edit-evaluation-form.html")

if __name__ == '__main__':
    app.run(debug=True)