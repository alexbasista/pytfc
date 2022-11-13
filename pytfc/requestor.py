"""
Module for HTTP verb functions against TFC/E API.
"""
import requests
import json
import logging
from sys import stdout
from abc import ABC

# Constants
MAX_PAGE_SIZE = 100


class Requestor(ABC):
    """
    Constructs HTTP verb methods to call TFC/E API. 
    This class is initialized via the client.py module.
    """
    def __init__(self, headers, log_level, verify):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(log_level)
        self._logger.addHandler(logging.StreamHandler(stdout))
        self._logger.debug("Instantiating Requestor class.")
        
        self._headers = headers
        self._verify = verify

    def post(self, url, payload):
        """
        Sends HTTP POST request to URL with specified params and payload.
        """
        r = None
        self._logger.debug(f"Sending HTTP POST to {url}.")
        self._logger.debug(json.dumps(payload, indent=2))
        r = requests.post(url=url, headers=self._headers,
            data=json.dumps(payload), verify=self._verify)
        r.raise_for_status()
        return r

    def get(self, url, filters=None, page_number=None, page_size=None,
            include=None, search=None, query=None):
        """
        Sends HTTP GET request to URL with specified params.
        """
        r = None
        
        query_params = []

        if filters is not None:
            if isinstance(filters, list):
                for i in filters:
                    filter_str = 'filter' + i
                    query_params.append(filter_str)
            else:
                raise TypeError(\
                    "The `filters` query parameter must be of the type `list`.")
        
        if page_number is not None:
            query_params.append(f'page[number]={page_number}')

        if page_size is not None:
            query_params.append(f'page[size]={page_size}')
        
        if include is not None:
            include_str = f'include={include}'
            query_params.append(include_str)
        
        if search is not None:
            if 'name' in search:
                query_params.append(f"search[name]={search['name']}")
            
            if 'tags' in search:
                query_params.append(f"search[tags]={search['tags']}")

            if 'exclude-tags' in search:
                query_params.append(f"search[exclude-tags]={search['exclude-tags']}")
            
            if 'version' in search:
                query_params.append(f"search[version]={search['version']}")
        
        if query is not None:
            query_params.append(f'q{query}')

        if query_params:
            url += '?' + '&'.join(query_params)
        
        self._logger.debug(f"Sending HTTP GET to {url}")
        r = requests.get(url=url, headers=self._headers, verify=self._verify)
        r.raise_for_status()
        return r

    def patch(self, url, payload):
        """
        Sends HTTP PATCH request to URL with specified params and payload.
        """
        r = None
        self._logger.debug(f"Sending HTTP PATCH to {url}")
        self._logger.debug(json.dumps(payload, indent=2))
        r = requests.patch(url=url, headers=self._headers,
            data=json.dumps(payload), verify=self._verify)
        r.raise_for_status()
        return r

    def delete(self, url):
        """
        Sends HTTP DELETE request to URL.
        """
        r = None
        self._logger.debug(f"Sending HTTP DELETE to {url}")
        r = requests.delete(url=url, headers=self._headers,
            verify=self._verify)
        r.raise_for_status()
        return r

    def _list_all(self, url, filters=None, include=None, search=None,
        query=None):
        """
        Utility method to enumerate pages in a response from a GET
        request against a list API endpoint and returns all of the
        results in an object with two arrays: `data` and `included`.
        """
        current_page_number = 1
        list_resp = self.get(url=url, page_number=current_page_number,
            page_size=MAX_PAGE_SIZE, filters=filters, include=include,
            search=search).json()

        if 'meta' in list_resp:
            self._logger.debug("Found `meta` block in list response.")
            total_pages = list_resp['meta']['pagination']['total-pages']
        elif 'pagination' in list_resp:
            self._logger.debug("Found `pagination` block in list response.")
            total_pages = list_resp['pagination']['total-pages']

        data = []
        included = []
        while current_page_number <= total_pages:
            list_resp = self.get(url, page_number=current_page_number,
                page_size=MAX_PAGE_SIZE, filters=filters, include=include,
                search=search, query=query).json()
            data += list_resp['data']

            if 'included' in list_resp:
                included += list_resp['included']
                self._logger.debug("Found `included` block in list response.")

            current_page_number += 1

        return {
            'data': data,
            'included': included
        }