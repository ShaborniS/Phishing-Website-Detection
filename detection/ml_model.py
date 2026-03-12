import joblib
import pandas as pd


MODEL_PATH = "models/phishing_model.pkl"


class MLPhishingDetector:

    def __init__(self):

        self.model = joblib.load(MODEL_PATH)

        # get feature names used during training
        self.feature_names = list(self.model.feature_names_in_)

    def predict(self, features: dict):

        # keep only the features that the model expects
        filtered = {k: features[k] for k in self.feature_names if k in features}

        df = pd.DataFrame([filtered])

        prediction = self.model.predict(df)[0]

        probability = self.model.predict_proba(df)[0][1]

        label = "phishing" if prediction == 1 else "legitimate"

        return label, probability