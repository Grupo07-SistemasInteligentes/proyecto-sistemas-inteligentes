import requests
import sys

try:
    response = requests.get("http://localhost:5000/health", timeout=5)
    if response.status_code == 200:
        sys.exit(0)
    else:
        sys.exit(1)
except:
    sys.exit(1)