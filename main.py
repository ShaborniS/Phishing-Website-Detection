from core.input_validator import normalize_url
from detection.safety_block import check_safety_lists
from features.url_features import extract_url_features

from detection.ml_model import MLPhishingDetector
from detection.rule_engine import rule_based_detection

from response.risk_scorer import compute_risk
from response.formatter import format_response


detector = MLPhishingDetector()


def analyze_url(url):

    url = normalize_url(url)

    # SAFETY BLOCK
    safety_result = check_safety_lists(url)

    if safety_result:
        prediction, probability, level = safety_result

        return {
            "url": url,
            "prediction": prediction,
            "probability": probability,
            "risk_score": int(probability * 100),
            "risk_level": level
        }

    # ML detection
    url_features = extract_url_features(url)

    feature_vector = url_features

    prediction, probability = detector.predict(feature_vector)

    score, level = compute_risk(probability, prediction)

    return {
        "url": url,
        "prediction": prediction,
        "probability": round(probability, 3),
        "risk_score": score,
        "risk_level": level
    }


if __name__ == "__main__":

    url = input("Enter URL: ")

    result = analyze_url(url)

    print("\nWebsite Analysis Result\n")

    for key, value in result.items():
        print(f"{key}: {value}")