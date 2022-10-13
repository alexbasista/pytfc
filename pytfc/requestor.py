"""
Module for HTTP verb functions against TFC/E API.
"""
import requests
import json


class Requestor(object):
    """
    Constructs HTTP verb methods to call TFC/E API. 
    This class is initialized via the client.py module,
    and the header is received from the Client class within.
    """
    def __init__(self, client, headers):
        self._logger = client._logger
        self.headers = headers

    def post(self, url, payload):
        r = None
        self._logger.debug(f"Sending HTTP POST to {url}.")
        r = requests.post(url=url, headers=self.headers, data=json.dumps(payload))
        r.raise_for_status()
        return r

    def get(self, url, filters=None, page_number=None, page_size=None, include=None):
        r = None
        
        query_params = []

        if filters is not None:
            if isinstance(filters, list):
                for i in filters:
                    filter_str = 'filter' + i
                    query_params.append(filter_str)
            else:
                raise TypeError("The `filters` query parameter must be of the type `list`.")
        
        if page_number is not None:
            query_params.append(f'page[number]={page_number}')

        if page_size is not None:
            query_params.append(f'page[size]={page_size}')
        
        if include is not None:
            include_str = f'include={include}'
            query_params.append(include_str)
        
        if query_params:
            url += '?' + '&'.join(query_params)
        
        self._logger.debug(f"Sending HTTP GET to {url}")
        r = requests.get(url=url, headers=self.headers)
        r.raise_for_status()
        return r

    def patch(self, url, payload):
        r = None
        self._logger.debug(f"Sending HTTP PATCH to {url}")
        r = requests.patch(url=url, headers=self.headers, data=json.dumps(payload))
        r.raise_for_status()
        return r

    def delete(self, url):
        r = None
        self._logger.debug(f"Sending HTTP DELETE to {url}")
        r = requests.delete(url=url, headers=self.headers)
        r.raise_for_status()
        return r

    # --- experimenting --- #
    def post_data(self, url, payload):
        r = None
        r = requests.post(url=url, headers=self.headers, data=payload)
        r.raise_for_status()
        return r
    
    # --- experimenting --- #
    def post_json(self, url, payload):
        r = None
        r = requests.post(url=url, headers=self.headers, json=payload)
        r.raise_for_status()
        return r