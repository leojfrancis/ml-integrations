import joblib
import os
import numpy as np
import pickle

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


def predict(**kwargs):
    gender = int(kwargs.get('gender'))
    age = int(kwargs.get('age'))
    hypertension = int(kwargs.get('hypertension'))
    heart_disease = int(kwargs.get('heart_disease'))
    ever_married = int(kwargs.get('ever_married'))
    work_type = int(kwargs.get('work_type'))
    residence_type = int(kwargs.get('Residence_type'))
    avg_glucose_level = float(kwargs.get('avg_glucose_level'))
    bmi = float(kwargs.get('bmi'))
    smoking_status = int(kwargs.get('smoking_status'))

    x = np.array([gender, age, hypertension, heart_disease, ever_married, work_type, residence_type,
                  avg_glucose_level, bmi, smoking_status]).reshape(1, -1)
    scaler_path = os.path.join(PROJECT_DIR,"models/scalar1.pkl")
    scaler = None
    with open(scaler_path, 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)
    
    x = scaler.transform(x)

    model_path = os.path.join(PROJECT_DIR,"models/svm.sav")
    dt = joblib.load(model_path)

    Y_pred = dt.predict(x)
    return Y_pred[0]