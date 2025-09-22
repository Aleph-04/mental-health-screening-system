from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/stats")
def stats():
    return render_template("statistics.html")

@app.route("/edit-evaluation-form")
def edit_evaluation_form():
    return render_template("edit-evaluation-form.html")

@app.route("/view-forms")
def view_forms():
    return render_template("view-forms.html")

@app.route("/results")
def results():
    return render_template("results.html")

if __name__ == '__main__':
    app.run(debug=True)