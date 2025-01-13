import requests

class llm:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def call(self, question: str) -> dict:
        """Send a question to the LLM API and return the response."""
        url = f"{self.base_url}/api/v1/prediction/983cd7ad-badd-49c1-9e8e-2b9108ba5b39"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        payload = {"question": question}

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()  # Raise an error for bad status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}