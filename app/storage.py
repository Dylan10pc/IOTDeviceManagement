"""Storage module, Persists local state to disk.

This module manages a JSON file that tracks which content items
have been downloaded to the device. This state persists across restarts,
allowing the service to resume where it left off.
"""

import json
import os

#this file tracks which items the device has already downloaded
STATE_FILE = "/tmp/winnow/state.json"


def load_local_state():

    #if this is the first run, no state file exists yet
    if not os.path.exists(STATE_FILE):
        return {}

    #read and parse the JSON state file
    with open(STATE_FILE) as f:
        return json.load(f)


def save_local_state(state):
    #write the state to disk in JSON format for easy inspection and debugging
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)
