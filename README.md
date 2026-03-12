## Running the Phishing Detection System

### 1. Clone the repository

```
git clone <repository-url>
cd phishing_detector
```

### 2. Install dependencies

Make sure Python 3.9+ is installed.

Install required libraries:

```
pip install -r requirements.txt
```

### 3. Run the detector

Run the test script:

```
python test_detector.py
```

You will be prompted to enter a URL:

```
Enter URL: https://www.google.com/
```

Example output:

```
---- Website Analysis ----

{
 'url': 'https://google.com',
 'prediction': 'legitimate',
 'probability': 0.03,
 'risk_score': 3,
 'risk_level': 'LOW'
}
```

---

### Using the Detection Engine in Code

The core detection function is located in:

```
detection/detector_service.py
```

Example usage:

```python
from detection.detector_service import analyze_url

result = analyze_url("example.com")

print(result)
```

The function returns:

```
{
 "url": "...",
 "prediction": "...",
 "probability": ...,
 "risk_score": ...,
 "risk_level": ...
}
```

This function can be integrated into a backend API or web application.
