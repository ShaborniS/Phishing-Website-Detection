import re
from urllib.parse import urlparse

# phishing-abused brand words
SUSPICIOUS_BRANDS = [
    "paypal",
    "apple",
    "amazon",
    "google",
    "facebook",
    "microsoft",
    "bank",
    "secure",
    "login",
    "verify",
    "account"
]

# legitimate high-traffic brands
KNOWN_BRANDS = [
    "google","youtube","facebook","whatsapp","instagram",
    "microsoft","apple","amazon","github","linkedin",
    "twitter","wikipedia","yahoo","netflix","reddit"
]


def detect_suspicious_brand(url):

    url_lower = url.lower()

    for brand in SUSPICIOUS_BRANDS:
        if brand + "." in url_lower:
            return 1

    return 0


def detect_known_brand(url):

    url_lower = url.lower()

    for brand in KNOWN_BRANDS:
        if brand + "." in url_lower:
            return 1

    return 0


def extract_url_features(url: str) -> dict:

    parsed = urlparse(url)

    domain = parsed.netloc
    path = parsed.path

    features = {}

    # structural features
    features["url_length"] = len(url)

    features["has_ip"] = 1 if re.search(r"\d+\.\d+\.\d+\.\d+", domain) else 0

    features["has_at_symbol"] = 1 if "@" in url else 0

    features["hyphen_in_domain"] = 1 if "-" in domain else 0

    features["subdomain_count"] = max(domain.count(".") - 1, 0)

    features["https"] = 1 if parsed.scheme == "https" else 0

    features["path_length"] = len(path)

    # ratios
    digit_count = sum(c.isdigit() for c in url)

    features["digit_ratio"] = digit_count / len(url)

    special_chars = re.findall(r"[^\w]", url)

    features["special_char_ratio"] = len(special_chars) / len(url)

    # brand indicators
    features["brand_keyword"] = detect_suspicious_brand(url)

    features["known_brand"] = detect_known_brand(url)

    # derived indicators
    features["high_digit_ratio"] = 1 if features["digit_ratio"] > 0.15 else 0

    features["long_url"] = 1 if len(url) > 75 else 0

    return features