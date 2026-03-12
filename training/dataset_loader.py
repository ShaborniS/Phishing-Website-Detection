import pandas as pd


def load_phishtank_dataset():
    """
    Loads real phishing URLs from verified_online.csv
    """
    path = "data/raw/verified_online.csv"

    df = pd.read_csv(path)

    # dataset contains many columns, we only need the URL
    urls = df["url"].dropna().tolist()

    return urls


def load_legitimate_dataset():

    path = "data/processed/legit_urls_expanded.csv"

    df = pd.read_csv(path)

    urls = df["url"].dropna().tolist()

    return urls


def load_uci_dataset():
    """
    Optional dataset (feature-based dataset already engineered).
    We will not use it in training because it already contains
    different features.
    """
    path = "data/raw/uci-ml-phishing-dataset.csv"

    df = pd.read_csv(path)

    return df