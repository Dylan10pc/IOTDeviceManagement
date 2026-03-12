
from stub_server import app

def test_manifest_item_structure():
    #create a test client to call the stub server
    client = app.test_client()

    #make a GET request to the manifest endpoint
    response = client.get("/v2/manifest")
    #parse the JSON response
    data = response.get_json()

    #get the first icon item to verify its structure
    item = data["icons"]["items"][0]

    #verify that the item has a unique name to identify it locally
    assert "name" in item
    #verify that the item has a uri to download from
    assert "uri" in item
