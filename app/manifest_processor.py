"""ManifestProcessor module, Processes manifest updates and detects new content.

This module:
- Compares incoming manifests against local state to detect new items
- Manages downloads of new content
- Persists state locally for durability across device restarts
- Handles extensible content types (icons, menus, etc.) without code changes
"""

import logging
from app.content_downloader import download_content
from app.storage import load_local_state, save_local_state

logger = logging.getLogger(__name__)

class ManifestProcessor:

    
    def __init__(self):

        self.local_state = load_local_state()
        logger.info(f"Loaded local state with {len(self.local_state)} items")
        
    def process(self, manifest):

        events = []
        #iterate through all content types in the manifest dynamically
        content_types = manifest.keys()
        
        for content_type in content_types:
            #get the items section for this content type (e.g., "icons" or "menus")
            section = manifest[content_type]
            
            #skip sections marked as unavailable
            #keep previously downloaded content available even if the source is down
            if section.get("unavailable", False):
                continue
            
            #extract list of items for this content type 
            items = section.get("items", [])

            #process each item to check if we need to download it
            for item in items:
                #extract item metadata
                name = item.get("name")
                uri = item.get("uri")

                #skip items with incomplete data
                if not name or not uri:
                    continue

                #check if this item is new and not in our local state
                if name not in self.local_state:
                    #download the new content to the device
                    download_content(uri, name)

                    #remember that we have this item so we don't re-download it
                    self.local_state[name] = uri

                    #create an event to notify other services of the new content
                    events.append({
                        "action": "ADDED",
                        "key": name
                    })

        #persist the updated state to disk so it survives device restarts
        save_local_state(self.local_state)

        return events
        