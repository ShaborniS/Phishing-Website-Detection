import joblib
import pandas as pd


MODEL_PATH = "models/phishing_model.pkl"


class MLPhishingDetector:

    def __init__(self):

        self.model = joblib.load(MODEL_PATH)

        # get feature names used during training
        self.feature_names = list(self.model.feature_names_in_)

    def predict(self, features: dict):

        # build feature vector in exact training order
        row = {}

        for name in self.feature_names:
            row[name] = features.get(name, 0)

        df = pd.DataFrame([row])

        prediction = self.model.predict(df)[0]

        probability = self.model.predict_proba(df)[0][1]

        label = "phishing" if prediction == 1 else "legitimate"

        return label, probability