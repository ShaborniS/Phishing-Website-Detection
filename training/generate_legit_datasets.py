import pandas as pd

INPUT = "data/raw/majestic_million.csv"
OUTPUT = "data/processed/legit_urls_expanded.csv"

SUBDOMAINS = [
    "www",
    "mail",
    "web",
    "docs",
    "drive",
    "support",
    "account"
]

df = pd.read_csv(INPUT)

domains = df["Domain"].head(5000)

urls = []

for d in domains:

    urls.append(f"https://{d}")

    for sub in SUBDOMAINS:
        urls.append(f"https://{sub}.{d}")

dataset = pd.DataFrame({"url": urls})

dataset.to_csv(OUTPUT, index=False)

print("Generated", len(dataset), "legitimate URLs")