from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import fetch_code_responses, check_student_status, authenticate_student, count_by_college, fetch_all_responses, fetch_responses, delete_entry, admin_authenticate, initialize_db, insert_to_responses, insert_to_predictions, fetch_result, count_records
from logistic_regression import load_phq9_model, make_phq9_prediction, make_gad7_prediction, load_gad7_model, make_sbqr_prediction
import random
import string
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for flash messages; and session.

# ------------------- MAIL CONFIG -------------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'mykekieran.alfane@antiquespride.edu.ph'  # <-- replace
app.config['MAIL_PASSWORD'] = 'erqylyfomebaqbwd'     # <-- replace
app.config['MAIL_DEFAULT_SENDER'] = 'mykekieran.alfane@antiquespride.edu.ph'

mail = Mail(app)

# ------------------- INITIALIZE -------------------
print("Hello from app.py")
initialize_db()
from database import initialize_registration_db
initialize_registration_db()
load_phq9_model()
load_gad7_model()

# ------------------- ROUTES -------------------

@app.route('/', methods=['GET', 'POST'])
def home():
    session.clear()
    
    if request.method == 'POST':
        code = request.form['login_code']
        session["session_code"] = code
        
        if authenticate_student(code):
            session["user"] = "student"
            if check_student_status(code) == "submitted": ### (check if student has already submitted an evaluation)b
                print("STUDENT ALREADY SUBMITTED")
                return redirect(url_for('student_view_evaluation'))
            
            return redirect(url_for('student_evaluation'))
        
        else:
            return render_template("student_login.html", message="Invalid code. Please try again.")
            
    return render_template("student_login.html")

@app.route("/admin", methods=['GET', 'POST'])
def admin_login():
    session.clear()
    message  = ""   
    if request.method == 'POST':
        username = request.form['admin_username']
        password = request.form['admin_password']
        print(username + " " + password)
        try:
            auth = admin_authenticate(username, password)
        except Exception as e:
            return render_template("error.html")
        if auth:
            session["user"] = "admin"
            return redirect(url_for("dashboard"))
        else:
            message = "Invalid username or password"
    return render_template("admin_login.html", message=message)

@app.route("/dashboard")
def dashboard():
    row = count_records()
    bar_graph_data = [count_by_college("CCIS"),
                      count_by_college("CEA"),
                      count_by_college("CBA"),
                      count_by_college("CMS"),
                      count_by_college("CHS"),
                      count_by_college("CIT"),]
    
    try:
        if session["user"] != "admin":
            flash("Unauthorized access. Please log in as admin.", "danger")
            return redirect(url_for("admin_login"))
        
        return render_template("admin_dashboard.html", row=row, bar_graph_data=bar_graph_data)
    
    except KeyError:
        return render_template("404notfound.html", message="404 not found.")

@app.route("/manage")
def manage():
    row = fetch_all_responses()
    
    try:
        if session["user"] != "admin":
            return render_template("404notfound.html", message="404 not found.")
        
        return render_template("admin_manage_users.html", row=row)
    
    except KeyError:
        return render_template("404notfound.html", message="404 not found.")

# ------ Redundant routes. remove later (sidebar.html ln32 will cause an error tho) ------
@app.route("/edit-evaluation-form")
def edit_evaluation_form():
    return render_template("admin_edit-evaluation-form.html")

@app.route("/view-forms")
def view_forms():
    return render_template("admin_view-forms.html")
# ----------------------------------------- #

@app.route("/results")
def results():
    row = fetch_all_responses()
    
    try:
        if session["user"] != "admin":
            return render_template("404notfound.html", message="404 not found.")
        
        return render_template("admin_results.html", row=row)
    except KeyError:
        return render_template("404notfound.html", message="404 not found.")

@app.route("/evaluation")
def student_evaluation():
    try:
        if not session.get("user"):
            return render_template("404notfound.html", message="404 not found.")
        
        return render_template("student_take_evaluation.html")
    except KeyError:
        return render_template("404notfound.html", message="404 not found.")
    
@app.route("/student-view-evaluation")
def student_view_evaluation():
    code = session.get("session_code")
    
    entry_id = fetch_code_responses(code)
    first_name = entry_id[0]['first_name']
    middle_name = entry_id[0]['middle_name']
    last_name = entry_id[0]['last_name']
    email_address = entry_id[0]['email_address']

    phq1_response = entry_id[0]['phq1']
    phq2_response = entry_id[0]['phq2']
    phq3_response = entry_id[0]['phq3']
    phq4_response = entry_id[0]['phq4']
    phq5_response = entry_id[0]['phq5']
    phq6_response = entry_id[0]['phq6']
    phq7_response = entry_id[0]['phq7']
    phq8_response = entry_id[0]['phq8']
    phq9_response = entry_id[0]['phq9']

    gad1_response = entry_id[0]['gad1']
    gad2_response = entry_id[0]['gad2']
    gad3_response = entry_id[0]['gad3']
    gad4_response = entry_id[0]['gad4']
    gad5_response = entry_id[0]['gad5']
    gad6_response = entry_id[0]['gad6']
    gad7_response = entry_id[0]['gad7']
    
    sbqr1_response = entry_id[0]['sbqr1']
    sbqr2_response = entry_id[0]['sbqr2']
    sbqr3_response = entry_id[0]['sbqr3']
    sbqr4_response = entry_id[0]['sbqr4']
    
    
    try:
        if not session.get("user"):
            return render_template("404notfound.html", message="404 not found.")
        
        return render_template("student_view_evaluation.html",
                               first_name=first_name,
                               middle_name=middle_name,
                               last_name=last_name, 
                               email_address=email_address,
                               phq1_response=phq1_response,
                               phq2_response=phq2_response,
                               phq3_response=phq3_response,
                               phq4_response=phq4_response,
                               phq5_response=phq5_response,
                               phq6_response=phq6_response,
                               phq7_response=phq7_response,
                               phq8_response=phq8_response,
                               phq9_response=phq9_response,
                               gad1_response=gad1_response,
                               gad2_response=gad2_response,
                               gad3_response=gad3_response,
                               gad4_response=gad4_response,
                               gad5_response=gad5_response,
                               gad6_response=gad6_response,
                               gad7_response=gad7_response,
                               sbqr1_response=sbqr1_response,
                               sbqr2_response=sbqr2_response,
                               sbqr3_response=sbqr3_response,
                               sbqr4_response=sbqr4_response,
                               )
        
    except KeyError:
        return render_template("404notfound.html", message="404 not found.")

# ------------------- NEW REGISTER ROUTE -------------------
@app.route("/student-register", methods=['GET', 'POST'])
def student_register():
    if request.method == "POST":
        email = request.form['email']

        # generate 6-digit code
        code = ''.join(random.choices(string.digits, k=6))

        # save to DB
        from database import insert_registration_code
        insert_registration_code(email, code)

        # send email
        msg = Message(
            subject="Your Registration Code",
            recipients=[email],
            body=f"Hello! Your registration code is: {code}\n\nDo not share it with anyone."
        )
        mail.send(msg)

        flash("Registration code sent to your email!", "success")
        return redirect(url_for("home"))

    return render_template("student_register.html")

# ------------------- SUBMIT EVALUATION TO DATABASE -------------------
@app.route("/evaluation", methods=['GET', 'POST'])
def submit_to_database():
    full_name = request.form['inputFirstName'] + " " + request.form['inputLastName']
    first_name = request.form['inputFirstName']
    college = "N/A"
    age = "N/A"
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
    
    ### SBQ-R ()
    sbqr1 = int(request.form.get('sbq1', 0))
    sbqr2 = int(request.form.get('sbq2', 0))
    sbqr3 = int(request.form.get('sbq3', 0))
    sbqr4 = int(request.form.get('sbq4', 0))
    
    code = session.get("session_code")

    ### Make Predictions (e.g low, moderate, high , severe) ###
    phq9_prediction = make_phq9_prediction(phq1, phq2, phq3, phq4, phq5, phq6, phq7, phq8, phq9)
    gad7_prediction = make_gad7_prediction(gad1, gad2, gad3, gad4, gad5, gad6, gad7)
    sbqr_prediction = make_sbqr_prediction(sbqr1, sbqr2, sbqr3, sbqr4)
    
    insert_to_responses(
            first_name, middle_name, last_name, email_address,
            phq1, phq2, phq3, phq4, phq5, phq6, phq7, phq8, phq9,
            gad1, gad2, gad3, gad4, gad5, gad6, gad7,
            sbqr1, sbqr2, sbqr3, sbqr4, code
        )
    
    insert_to_predictions(
        full_name, college, age, phq9_prediction, gad7_prediction, sbqr_prediction
    )
    
    print("Data inserted to database for ", first_name, flush=True)
    return redirect(url_for("student_evaluation"))

# ------------------- ADMIN VIEW ---------boto----------
@app.route("/admin-view-evaluation", methods=['GET', 'POST'])
def admin_view_evaluation():
    if request.method == 'POST':
        if "view_button" in request.form:
            id = request.form['view_button']
            print("Viewing evaluation for ID:", id)
            
            entry_id = fetch_responses(id)
            entry_results = fetch_result(id)

            first_name = entry_id[0]['first_name']
            middle_name = entry_id[0]['middle_name']
            last_name = entry_id[0]['last_name']
            email_address = entry_id[0]['email_address']

            phq1_response = entry_id[0]['phq1']
            phq2_response = entry_id[0]['phq2']
            phq3_response = entry_id[0]['phq3']
            phq4_response = entry_id[0]['phq4']
            phq5_response = entry_id[0]['phq5']
            phq6_response = entry_id[0]['phq6']
            phq7_response = entry_id[0]['phq7']
            phq8_response = entry_id[0]['phq8']
            phq9_response = entry_id[0]['phq9']

            gad1_response = entry_id[0]['gad1']
            gad2_response = entry_id[0]['gad2']
            gad3_response = entry_id[0]['gad3']
            gad4_response = entry_id[0]['gad4']
            gad5_response = entry_id[0]['gad5']
            gad6_response = entry_id[0]['gad6']
            gad7_response = entry_id[0]['gad7']
            
            sbqr1_response = entry_id[0]['sbqr1']
            sbqr2_response = entry_id[0]['sbqr2']
            sbqr3_response = entry_id[0]['sbqr3']
            sbqr4_response = entry_id[0]['sbqr4']
            
            phq9_result = entry_results[0]['phq9_result']
            gad7_result = entry_results[0]['gad7_result']
            sbqr_result = entry_results[0]['sbqr_result']
            
        if "delete_entry" in request.form:
            id = request.form['delete_entry']
            print("Deleting evaluation for ID:", id)
            delete_entry(id)
            return redirect(url_for("results"))
        
        return render_template("admin_view_evaluation.html", id=id,
                               first_name=first_name,
                               middle_name=middle_name,
                               last_name=last_name,
                               email_address=email_address,
                               phq1_response=phq1_response,
                               phq2_response=phq2_response,
                               phq3_response=phq3_response,
                               phq4_response=phq4_response,
                               phq5_response=phq5_response,
                               phq6_response=phq6_response,
                               phq7_response=phq7_response,
                               phq8_response=phq8_response,
                               phq9_response=phq9_response,
                               gad1_response=gad1_response,
                               gad2_response=gad2_response,
                               gad3_response=gad3_response,
                               gad4_response=gad4_response,
                               gad5_response=gad5_response,
                               gad6_response=gad6_response,
                               gad7_response=gad7_response,
                               sbqr1_response=sbqr1_response,
                               sbqr2_response=sbqr2_response,
                               sbqr3_response=sbqr3_response,
                               sbqr4_response=sbqr4_response,
                               phq9_result=phq9_result,
                               gad7_result=gad7_result,
                               sbqr_result=sbqr_result
                               )

if __name__ == '__main__':
    app.run(debug=True)
