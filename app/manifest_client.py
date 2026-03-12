"""ManifestClient module

This module implements HTTP communication with the manifest endpoint including:
- ETag-based caching to minimize bandwidth and processing
- Device authentication via custom headers
- Proper error handling for various HTTP status codes
"""

import requests
import logging

logger = logging.getLogger(__name__)

class ManifestClient:
    
    def __init__(self, manifest_url, device_token):

        self.manifest_url = manifest_url
        self.device_token = device_token
        self.etag = None  # Cache the ETag from the last successful response
        
    def fetch_manifest(self):
 
        #set up HTTP headers with device authentication
        headers = {"X-Authorization-Device": self.device_token}
        
        #if we have a cached ETag, include it to request only if the manifest has changed
        #this optimizes bandwidth by avoiding downloads of unchanged data
        if self.etag:
            headers["If-None-Match"] = self.etag
        
        try:
            #perform HTTP GET request to fetch the manifest
            response = requests.get(self.manifest_url, headers=headers, timeout=10)
            
            #304 Not Modified: The manifest hasn't changed since we last fetched it
            #return None to skip processing and save bandwidth and processing time
            if response.status_code == 304:
                logger.debug("Manifest unchanged (304 Not Modified)")
                return None

            #200 OK: New manifest data is available
            #store the ETag for future requests and return the manifest content
            if response.status_code == 200:
                self.etag = response.headers.get("ETag")
                logger.info("Manifest fetched successfully")
                return response.json()

            #401 Unauthorized: Device authentication failed
            #this could indicate an invalid token or revoked device access
            if response.status_code == 401:
                raise Exception("Device authentication failed")
            
            #500 Internal Server Error: The manifest service encountered a critical error
            #the device should continue retrying on subsequent polls
            if response.status_code == 500:
                raise Exception("Server error while fetching manifest")

            #unexpected status code - log it but don't fail
            logger.warning(f"Unexpected status code: {response.status_code}")
            return None
        except requests.RequestException as e:
            #log the error and raise so the main loop can handle retries
            logger.error(f"Network error fetching manifest: {e}")
            raise