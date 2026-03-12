"""Stub server module - Mock manifest endpoint for local testing.

This Flask server simulates the cloud manifest service, providing
a local endpoint for the device service to poll during development
and testing. It returns a simple manifest with one placeholder icon.
"""

from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/v2/manifest")
def manifest():
    """Return a mock manifest with test content.
    
    In a real deployment, this endpoint would:
    - Check device authentication from X-Authorization-Device header
    - Return a 304 Not Modified if the ETag matches
    - Return new manifest content if changes are detected
    
    For testing, this just returns a static manifest with one icon.
    """
    return jsonify({
        "icons": {
            "items": [
                {
                    "name": "icon-1.png",
                    "uri": "https://via.placeholder.com/150"
                }
            ]
        }
    })

if __name__ == "__main__":
    # Start the Flask development server on port 8080
    # In local development, the device service connects to http://localhost:8080
    app.run(port=8080)