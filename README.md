# IoT device manifest service

A containerized service that runs on IoT waste tracking devices to automatically download and manage device-specific content from a cloud manifest service. 

This service:
- Polls a cloud manifest endpoint for changes (with ETag caching)
- Processes manifest updates to detect new or changed content
- Automatically downloads new content to the device
- Publishes events for content updates via a dummy MQTT publisher
- Handles graceful shutdown for device restarts
- Supports extensible content types (menus, icons, etc.)

## Building and running locally

### Prerequisites

- Python 3.11+
- Docker (optional, for containerized deployment)

### Setup

1. **Create virtual environment:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the tests

```bash
pytest tests/
```

All tests should pass.

### Running the service locally

1. **Start the stub manifest server** (in a separate terminal):
   ```bash
   python stub_server.py
   ```
   This runs on `http://localhost:8080` and simulates the cloud manifest API.

2. **Run the device service:**
   ```bash
   python app/main.py
   ```

The service will:
- Poll the manifest every 10 seconds
- Download new content to `/tmp/winnow/`
- Log all activity to stdout
- Gracefully shutdown on SIGINT/SIGTERM signals

### Docker deployment

1. **Build the image:**
   ```bash
   docker build -t iot-manifest-service .
   ```

2. **Run the container:**
   ```bash
   docker run -v /tmp/winnow:/tmp/winnow \
     --network host \
     iot-manifest-service
   ```

The container expects:
- Manifest server at `http://localhost:8080`
- Downloaded files stored at `/tmp/winnow`
- Network access to both the manifest service and content URIs

## Configuration

Edit these values in `app/main.py`:

- `POLLING_INTERVAL_SECONDS`: Polling frequency (default: 10s)
- `DEVICE_TOKEN`: Device authentication token
- `MANIFEST_URL`: Manifest endpoint URL

## Testing

The test suite includes:

- `test_manifest_returns_200()` - Verifies stub server responds correctly
- `test_manifest_contains_icons()` - Verifies manifest structure
- `test_manifest_item_structure()` - Verifies item fields
- `test_processor_detects_new_item()` - Verifies change detection logic

Run with: `pytest tests/ -v`
