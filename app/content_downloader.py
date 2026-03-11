import os
import requests

DOWNLOAD_PATH = "/tmp/winnow"

os.makedirs(DOWNLOAD_PATH, exist_ok=True)


def download_content(uri, name):
    response = requests.get(uri)