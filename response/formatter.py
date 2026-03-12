def format_response(url, prediction, probability, score, level, features):

    return {
        "url": url,
        "prediction": prediction,
        "probability": round(probability, 3),
        "risk_score": score,
        "risk_level": level,
        "features": features
    }