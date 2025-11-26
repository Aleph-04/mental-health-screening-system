from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from database import initialize_db, insert_to_responses, insert_to_predictions, fetch_result ## import functions from database.py ###
from logistic_regression import load_trained_model, make_prediction

app = Flask(__name__)

print("Hello from app.py")
initialize_db()
load_trained_model()


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
    print("IF YOU SEE THE THING BELOW THIS, THEN IT WORKS")
    row = fetch_result()
    return render_template("admin_results.html", row=row)

@app.route("/evaluation")
def student_evaluation():
    return render_template("student_evaluation_form.html")

### example for database insertion boi; once mag submit ang forms, ga run ang function nga ja.###
@app.route("/evaluation", methods=['GET', 'POST'])
def submit_to_database():
    full_name = request.form['inputFirstName'] + " " + request.form['inputLastName']
    first_name = request.form['inputFirstName']
    middle_name = request.form['inputMiddleName']
    last_name = request.form['inputLastName']
    email_address = request.form['inputEmailAddress']

    ### PHQ9
    phq1 = int(request.form.get('phq1', 0))
    phq2 = int(request.form.get('phq2', 0))
    phq3 = int(request.form.get('phq3', 0))
    phq4 = int(request.form.get('phq4', 0))
    phq5 = int(request.form.get('phq5', 0))
    phq6 = int(request.form.get('phq6', 0))
    phq7 = int(request.form.get('phq7', 0))
    phq8 = int(request.form.get('phq8', 0))
    phq9 = int(request.form.get('phq9', 0))

    ### GAD7
    gad1 = int(request.form.get('gad1', 0))
    gad2 = int(request.form.get('gad2', 0))
    gad3 = int(request.form.get('gad3', 0))
    gad4 = int(request.form.get('gad4', 0))
    gad5 = int(request.form.get('gad5', 0))
    gad6 = int(request.form.get('gad6', 0))
    gad7 = int(request.form.get('gad7', 0))
    

    prediction = make_prediction(phq1, phq2, phq3, phq4, phq5, phq6, phq7, phq8, phq9)
    
    
    insert_to_responses(
            first_name, middle_name, last_name, email_address,
            phq1, phq2, phq3, phq4, phq5, phq6, phq7, phq8, phq9,
            gad1, gad2, gad3, gad4, gad5, gad6, gad7
        )
    
    insert_to_predictions(
        full_name, "N/A", "N/A", prediction
    )
    
    print("Data inserted to database for ", first_name, flush=True)
    return redirect(url_for("student_take_evaluation"))
    

if __name__ == '__main__':
    app.run(debug=True)