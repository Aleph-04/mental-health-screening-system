from flask import Flask, render_template, request, redirect, url_for, flash, session, Response
from database import (count_gad7_severe, count_phq9_severe, count_sbqr_positive, fetch_responses, 
                      fetch_code_responses, check_student_status, authenticate_student, count_by_college, 
                      fetch_all_responses, delete_entry, admin_authenticate, initialize_db, 
                      insert_to_responses, insert_to_predictions, fetch_result, count_records,
                      get_clinical_distribution, get_demographic_distribution, get_submission_trends,
                      get_recent_critical_cases, get_export_data, insert_feedback, fetch_feedback)
from logistic_regression import load_phq9_model, make_phq9_prediction, make_gad7_prediction, load_gad7_model, make_sbqr_prediction
import random
import string
import csv
import io
import sqlite3
import pandas as pd
from datetime import datetime
from flask_mail import Mail, Message

SYMPTOM_MAP = {
    'phq1': "Little interest or pleasure in doing things",
    'phq2': "Feeling down, depressed, or hopeless",
    'phq3': "Trouble falling or staying asleep, or sleeping too much",
    'phq4': "Feeling tired or having little energy",
    'phq5': "Poor appetite or overeating",
    'phq6': "Feeling bad about yourself, failure, or letting family down",
    'phq7': "Trouble concentrating on things",
    'phq8': "Moving or speaking slowly, or being too fidgety/restless",
    'phq9': "Thoughts of self-harm or that you'd be better off dead",
    'gad1': "Feeling nervous, anxious, or on edge",
    'gad2': "Not being able to stop or control worrying",
    'gad3': "Worrying too much about different things",
    'gad4': "Trouble relaxing",
    'gad5': "Being so restless that it is hard to sit still",
    'gad6': "Becoming easily annoyed or irritable",
    'gad7': "Feeling afraid as if something awful might happen"
}

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for flash messages; and session.

# ------------------- MAIL CONFIG -------------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ljadopina@antiquespride.edu.ph'  # <-- replace
app.config['MAIL_PASSWORD'] = 'xghgxfwoxxwqokyw'     # <-- replace
app.config['MAIL_DEFAULT_SENDER'] = 'ljadopina@antiquespride.edu.ph'

mail = Mail(app)

# ------------------- INITIALIZE -------------------
print("Hello from app.py")
initialize_db()
from database import initialize_registration_db
initialize_registration_db()
load_phq9_model()
load_gad7_model()

x = fetch_all_responses()
print("TESTING fetch_all_responses():", [i['code'] for i in x])

### for sidebar highlighting active page.
def is_active(endpoint):
    return "active" if request.endpoint == endpoint else ""

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
    try:
        if session.get("user") != "admin":
            flash("Unauthorized access. Please log in as admin.", "danger")
            return redirect(url_for("admin_login"))

        # Get filter parameter
        college_filter = request.args.get('college')
        if college_filter == 'all': college_filter = None

        records = count_records()
        sbqr_positive = count_sbqr_positive()
        gad7_severe = count_gad7_severe()
        phq9_severe = count_phq9_severe()
        
        # New analytics with filtering
        phq9_dist = get_clinical_distribution('phq9', college_filter)
        gad7_dist = get_clinical_distribution('gad7', college_filter)
        trends_data = get_submission_trends(college_filter)
        trends = trends_data['daily_data']
        trend_percent = trends_data['trend_percent']
        trend_direction = trends_data['trend_direction']
        critical_cases = get_recent_critical_cases(limit=5)
        
        bar_graph_data = [count_by_college("ccis"),
                          count_by_college("cea"),
                          count_by_college("cmg"),
                          count_by_college("cms"),
                          count_by_college("chs"),
                          count_by_college("cit"),]

        return render_template("admin_dashboard.html", 
                             is_active=is_active, 
                             records=records, 
                             sbqr_positive=sbqr_positive, 
                             gad7_severe=gad7_severe, 
                             phq9_severe=phq9_severe, 
                             bar_graph_data=bar_graph_data,
                             phq9_dist=phq9_dist,
                             gad7_dist=gad7_dist,
                             trends=trends,
                             trend_percent=trend_percent,
                             trend_direction=trend_direction,
                             critical_cases=critical_cases,
                             selected_college=college_filter or 'all')
    
    except Exception as e:
        import traceback
        print("!!! DASHBOARD ERROR !!!")
        traceback.print_exc()
        return render_template("404notfound.html", message="An error occurred while loading dashboard analytics.")

@app.route("/manage")
def manage():
    row = fetch_all_responses()
    
    try:
        if session["user"] != "admin":
            return render_template("404notfound.html", message="404 not found.")
        
        return render_template("admin_manage_users.html", is_active=is_active, row=row)
    
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

@app.route("/admin/export-csv")
def export_csv():
    try:
        if session.get("user") != "admin":
            return redirect(url_for("admin_login"))
        
        data = get_export_data()
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Headers
        writer.writerow(['Registration Code', 'First Name', 'Last Name', 'Sex', 'College', 'Year Level', 'Email', 'Submission Date', 'PHQ-9 Result', 'GAD-7 Result', 'SBQ-R Result'])
        
        for row in data:
            writer.writerow([
                row['code'], row['first_name'], row['last_name'], row['sex'], 
                row['college'].upper(), row['year_level'], row['email_address'], 
                row['submission_date'], row['phq9_result'], row['gad7_result'], row['sbqr_result']
            ])
            
        output.seek(0)
        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-disposition": "attachment; filename=mhs_clinical_export.csv"}
        )
    except Exception as e:
        print(f"Export error: {e}")
        return redirect(url_for("dashboard"))

@app.route("/admin/export/carelist")
def export_carelist():
    try:
        if session.get("user") != "admin":
            return redirect(url_for("admin_login"))
            
        conn = sqlite3.connect('database.db')
        
        # Querying responses and joining with predictions for High-Risk (Carelist) students
        query = """
            SELECT 
                r.code AS 'Student Code',
                r.last_name AS 'Last Name',
                r.first_name AS 'First Name',
                r.college AS 'College',
                p.phq9_result AS 'Depression (PHQ-9)',
                p.gad7_result AS 'Anxiety (GAD-7)',
                p.sbqr_result AS 'Suicide Risk (SBQ-R)'
            FROM responses r
            JOIN predictions p ON r.code = p.code
            WHERE p.phq9_result IN ('Moderately Severe', 'Severe')
               OR p.gad7_result IN ('Moderately Severe', 'Severe')
               OR p.sbqr_result = 'Positive'
            ORDER BY r.submission_date DESC
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        # Convert DataFrame to CSV
        output = io.StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        
        # Generate filename with current timestamp
        timestamp = datetime.now().strftime("%Y%m%d")
        filename = f"Carelist_Report_{timestamp}.csv"
        
        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        print(f"Carelist export error: {e}")
        return redirect(url_for("results"))

@app.route("/results")
def results():
    row = fetch_all_responses()
    
    try:
        if session["user"] != "admin":
            return render_template("404notfound.html")
        
        return render_template("admin_results.html", is_active=is_active, row=row)
    except KeyError:
        return render_template("404notfound.html")

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
    facebook = entry_id[0]['facebook']
    present_address = entry_id[0]['present_address']
    permanent_address = entry_id[0]['permanent_address']
    religion = entry_id[0]['religion']
    contact_number = entry_id[0]['contact_number']
    extension = entry_id[0]['extension']
    place_of_birth = entry_id[0]['place_of_birth']
    date_of_birth = entry_id[0]['date_of_birth']
    college = entry_id[0]['college']
    degree_program_college = entry_id[0]['degree_program_college']
    elementary_level = entry_id[0]['elementary_level']
    highest_education = entry_id[0]['college_level'] if entry_id[0]['college_level'] else (entry_id[0]['senior_high_school'] if entry_id[0]['senior_high_school'] else entry_id[0]['junior_high_school'] if entry_id[0]['junior_high_school'] else entry_id[0]['elementary_level'])
    
    year_attended_college = entry_id[0]['year_attended_college']
    year_attended_senior_high = entry_id[0]['year_attended_senior_high']
    year_attended_junior_high = entry_id[0]['year_attended_junior_high']
    year_attended_elementary = entry_id[0]['year_attended_elementary']
    
    basic_education_senior_high = entry_id[0]['basic_education_senior_high']
    basic_education_junior_high = entry_id[0]['basic_education_junior_high']
    basic_education_elementary = entry_id[0]['basic_education_elementary']
    
    honors_college = entry_id[0]['honors_college']
    honors_senior_high = entry_id[0]['honors_senior_high']
    honors_junior_high = entry_id[0]['honors_junior_high']
    honors_elementary = entry_id[0]['honors_elementary']
    name_of_mother = entry_id[0]['name_of_mother']
    occupation_of_mother = entry_id[0]['occupation_of_mother']
    mother_contact_number = entry_id[0]['mother_contact_number']
    name_of_father = entry_id[0]['name_of_father']
    occupation_of_father = entry_id[0]['occupation_of_father']
    father_contact_number = entry_id[0]['father_contact_number']
    
    disability_str = entry_id[0]['disability']
    applicable_str = entry_id[0]['applicable']
    
    sex = entry_id[0]['sex']
    civil_status = entry_id[0]['civil_status']

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
 id=id,
                               first_name=first_name,
                               middle_name=middle_name,
                               last_name=last_name,
                               email_address=email_address,
                               facebook=facebook,
                               present_address=present_address,
                               permanent_address=permanent_address,
                               religion=religion,
                               contact_number=contact_number,
                               extension=extension,
                               place_of_birth=place_of_birth,
                               date_of_birth=date_of_birth,
                               college=college,
                               degree_program_college=degree_program_college,
                               elementary_level=elementary_level,
                               highest_education=highest_education,
                               year_attended_college=year_attended_college,
                               year_attended_senior_high=year_attended_senior_high,
                               year_attended_junior_high=year_attended_junior_high,
                               year_attended_elementary=year_attended_elementary,
                               basic_education_senior_high=basic_education_senior_high,
                               basic_education_junior_high=basic_education_junior_high,
                               basic_education_elementary=basic_education_elementary,
                               honors_college=honors_college,
                               honors_senior_high=honors_senior_high,
                               honors_junior_high=honors_junior_high,
                               honors_elementary=honors_elementary,
                               name_of_mother=name_of_mother,
                               occupation_of_mother=occupation_of_mother,
                               mother_contact_number=mother_contact_number,
                               name_of_father=name_of_father,
                               occupation_of_father=occupation_of_father,
                               father_contact_number=father_contact_number,
                               disability=disability_str,
                               applicable=applicable_str,
                               sex=sex,
                               civil_status=civil_status,
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

# ---------------------------------------------------- SUBMIT EVALUATION TO DATABASE ------------------------------------------------------
@app.route("/evaluation", methods=['GET', 'POST'])
def submit_to_database():
    full_name = request.form['inputFirstName'] + " " + request.form['inputLastName']
    first_name = request.form['inputFirstName']
    college = college = request.form['college']
    age = "N/A"
    middle_name = request.form['inputMiddleName']
    last_name = request.form['inputLastName']
    email_address = request.form['inputEmailAddress']
    place_of_birth = request.form['place_of_birth']
    extension = request.form['extension']
    contact_number = request.form['contact_number']
    religion = request.form['religion']
    permanent_address = request.form['permanent_address']
    present_address = request.form['present_address']
    facebook = request.form['facebook']
    elementary_level = request.form['elementary_level']
    basic_education_elementary = request.form['basic_education_elementary']
    year_attended_elementary = request.form['year_attended_elementary']
    honors_elementary = request.form['honors_elementary']
    junior_high_school = request.form['junior_high_school']
    basic_education_junior_high = request.form['basic_education_junior_high']
    year_attended_junior_high = request.form['year_attended_junior_high']
    honors_junior_high = request.form['honors_junior_high']
    senior_high_school = request.form['senior_high_school']
    basic_education_senior_high = request.form['basic_education_senior_high']
    year_attended_senior_high = request.form['year_attended_senior_high']
    honors_senior_high = request.form['honors_senior_high']
    college_level = request.form['college_level']
    degree_program_college = request.form['degree_program_college']
    year_attended_college = request.form['year_attended_college']
    honors_college = request.form['honors_college']
    name_of_mother = request.form['name_of_mother']
    occupation_of_mother = request.form['occupation_of_mother']
    mother_contact_number = request.form['mother_contact_number']
    name_of_father = request.form['name_of_father']
    occupation_of_father = request.form['occupation_of_father']
    father_contact_number = request.form['father_contact_number']
    date_of_birth = request.form['date_of_birth']
    monthly_income = request.form['monthly_income']
    sex = request.form['sex']

    # --- ja ang PWD, IP, Solo Parent, OFW, LGBTQIA+, Working Student, Others) ---
    applicable = request.form.getlist('applicable[]')             # captures ALL checked values boss

    # Extra fields
    children_no = request.form.get('children_no', '')             # solo poarent children number
    applicable_other = request.form.get('applicable_other', '')   # "Other" text field

    # --- Disability checkboxes ---
    disability = request.form.getlist('disability[]')             # captures ALL checked values
    disability_other = request.form.get('disability_other', '')   # "other" text field

    # convert ya to strings for DB storage
    applicable_str = ", ".join(applicable)
    disability_str = ", ".join(disability)

    # append Solo Parent children number if provided
    if children_no and "Solo Parent" in applicable:
     applicable_str += f" (Children: {children_no})"

    # append "Other" values if provided
    if applicable_other:
     applicable_str += f", Other: {applicable_other}"
    if disability_other:
     disability_str += f", Other: {disability_other}"

    # --- Civil Status ---
    civil_status = request.form.get('civil_status', '')   # Single, Married, Widowed, Separated, Other
    civil_status_other = request.form.get('civil_status_other', '')

    # kung ang "Other" is chosen, append na text field
    if civil_status == "Other" and civil_status_other:
     civil_status = f"Other: {civil_status_other}"


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
            sex, monthly_income, date_of_birth, civil_status, father_contact_number,
            occupation_of_father, name_of_father, mother_contact_number, occupation_of_mother, name_of_mother,
            honors_college, year_attended_college, degree_program_college, college_level, honors_senior_high,
            year_attended_senior_high, basic_education_senior_high, senior_high_school, honors_junior_high,
            year_attended_junior_high, basic_education_junior_high, junior_high_school, honors_elementary,
            year_attended_elementary, basic_education_elementary, elementary_level, facebook, present_address,
            permanent_address, religion, contact_number, extension, place_of_birth, college, 
            phq1, phq2, phq3, phq4, phq5, phq6, phq7, phq8, phq9,
            gad1, gad2, gad3, gad4, gad5, gad6, gad7,
            sbqr1, sbqr2, sbqr3, sbqr4, applicable_str, disability_str, code
        )
    
    insert_to_predictions(
        code, full_name, college, age, phq9_prediction, gad7_prediction, sbqr_prediction
    )
    
    print("Data inserted to database for ", code, first_name, flush=True)
    return render_template("student_submitted.html") ### might change later 

# ------------------- ADMIN Dashboard > Results > View evaluation (blue button) ---------boto, guba pagid----------
@app.route("/admin-view-evaluation", methods=['GET', 'POST'])
def admin_view_evaluation():
    is_modal = request.args.get('modal') == '1'
    code = request.form.get('view_button') if request.method == 'POST' else request.args.get('code')
    
    if request.method == 'POST' and "delete_entry" in request.form:
        delete_code = request.form['delete_entry']
        print("Deleting evaluation for Code:", delete_code)
        delete_entry(delete_code)
        return redirect(url_for("results"))
        
    if code:
        if True: # Preserve original indentation block
            print("Viewing evaluation for Code:", code)

            entry_id = fetch_responses(code)
            entry_results = fetch_result(code)
            feedback = fetch_feedback(code)
            
            print(entry_id)
        

            first_name = entry_id[0]['first_name']
            middle_name = entry_id[0]['middle_name']
            last_name = entry_id[0]['last_name']
            email_address = entry_id[0]['email_address']
            facebook = entry_id[0]['facebook']
            present_address = entry_id[0]['present_address']
            permanent_address = entry_id[0]['permanent_address']
            religion = entry_id[0]['religion']
            contact_number = entry_id[0]['contact_number']
            extension = entry_id[0]['extension']
            place_of_birth = entry_id[0]['place_of_birth']
            date_of_birth = entry_id[0]['date_of_birth']
            college = entry_id[0]['college']
            degree_program_college = entry_id[0]['degree_program_college']
            elementary_level = entry_id[0]['elementary_level']
            highest_education = entry_id[0]['college_level'] if entry_id[0]['college_level'] else (entry_id[0]['senior_high_school'] if entry_id[0]['senior_high_school'] else entry_id[0]['junior_high_school'] if entry_id[0]['junior_high_school'] else entry_id[0]['elementary_level'])
            
            year_attended_college = entry_id[0]['year_attended_college']
            year_attended_senior_high = entry_id[0]['year_attended_senior_high']
            year_attended_junior_high = entry_id[0]['year_attended_junior_high']
            year_attended_elementary = entry_id[0]['year_attended_elementary']
            
            basic_education_senior_high = entry_id[0]['basic_education_senior_high']
            basic_education_junior_high = entry_id[0]['basic_education_junior_high']
            basic_education_elementary = entry_id[0]['basic_education_elementary']
            
            honors_college = entry_id[0]['honors_college']
            honors_senior_high = entry_id[0]['honors_senior_high']
            honors_junior_high = entry_id[0]['honors_junior_high']
            honors_elementary = entry_id[0]['honors_elementary']
            name_of_mother = entry_id[0]['name_of_mother']
            occupation_of_mother = entry_id[0]['occupation_of_mother']
            mother_contact_number = entry_id[0]['mother_contact_number']
            name_of_father = entry_id[0]['name_of_father']
            occupation_of_father = entry_id[0]['occupation_of_father']
            father_contact_number = entry_id[0]['father_contact_number']
            
            disability_str = entry_id[0]['disability'] or ""
            applicable_str = entry_id[0]['applicable'] or ""
            
            sex = entry_id[0]['sex']
            civil_status = entry_id[0]['civil_status']

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
            
            phq9_result = entry_results[0]['phq9_result'] or ""
            gad7_result = entry_results[0]['gad7_result'] or ""
            sbqr_result = entry_results[0]['sbqr_result'] or ""

            # --- XAI Logic: Extract Driving Symptoms (Score 2 or 3) ---
            driving_symptoms = []
            # PHQ-9 (1-8) - PHQ9 is treated separately as a red flag
            for i in range(1, 9):
                score = entry_id[0][f'phq{i}']
                if score is not None and score >= 2:
                    driving_symptoms.append({'text': SYMPTOM_MAP[f'phq{i}'], 'score': score})
            
            # GAD-7 (1-7)
            for i in range(1, 8):
                score = entry_id[0][f'gad{i}']
                if score is not None and score >= 2:
                    driving_symptoms.append({'text': SYMPTOM_MAP[f'gad{i}'], 'score': score})

            # Check for critical flags
            has_critical_warning = (
                (entry_id[0]['phq9'] is not None and entry_id[0]['phq9'] > 0) or
                (entry_id[0]['sbqr1'] is not None and entry_id[0]['sbqr1'] > 1) or  # In SBQ-R, higher values are riskier
                (entry_id[0]['sbqr2'] is not None and entry_id[0]['sbqr2'] > 1) or
                (entry_id[0]['sbqr3'] is not None and entry_id[0]['sbqr3'] > 1) or
                (entry_id[0]['sbqr4'] is not None and entry_id[0]['sbqr4'] > 1) or
                ("Severe" in phq9_result if phq9_result else False) or 
                ("Severe" in gad7_result if gad7_result else False) or 
                ("Positive" in sbqr_result if sbqr_result else False)
            )
            
        return render_template("admin_view_evaluation.html", id=code,
                               is_modal=is_modal,
                               first_name=first_name,
                               middle_name=middle_name,
                               last_name=last_name,
                               email_address=email_address,
                               facebook=facebook,
                               present_address=present_address,
                               permanent_address=permanent_address,
                               religion=religion,
                               contact_number=contact_number,
                               extension=extension,
                               place_of_birth=place_of_birth,
                               date_of_birth=date_of_birth,
                               college=college,
                               degree_program_college=degree_program_college,
                               elementary_level=elementary_level,
                               highest_education=highest_education,
                               year_attended_college=year_attended_college,
                               year_attended_senior_high=year_attended_senior_high,
                               year_attended_junior_high=year_attended_junior_high,
                               year_attended_elementary=year_attended_elementary,
                               basic_education_senior_high=basic_education_senior_high,
                               basic_education_junior_high=basic_education_junior_high,
                               basic_education_elementary=basic_education_elementary,
                               honors_college=honors_college,
                               honors_senior_high=honors_senior_high,
                               honors_junior_high=honors_junior_high,
                               honors_elementary=honors_elementary,
                               name_of_mother=name_of_mother,
                               occupation_of_mother=occupation_of_mother,
                               mother_contact_number=mother_contact_number,
                               name_of_father=name_of_father,
                               occupation_of_father=occupation_of_father,
                               father_contact_number=father_contact_number,
                               disability=disability_str,
                               applicable=applicable_str,
                               sex=sex,
                               civil_status=civil_status,
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
                               sbqr_result=sbqr_result,
                               driving_symptoms=driving_symptoms,
                               has_critical_warning=has_critical_warning,
                               feedback=feedback
                               )

@app.route("/admin/feedback/<string:student_code>", methods=["POST"])
def admin_feedback(student_code):
    if session.get("user") != "admin":
        return redirect(url_for('admin_login'))
        
    data = {
        'verified_phq9': request.form.get('verified_phq9'),
        'verified_gad7': request.form.get('verified_gad7'),
        'verified_sbqr': request.form.get('verified_sbqr'),
        'clinical_notes': request.form.get('clinical_notes')
    }
    
    insert_feedback(student_code, data)
    flash("Clinical feedback saved successfully.", "success")
    
    # Render the template directly with the updated feedback since redirecting to a POST route is not possible
    entry_id = fetch_responses(student_code)
    entry_results = fetch_result(student_code)
    feedback = fetch_feedback(student_code)
    
    if not entry_id:
        return redirect(url_for("results"))

    # Reuse the same local variables assignment as in admin_view_evaluation to re-render the page
    first_name = entry_id[0]['first_name']
    middle_name = entry_id[0]['middle_name']
    last_name = entry_id[0]['last_name']
    email_address = entry_id[0]['email_address']
    facebook = entry_id[0]['facebook']
    present_address = entry_id[0]['present_address']
    permanent_address = entry_id[0]['permanent_address']
    religion = entry_id[0]['religion']
    contact_number = entry_id[0]['contact_number']
    extension = entry_id[0]['extension']
    place_of_birth = entry_id[0]['place_of_birth']
    date_of_birth = entry_id[0]['date_of_birth']
    college = entry_id[0]['college']
    sex = entry_id[0]['sex']
    civil_status = entry_id[0]['civil_status']
    monthly_income = entry_id[0]['monthly_income']
    father_contact_number = entry_id[0]['father_contact_number']
    occupation_of_father = entry_id[0]['occupation_of_father']
    name_of_father = entry_id[0]['name_of_father']
    mother_contact_number = entry_id[0]['mother_contact_number']
    occupation_of_mother = entry_id[0]['occupation_of_mother']
    name_of_mother = entry_id[0]['name_of_mother']
    
    disability_str = entry_id[0]['disability'] or ""
    applicable_str = entry_id[0]['applicable'] or ""

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

    phq9_result = entry_results[0]['phq9_result'] or ""
    gad7_result = entry_results[0]['gad7_result'] or ""
    sbqr_result = entry_results[0]['sbqr_result'] or ""

    driving_symptoms = []
    for i in range(1, 10):
        score = entry_id[0][f'phq{i}']
        if score is not None and score >= 2:
            driving_symptoms.append({'text': SYMPTOM_MAP[f'phq{i}'], 'score': score})
    for i in range(1, 8):
        score = entry_id[0][f'gad{i}']
        if score is not None and score >= 2:
            driving_symptoms.append({'text': SYMPTOM_MAP[f'gad{i}'], 'score': score})

    has_critical_warning = (
        (entry_id[0]['phq9'] is not None and entry_id[0]['phq9'] > 0) or
        (entry_id[0]['sbqr1'] is not None and entry_id[0]['sbqr1'] > 1) or
        (entry_id[0]['sbqr2'] is not None and entry_id[0]['sbqr2'] > 1) or
        (entry_id[0]['sbqr3'] is not None and entry_id[0]['sbqr3'] > 1) or
        (entry_id[0]['sbqr4'] is not None and entry_id[0]['sbqr4'] > 1) or
        ("Severe" in phq9_result if phq9_result else False) or 
        ("Severe" in gad7_result if gad7_result else False) or 
        ("Positive" in sbqr_result if sbqr_result else False)
    )

    return render_template("admin_view_evaluation.html", id=student_code,
                           first_name=first_name,
                           middle_name=middle_name,
                           last_name=last_name,
                           email_address=email_address,
                           facebook=facebook,
                           present_address=present_address,
                           permanent_address=permanent_address,
                           religion=religion,
                           place_of_birth=place_of_birth,
                           date_of_birth=date_of_birth,
                           college=college,
                           contact_number=contact_number,
                           extension=extension,
                           monthly_income=monthly_income,
                           name_of_mother=name_of_mother,
                           occupation_of_mother=occupation_of_mother,
                           mother_contact_number=mother_contact_number,
                           name_of_father=name_of_father,
                           occupation_of_father=occupation_of_father,
                           father_contact_number=father_contact_number,
                           disability=disability_str,
                           applicable=applicable_str,
                           sex=sex,
                           civil_status=civil_status,
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
                           sbqr_result=sbqr_result,
                           driving_symptoms=driving_symptoms,
                           has_critical_warning=has_critical_warning,
                           feedback=feedback
                           )

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)

