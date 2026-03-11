import time

from manifest_client import ManifestClient
from manifest_processor import ManifestProcessor
from publisher import DummyPublisher

POLLING_INTERVAL_SECONDS = 10
DEVICE_TOKEN = "device_1234"
MANIFEST_URL = "http://localhost:8080/v2/manifest"

def main():
    client = ManifestClient(MANIFEST_URL, DEVICE_TOKEN)
    processor = ManifestProcessor()
    publisher = DummyPublisher()
    while True:
        manifest = client.fetch_manifest()
        if manifest:
            events = processor.process(manifest)
            
            for event in events:
                publisher.publish(event)
        time.sleep(POLLING_INTERVAL_SECONDS)
if __name__ == "__main__":    
    main()