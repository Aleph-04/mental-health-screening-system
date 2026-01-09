from flask import Flask, render_template, request, redirect, url_for
from database import initialize_db, insert_to_responses, insert_to_predictions, fetch_result, count_records ## import functions from database.py ###
from logistic_regression import load_phq9_model, make_phq9_prediction, make_gad7_prediction, load_gad7_model ## import functions from logistic_regression.py ###

app = Flask(__name__)

print("Hello from app.py")
initialize_db()
load_phq9_model()
load_gad7_model()


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
    row = count_records()
    return render_template("admin_dashboard.html", row=row)

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
    
    ### SBQ-R (optional, additive)
    sbqr1 = int(request.form.get('sbq1', 0))
    sbqr2 = int(request.form.get('sbq2', 0))
    sbqr3 = int(request.form.get('sbq3', 0))
    sbqr4 = int(request.form.get('sbq4', 0))

    sbqr_risk = "HIGH" if sbqr_total >= 7 else "LOW" ### pati ja


    sbqr_total = sbqr1 + sbqr2 + sbqr3 + sbqr4  ### ja turoka bi lor

    ### Make Predictions (e.g low, moderate, high , severe) ###
    phq9_prediction = make_phq9_prediction(phq1, phq2, phq3, phq4, phq5, phq6, phq7, phq8, phq9)
    gad7_prediction = make_gad7_prediction(gad1, gad2, gad3, gad4, gad5, gad6, gad7)
    
    
    insert_to_responses(
            first_name, middle_name, last_name, email_address,
            phq1, phq2, phq3, phq4, phq5, phq6, phq7, phq8, phq9,
            gad1, gad2, gad3, gad4, gad5, gad6, gad7,
            sbqr1, sbqr2, sbqr3, sbqr4, sbqr_total, sbqr_risk
        )
    
    insert_to_predictions(
        full_name, "N/A", "N/A", phq9_prediction, gad7_prediction
    )
    
    print("Data inserted to database for ", first_name, flush=True)
    return redirect(url_for("student_take_evaluation"))
    

if __name__ == '__main__':
    app.run(debug=True)