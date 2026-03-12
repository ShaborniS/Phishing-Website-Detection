def compute_risk(probability: float, prediction: str):

    risk_score = int(probability * 100)

    if prediction == "phishing":
        risk_level = "HIGH"

    elif risk_score >= 40:
        risk_level = "MEDIUM"

    else:
        risk_level = "LOW"

    return risk_score, risk_level