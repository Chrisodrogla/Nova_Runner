import requests
import json


class HTTP:

    def __init__(self):
        self.api_key = 'hhkX1YYg8gECcptPpk8d3OKalNaRlQQoj9zU9Ahs4xhaLE4eF5XYfmze0LN8hpoffYevtG16SuEXFXonbg'
        self.api_url = 'https://scraping.narf.ai/api/v1/'

    

    def get(self, url, headers=None, render=False):
        try:
            payload = {
                "api_key": self.api_key,
                "url": url
            }

            if headers:
                payload.update({"headers": json.dumps(headers)})

            response = requests.get(self.api_url, timeout=300, params=payload)
            if response.status_code in [200, 201]:
                return response
        except:
            pass
        return None
    

    def post(self, url, headers=None, render=False, data=None):
        try:
            payload = {
                "api_key": self.api_key,
                "url": url,
                "render_js": render
            }

            if headers:
                payload.update({"headers": json.dumps(headers)})

            response = requests.post(self.api_url, timeout=300, params=payload, json=data)
            if response.status_code in [200, 201]:
                return response
        except:
            pass
        return None