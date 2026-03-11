import json


class DummyPublisher:

    def publish(self, event):

        payload = json.dumps(event)

        print(f"Publishing {payload}")