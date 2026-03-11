import requests

class ManifestClient:
    def __init__(self, manifest_url, device_token):
        self.manifest_url = manifest_url
        self.device_token = device_token
        self.etag = None
        
    def fetch_manifest(self):
        headers = {"X-Authorization-Device": self.device_token}
        
        if self.etag:
            headers["If-None-Match"] = self.etag
        
        response = requests.get(self.manifest_url, headers=headers)
        
        if response.status_code == 304:
            return None

        if response.status_code == 200:
            self.etag = response.headers.get("ETag")
            return response.json()

        if response.status_code == 401:
            raise Exception("Device authentication failed")
        
        if response.status_code == 500:
            raise Exception("Server error while fetching manifest")

        return None