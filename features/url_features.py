import re
from urllib.parse import urlparse


def extract_url_features(url: str) -> dict:

    parsed = urlparse(url)

    domain = parsed.netloc.lower()

    # normalize domain (remove www)
    if domain.startswith("www."):
        domain = domain[4:]

    path = parsed.path

    # normalize root path
    if path == "/":
        path = ""

    features = {}

    features["url_length"] = len(url)

    # check IP address
    features["has_ip"] = 1 if re.search(r"\d+\.\d+\.\d+\.\d+", domain) else 0

    # @ symbol
    features["has_at_symbol"] = 1 if "@" in url else 0

    # hyphen in domain
    features["hyphen_in_domain"] = 1 if "-" in domain else 0

    # subdomain count
    parts = domain.split(".")
    features["subdomain_count"] = max(len(parts) - 2, 0)

    # https
    features["https"] = 1 if parsed.scheme == "https" else 0

    # path length
    features["path_length"] = len(path)

    # digit ratio
    digit_count = sum(c.isdigit() for c in url)
    features["digit_ratio"] = digit_count / len(url)

    # special character ratio
    special_chars = re.findall(r"[^\w./]", url)
    features["special_char_ratio"] = len(special_chars) / len(url)

    # high digit ratio
    features["high_digit_ratio"] = 1 if features["digit_ratio"] > 0.15 else 0

    # long url
    features["long_url"] = 1 if len(url) > 75 else 0

    # hostname length
    features["hostname_length"] = len(domain)

    # domain token count
    tokens = re.split(r"[.-]", domain)
    features["domain_token_count"] = len(tokens)

    return features