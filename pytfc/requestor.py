"""
Module for HTTP verb functions against TFC/E API.
"""
import requests
import json

class Requestor(object):
    """
    Construct HTTP verb methods to call TFC/E API. 
    This class is initialized via the parent Client class,
    and the header is inherited from the Client class.
    """
    def __init__(self, headers, **kwargs):
        self.headers = headers

    def post(self, url, payload):
        r = None
        r = requests.post(url=url, headers=self.headers, data=json.dumps(payload))
        r.raise_for_status()
        return r

    def get(self, url):
        r = None
        r = requests.get(url=url, headers=self.headers)
        r.raise_for_status()
        return r

    def patch(self, url, payload):
        r = None
        r = requests.patch(url=url, headers=self.headers, data=json.dumps(payload))
        r.raise_for_status()
        return r

    def delete(self, url):
        r = None
        r = requests.delete(url=url, headers=self.headers)
        r.raise_for_status()
        return r

    # --- temp testing --- #
    def post_data(self, url, payload):
        r = None
        r = requests.post(url=url, headers=self.headers, data=payload)
        r.raise_for_status()
        return r
    
    def post_json(self, url, payload):
        r = None
        r = requests.post(url=url, headers=self.headers, json=payload)
        r.raise_for_status()
        return r