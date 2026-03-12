"""ContentDownloader module, downloads content from URIs to the device.

This module handles:
- Fetching content files from remote URIs
- Storing files locally on the device
- Error handling and logging of download failures

"""

import os
import requests
import logging

logger = logging.getLogger(__name__)

#directory where all downloaded content is stored
DOWNLOAD_PATH = "/tmp/winnow"

#ensure the download directory exists 
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

def download_content(uri, name):
    
    try:
        #fetch the content from the remote URI with a 30-second timeout
        #larger timeout allows for slow network conditions on IoT devices
        response = requests.get(uri, timeout=30)
        response.raise_for_status()
        
        #construct the local file path
        path = os.path.join(DOWNLOAD_PATH, name)
        
        #write the downloaded content to disk in binary mode
        with open(path, "wb") as f:
            f.write(response.content)
        
        #log successful download for monitoring and troubleshooting
        logger.info(f"Downloaded {name} from {uri} to {path}")
    except requests.RequestException as e:
        #log the error with context for debugging
        logger.error(f"Failed to download {name} from {uri}: {e}")
        raise