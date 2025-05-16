import os
import requests
from dotenv import load_dotenv

load_dotenv()

def analyze_text_with_nlu(text: str = "Digitalscorpyun speaks in sacred code."):
    api_key = os.getenv("IBM_NLU_APIKEY")
    url = os.getenv("IBM_NLU_URL")

    if not api_key or not url:
        return "❌ IBM NLU credentials missing in .env"

    try:
        response = requests.post(
            f"{url}/v1/analyze",
            headers={"Content-Type": "application/json"},
            params={"version": "2021-08-01"},
            json={
                "text": text,
                "features": {
                    "sentiment": {},
                    "keywords": {"limit": 5}
                }
            },
            auth=("apikey", api_key)
        )

        if response.status_code == 200:
            result = response.json()
            return {
                "sentiment": result.get("sentiment", {}),
                "keywords": [kw["text"] for kw in result.get("keywords", [])]
            }
        else:
            return f"❌ Error {response.status_code}: {response.text}"

    except Exception as e:
        return f"⚠️ Exception: {str(e)}"
