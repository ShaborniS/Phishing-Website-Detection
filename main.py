from core.input_validator import normalize_url
from core.html_fetcher import fetch_html

from features.url_features import extract_url_features
from features.html_features import extract_html_features
from features.feature_vector import build_feature_vector

from detection.ml_model import MLPhishingDetector
from detection.rule_engine import rule_based_detection

from response.risk_scorer import compute_risk
from response.formatter import format_response


detector = MLPhishingDetector()


def analyze_url(url):

    url = normalize_url(url)

    html = fetch_html(url)

    url_features = extract_url_features(url)

    html_features = extract_html_features(html, url)

    feature_vector = build_feature_vector(url_features, html_features)

    try:

        prediction, probability = detector.predict(feature_vector)

    except Exception:

        prediction, score = rule_based_detection(feature_vector, url)

        probability = score / 10

    score, level = compute_risk(probability)

    result = format_response(
        url,
        prediction,
        probability,
        score,
        level,
        feature_vector
    )

    return result


if __name__ == "__main__":

    url = input("Enter URL: ")

    result = analyze_url(url)

    print("\nWebsite Analysis Result\n")

    for key, value in result.items():
        print(f"{key}: {value}")