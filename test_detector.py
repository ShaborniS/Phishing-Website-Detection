from detection.detector_services import analyze_url


if __name__ == "__main__":

    url = input("Enter URL: ")

    result = analyze_url(url)

    print("\n---- Website Analysis ----\n")
    print(result)