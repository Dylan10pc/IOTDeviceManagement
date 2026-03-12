"""Test for manifest HTTP status, verifies the stub server is accessible.

This test ensures that the stub server is running and responding to requests
with a successful HTTP 200 status code.
"""

from stub_server import app

def test_manifest_returns_200():

    #create a test client to call the stub server
    client = app.test_client()

    #make a GET request to the manifest endpoint
    response = client.get("/v2/manifest")

    #verify that the response has a 200 OK status code
    assert response.status_code == 200
