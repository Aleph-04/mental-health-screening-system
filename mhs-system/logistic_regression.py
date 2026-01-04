import joblib

def load_phq9_model():
    loaded_model = joblib.load("logistic_regression_model_phq9.pkl")
    print("PHQ9 Model loaded successfully.")
    return loaded_model

def load_sbqr_model():
    loaded_model = joblib.load("logistic_regression_model_sbqr.pkl")
    print("SBQR Model loaded successfully.")
    return loaded_model

def load_gad7_model():
    loaded_model = joblib.load("logistic_regression_model_gad7.pkl")
    print("GAD7 Model loaded successfully.")
    return loaded_model






def make_phq9_prediction(phq1, phq2, phq3, phq4, phq5, phq6, phq7, phq8, phq9):
    model = load_phq9_model()
    input_data = [[phq1, phq2, phq3, phq4, phq5, phq6, phq7, phq8, phq9]]
    prediction = model.predict(input_data)
    
    match prediction[0]:
        case 0:
            return "Mild"
        case 1:
            return "Moderate"
        case 2:
            return "Moderately Severe"
        case 3:
            return "Severe"

# def make_sbqr_prediction():
#     return None

def make_gad7_prediction(gad1, gad2, gad3, gad4, gad5, gad6, gad7):
    model = load_gad7_model()
    input_data = [[gad1, gad2, gad3, gad4, gad5, gad6, gad7]]
    prediction = model.predict(input_data)
    
    match prediction[0]:
        case 0:
            return "Mild"
        case 1:
            return "Moderate"
        case 2:
            return "Moderately Severe"
        case 3:
            return "Severe"