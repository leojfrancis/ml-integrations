import joblib
import os
import numpy as np
import pickle
import enum

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


class GenderEnum(enum.Enum):
    Female = 0
    Male = 1


class ResidencyEnum(enum.Enum):
    Urban = 0
    Rural = 1


class WorkEnum(enum.Enum):
    Government = 0
    Never = 1
    Private = 2
    Self_employed = 3
    For_Children = 4


class SmokingStatusEnum(enum.Enum):
    Unknown = 0
    Formerly = 1
    Never = 2
    Smokes = 3


class CheckBoxEnum(enum.Enum):
    on = 1
    off = 0


class Predict:
    def __init__(self, **kwargs):
        self.gender = GenderEnum[kwargs.get('gender')].value
        self.age = int(kwargs.get('age'))
        self.hypertension=CheckBoxEnum[kwargs.get('hypertension')].value if 'hypertension' in kwargs else 0
        self.heart_disease=CheckBoxEnum[kwargs.get('heart_disease')].value if 'heart_disease' in kwargs else 0
        self.ever_married=CheckBoxEnum[kwargs.get('ever_married')].value if 'ever_maried' in kwargs else 0
        self.work_type=WorkEnum[kwargs.get('work_type')].value
        self.residence_type=ResidencyEnum[kwargs.get('Residence_type')].value
        self.avg_glucose_level=float(kwargs.get('avg_glucose_level'))
        self.bmi=float(kwargs.get('bmi'))
        self.smoking_status=SmokingStatusEnum[kwargs.get('smoking_status')].value



    def predict(self):
        print(self)
        x=np.array([self.gender, self.age, self.hypertension, self.heart_disease, self.ever_married, self.work_type, self.residence_type,
                      self.avg_glucose_level, self.bmi, self.smoking_status]).reshape(1, -1)
        scaler_path=os.path.join(PROJECT_DIR, "models/scalar1.pkl")
        scaler=None
        with open(scaler_path, 'rb') as scaler_file:
            scaler=pickle.load(scaler_file)

        x=scaler.transform(x)

        model_path=os.path.join(PROJECT_DIR, "models/svm.sav")
        dt=joblib.load(model_path)

        Y_pred=dt.predict(x)
        return Y_pred[0]
