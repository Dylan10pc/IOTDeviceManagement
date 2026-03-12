"""Main service module 

This is the entrypoint for the IoT device manifest service. This service is responsible for:
- Polls the cloud manifest endpoint at regular intervals
- Processes manifest updates to detect new content
- Handles graceful shutdown when the device is powered off
- Manages error handling and retries across service disruptions
"""

import time
import logging
import signal
import sys
from app.manifest_client import ManifestClient
from app.manifest_processor import ManifestProcessor
from app.publisher import DummyPublisher

#how often to poll the manifest endpoint for changes (in seconds)
#lower values detect changes faster but consume more bandwidth and CPU
POLLING_INTERVAL_SECONDS = 10

#authentication token that identifies this specific device to the cloud service
DEVICE_TOKEN = "device_1234"

#URL of the cloud manifest endpoint
MANIFEST_URL = "http://localhost:8080/v2/manifest"

#configure logging to show timestamps and log level
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#global flag to signal the polling loop to shut down gracefully
shutdown_event = False

def handle_shutdown(signum, frame):
    
    #This handler allow the main loop to finish processing the current manifest and exit cleanly without a forceful kill
    global shutdown_event
    logger.info("Shutdown signal received, gracefully stopping...")
    shutdown_event = True

def main():
    """Main service loop
    
    The service:
    1. Registers signal handlers for graceful shutdown
    2. Initializes components (client, processor, publisher)
    3. Enters a polling loop that:
       - Fetches the manifest from the cloud
       - Detects and downloads new content
       - Publishes events for newly added items
       - Sleeps before the next poll
    4. Exits gracefully when a shutdown signal is received
    """
    global shutdown_event
    
    #register signal handlers to catch shutdown requests from the OS
    #SIGTERM: Normal termination signal
    #SIGINT: Keyboard interrupt (Ctrl+C)
    #This allows the service to exit cleanly instead of being killed abruptly
    signal.signal(signal.SIGTERM, handle_shutdown)
    signal.signal(signal.SIGINT, handle_shutdown)
    
    #initialize the key components
    #fetches manifests
    client = ManifestClient(MANIFEST_URL, DEVICE_TOKEN)  
    #detects new items
    processor = ManifestProcessor()
    #publishes events
    publisher = DummyPublisher()                               
    
    logger.info(f"Starting manifest poller. URL: {MANIFEST_URL}")
    
    #main polling loop which runs until shutdown signal is received
    while not shutdown_event:
        try:
            #step 1: Fetch the manifest from the cloud endpoint
            #returns None if unchanged (304) or dict with new content (200)
            manifest = client.fetch_manifest()
            
            #step 2: If new manifest data is available then process it
            if manifest:
                #detect new items and download them
                events = processor.process(manifest)
                
                #step 3: Publish an event for each newly downloaded item
                for event in events:
                    publisher.publish(event)
            else:
                logger.debug("No manifest update received")
        except Exception as e:
            logger.error(f"Error fetching or processing manifest: {e}")
        
        #only sleep if we haven't received a shutdown signal
        if not shutdown_event:
            time.sleep(POLLING_INTERVAL_SECONDS)
    
    logger.info("Service stopped successfully")

if __name__ == "__main__":
    main()