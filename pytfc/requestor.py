"""
Module for HTTP verb functions against TFC/E API.
"""
import requests
import json
import logging
import sys
from abc import ABCMeta, abstractmethod

# Constants
MAX_PAGE_SIZE = 100


class Requestor:
    """
    Constructs HTTP verb methods to call TFC/E API. 
    This class is initialized via the client.py module,
    and the header is received from the Client class within.
    """
    
    __metaclass__ = ABCMeta
    
    def __init__(self, headers, base_uri, verify, log_level):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(log_level)
        self._logger.addHandler(logging.StreamHandler(sys.stdout))
        
        self._headers = headers
        self._base_uri = base_uri
        self._verify = verify
        

    def post(self, path, payload):
        r = None
        url = self._base_uri + path
        self._logger.debug(f"Sending HTTP POST to {url}")
        self._logger.debug(json.dumps(payload, indent=2))
        r = requests.post(url=url, headers=self._headers, data=json.dumps(payload))
        r.raise_for_status()
        return r

    def get(self, path, filters=None, page_number=None, page_size=None,
            include=None, search=None, query=None, since=None):
        r = None
        url = self._base_uri + path
        
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
            
            if 'user' in search:
                query_params.append(f"search[user]={search['user']}")

            if 'commit' in search:
                query_params.append(f"search[commit]={search['commit']}")
        
        if query is not None:
            query_params.append(f'q={query}')

        if since is not None:
            query_params.append(f'since={since}')

        if query_params:
            url += '?' + '&'.join(query_params)
        
        self._logger.debug(f"Sending HTTP GET to {url}")
        r = requests.get(url=url, headers=self._headers)
        r.raise_for_status()
        return r

    def patch(self, path, payload):
        r = None
        url = self._base_uri + path
        self._logger.debug(f"Sending HTTP PATCH to {url}")
        self._logger.debug(json.dumps(payload, indent=2))
        r = requests.patch(url=url, headers=self._headers, data=json.dumps(payload))
        r.raise_for_status()
        return r

    def delete(self, path, payload=None):
        r = None
        url = self._base_uri + path
        self._logger.debug(f"Sending HTTP DELETE to {url}")
        r = requests.delete(url=url, headers=self._headers, data=json.dumps(payload))
        r.raise_for_status()
        return r

    def list_all(self, path, filters=None, include=None, search=None,
                 query=None, since=None):
        """
        Utility method to enumerage pages in a response from a `get`
        request to a list API endpoint and returns all of the results.
        """
        current_page_number = 1
        list_resp = self.get(path=path, page_number=current_page_number,
            page_size=MAX_PAGE_SIZE, filters=filters, include=include,
            search=search, query=query, since=since).json()

        if 'meta' in list_resp:
            self._logger.debug("Found `meta` block in list response.")
            total_pages = list_resp['meta']['pagination']['total-pages']
        elif 'pagination' in list_resp:
            self._logger.debug("Found `pagination` block in list response.")
            total_pages = list_resp['pagination']['total_pages']

        data = []
        included = []
        while current_page_number <= total_pages:
            list_resp = self.get(path=path, page_number=current_page_number,
                page_size=MAX_PAGE_SIZE, filters=filters, include=include,
                search=search, query=query, since=since).json()
            data += list_resp['data']

            if 'included' in list_resp:
                included += list_resp['included']
                self._logger.debug("Found `included` block in list response.")

            current_page_number += 1

        return {
            'data': data,
            'included': included
        }