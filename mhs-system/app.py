from flask import Flask, render_template
import sqlite3

from database import initialize_db

app = Flask(__name__)

initialize_db()

@app.route('/')
def home():
    return render_template("student_login.html")

@app.route("/admin")
def admin_login():
    return render_template("admin_login.html")

@app.route("/evaluation")
def student_take_evaluation():
    return render_template("student_take_evaluation.html")

@app.route("/dashboard")
def dashboard():
    return render_template("admin_dashboard.html")

@app.route("/stats")
def stats():
    return render_template("admin_statistics.html")

@app.route("/edit-evaluation-form")
def edit_evaluation_form():
    return render_template("admin_edit-evaluation-form.html")

@app.route("/view-forms")
def view_forms():
    return render_template("admin_view-forms.html")

@app.route("/results")
def results():
    return render_template("admin_results.html")

@app.route("/evaluation")
def student_evaluation():
    return render_template("student_evaluation_form.html")

if __name__ == '__main__':
    app.run(debug=True)