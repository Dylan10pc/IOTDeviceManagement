"""Test for manifest structure, verifies the stub server response format.

This test ensures that the stub server returns a properly structured
manifest with the expected 'icons' section and items list.
"""

from stub_server import app

def test_manifest_contains_icons():

    #create a test client to call the stub server without actually running it as a server
    client = app.test_client()

    #make a GET request to the manifest endpoint
    response = client.get("/v2/manifest")
    #parse the JSON response
    data = response.get_json()

    #verify that the required top level "icons" key exists
    assert "icons" in data
    #verify that the icons section contains an "items" list
    assert "items" in data["icons"]
