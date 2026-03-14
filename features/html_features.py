from bs4 import BeautifulSoup
from urllib.parse import urlparse


def get_base_domain(domain):
    parts = domain.split(".")
    if len(parts) >= 2:
        return parts[-2] + "." + parts[-1]
    return domain


def extract_html_features(html, base_url):

    features = {}

    if html is None:
        features["login_form"] = 0
        features["iframe_count"] = 0
        features["external_link_ratio"] = 0
        features["form_action_external"] = 0
        return features

    soup = BeautifulSoup(html, "html.parser")

    # login form detection
    password_inputs = soup.find_all("input", {"type": "password"})
    features["login_form"] = 1 if len(password_inputs) > 0 else 0

    # iframe detection
    features["iframe_count"] = len(soup.find_all("iframe"))

    # external link ratio
    links = soup.find_all("a", href=True)
    total_links = len(links)

    external_links = 0

    base_domain = urlparse(base_url).netloc
    base_root = get_base_domain(base_domain)

    for link in links:

        link_domain = urlparse(link["href"]).netloc

        if link_domain:

            link_root = get_base_domain(link_domain)

            if link_root != base_root:
                external_links += 1

    if total_links > 0:
        ratio = external_links / total_links

        # cap extreme values to reduce bias
        features["external_link_ratio"] = min(ratio, 0.9)

    else:
        features["external_link_ratio"] = 0

    # form action mismatch
    forms = soup.find_all("form", action=True)

    mismatch = 0

    for form in forms:

        action_domain = urlparse(form["action"]).netloc

        if action_domain:

            action_root = get_base_domain(action_domain)

            if action_root != base_root:
                mismatch = 1

    features["form_action_external"] = mismatch

    return features