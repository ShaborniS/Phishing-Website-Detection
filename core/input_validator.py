from urllib.parse import urlparse


def normalize_url(url: str) -> str:
    """
    Ensures URL contains scheme.
    """
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    return url


def extract_domain(url: str) -> str:
    """
    Extract domain from URL.
    """
    parsed = urlparse(url)
    return parsed.netloc


def validate_url(url: str) -> bool:
    """
    Basic URL validation.
    """
    parsed = urlparse(url)
    return all([parsed.scheme, parsed.netloc])