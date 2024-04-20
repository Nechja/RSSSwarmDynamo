import requests
from requests.exceptions import RequestException

class HttpClient:
    def __init__(self, config):
        self.client = requests.Session()
        self.config = config

    def get(self, url):
        return self.client.get(url)
    
    def post(self, url, endpoint, data):
        try:
            return self.client.post(f"http://{url}:{self.config.FLASK_PORT}{endpoint}", json=data)
        except RequestException as e:
            print(f"Error sending POST request to {url}: {e}")
            return None