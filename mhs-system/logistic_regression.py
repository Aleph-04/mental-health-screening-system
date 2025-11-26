import joblib

def load_trained_model():
    loaded_model = joblib.load("logistic_regression_model.pkl")
    
    
    print("Model loaded successfully.")
    return loaded_model

def make_prediction(phq1, phq2, phq3, phq4, phq5, phq6, phq7, phq8, phq9):
    model = load_trained_model()
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
    