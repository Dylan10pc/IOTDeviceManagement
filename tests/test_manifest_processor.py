#test for manifest processor, verifies change detection logic.

#this test ensures that the manifest processor correctly identifies new items
#that need to be downloaded and generates appropriate events.


from unittest.mock import patch
from app.manifest_processor import ManifestProcessor

def test_processor_detects_new_item():

    
    #mock the download_content function so we don't actually download during testing
    with patch('app.manifest_processor.download_content') as mock_download:
        #create a processor instance with empty local state
        processor = ManifestProcessor()

        #create a test manifest with one icon item
        manifest = {
            "icons": {
                "items": [
                    {
                        "name": "test-icon.png",
                        "uri": "http://example/icon"
                    }
                ]
            }
        }

        #the processor should detect this as a new item
        events = processor.process(manifest)

        #verify that exactly one event was generated for the new item
        assert len(events) == 1
        #verify that the event indicates the item was added
        assert events[0]["action"] == "ADDED"
        #verify that the event contains the correct item name
        assert events[0]["key"] == "test-icon.png"
        #verify that the download was attempted with the correct URI and name
        mock_download.assert_called_once_with("http://example/icon", "test-icon.png")
