from content_downloader import download_content
from storage import load_local_state, save_local_state

class ManifestProcessor:
    
    def __init__(self):
        self.local_state = load_local_state()
        
    def process(self, manifest):
        events = []
        content_types = manifest.keys()
        for content_type in content_types:
            
            section = manifest[content_type]
            
            if not section.get("enabled", False):
                continue
            
            items = section.get("items", [])

            for item in items:

                name = item.get("name")
                uri = item.get("uri")

                if not name or not uri:
                    continue

                if name not in self.local_state:

                    download_content(uri, name)

                    self.local_state[name] = uri

                    events.append({
                        "action": "ADDED",
                        "key": name
                    })

        save_local_state(self.local_state)

        return events
        