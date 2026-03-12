"""Publisher module, Publishes events when content is downloaded.

In production, this would publish to MQTT or another message broker.
For testing and development, it logs to stdout.
"""
import json


class DummyPublisher:

    def publish(self, event):

        #convert the event to JSON and output to stdout
        #example output: Publishing {"action": "ADDED", "key": "icon-1.png"}
        payload = json.dumps(event)
        print(f"Publishing {payload}")