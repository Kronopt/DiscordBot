#!python3
# coding: utf-8


"""
Pyppeteer fixes
"""


import http
import json
import time
import urllib
import pyppeteer


def get_ws_endpoint(url):
    url = url + '/json/version'
    timeout = time.time() + 30
    while True:
        if time.time() > timeout:
            raise pyppeteer.errors.BrowserError('Browser closed unexpectedly:\n')
        try:
            with urllib.request.urlopen(url) as f:
                data = json.loads(f.read().decode())
            break
        except (urllib.error.URLError, http.client.HTTPException):
            pass
        time.sleep(0.1)

    return data['webSocketDebuggerUrl']
