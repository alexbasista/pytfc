"""
Module for HTTP verb functions against TFC/E API with enhanced response handling.
"""
import requests
import json
import logging
import sys

# Constants
MAX_PAGE_SIZE = 100


class TFCResponse:
    """
    Response wrapper that provides both parsed data and access to response metadata.
    
    This wrapper maintains backward compatibility with requests.Response while 
    offering a more Pythonic interface for accessing response data and metadata.
    
    Args:
        response: The original requests.Response object
        
    Attributes:
        status_code: HTTP status code (e.g., 200, 404, 500)
        headers: Response headers as a dictionary
        url: The URL that was requested
        data: Parsed JSON response data (None if not JSON)
        
    Examples:
        >>> response = TFCResponse(requests_response)
        >>> response.status_code
        200
        >>> response.data
        {'data': [{'id': 'ws-123', 'type': 'workspaces', ...}]}
        >>> if response.exception:
        ...     print(f"Error: {response.exception}")
    """
    
    def __init__(self, response):
        self._response = response
        self.status_code = response.status_code
        self.headers = response.headers
        self.url = response.url
        
        # Parse JSON data if available
        try:
            self._data = response.json() if response.content else None
        except (ValueError, requests.exceptions.JSONDecodeError):
            self._data = None
    
    @property
    def data(self):
        """Get the parsed JSON data"""
        return self._data
    
    def json(self):
        """Get the parsed JSON data - backward compatible with requests.Response"""
        return self._data
    
    @property
    def text(self):
        """Get the response text"""
        return self._response.text
    
    @property
    def content(self):
        """Get the raw response content"""
        return self._response.content
    
    @property
    def exception(self):
        """Get the HTTPError exception that would be raised, or None if successful"""
        if self.status_code >= 400:
            return requests.exceptions.HTTPError(
                f"{self.status_code} Client Error: {self._response.reason} for url: {self.url}",
                response=self._response
            )
        return None

    def raise_for_status(self):
        """Raise an exception for HTTP error status codes"""
        return self._response.raise_for_status()
    
    @property
    def raw_response(self):
        """Access to the original requests.Response object if needed"""
        return self._response
    
    def __repr__(self):
        return f"<TFCResponse [{self.status_code}]>"


class Requestor:
    """
    HTTP client for TFC/E API with enhanced response handling and pagination.
    
    This class handles all HTTP communication with Terraform Cloud/Enterprise APIs,
    providing consistent response wrapping, error handling, and automatic pagination
    for list endpoints.
    
    Args:
        headers: Default headers for all requests (authentication, content-type)
        base_uri: Base URI for API endpoints (e.g., 'https://app.terraform.io/api/v2')
        verify: SSL certificate verification (True/False or path to CA bundle)
        log_level: Logging level for request debugging
        
    Examples:
        >>> requestor = Requestor(
        ...     headers={'Authorization': 'Bearer token'},
        ...     base_uri='https://app.terraform.io/api/v2',
        ...     verify=True,
        ...     log_level=logging.INFO
        ... )
        >>> response = requestor.get('/organizations/my-org/workspaces')
    """
    
    def __init__(self, headers, base_uri, verify, log_level):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(log_level)
        self._logger.addHandler(logging.StreamHandler(sys.stdout))
        
        self._headers = headers
        self._base_uri = base_uri
        self._verify = verify

    def post(self, path, payload):
        """
        Perform HTTP POST request to TFC/E API.
        
        Args:
            path: API endpoint path (e.g., '/organizations/my-org/workspaces')
            payload: Dictionary to be sent as JSON in request body
            
        Returns:
            TFCResponse: Wrapped response with data, status_code, and metadata
            
        Raises:
            HTTPError: If the request returns a 4xx or 5xx status code
        """
        
        url = self._base_uri + path
        self._logger.debug(f"Sending HTTP POST to {url}")
        self._logger.debug(json.dumps(payload, indent=2))
        
        r = requests.post(url=url, headers=self._headers, data=json.dumps(payload), verify=self._verify)
        r.raise_for_status()
        return TFCResponse(r)

    def get(
        self,
        path,
        filters=None,
        page_number=None,
        page_size=None,
        include=None,
        search=None,
        query=None,
        since=None,
    ):
        """
        Perform HTTP GET request to TFC/E API.
        
        Args:
            path: API endpoint path (e.g., '/organizations/my-org/workspaces')
            filters: List of filter strings in format ['[field]=value']
            page_number: Page number for pagination (1-based)
            page_size: Number of items per page (max 100)
            include: Comma-separated list of related resources to include
            search: Dict of search parameters (name, tags, version, user, commit)
            query: General query string parameter
            since: Timestamp for filtering results
            
        Returns:
            TFCResponse: Wrapped response with data, status_code, and metadata
            
        Raises:
            TypeError: If filters is not a list
            
        Examples:
            >>> response = requestor.get('/organizations/my-org/workspaces')
            >>> response = requestor.get('/workspaces', 
            ...                        filters=['[name]=prod'], 
            ...                        page_size=50)
        """

        url = self._base_uri + path
        query_params = []

        if filters is not None:
            if isinstance(filters, list):
                for i in filters:
                    filter_str = 'filter' + i
                    query_params.append(filter_str)
            else:
                raise TypeError(
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
        r = requests.get(url=url, headers=self._headers, verify=self._verify)
        return TFCResponse(r)

    def patch(self, path, payload):
        """
        Perform HTTP PATCH request to TFC/E API.
        
        Args:
            path: API endpoint path (e.g., '/organizations/my-org/workspaces/ws-123')
            payload: Dictionary to be sent as JSON in request body
            
        Returns:
            TFCResponse: Wrapped response with data, status_code, and metadata
            
        Raises:
            HTTPError: If the request returns a 4xx or 5xx status code
            
        Examples:
            >>> response = requestor.patch('/workspaces/ws-123', {
            ...     'data': {
            ...         'type': 'workspaces',
            ...         'attributes': {'terraform-version': '1.6.0'}
            ...     }
            ... })
        """
        
        url = self._base_uri + path
        self._logger.debug(f"Sending HTTP PATCH to {url}")
        self._logger.debug(json.dumps(payload, indent=2))
        
        r = requests.patch(url=url, headers=self._headers, data=json.dumps(payload), verify=self._verify)
        r.raise_for_status()
        return TFCResponse(r)

    def delete(self, path, payload=None):
        """
        Perform HTTP DELETE request to TFC/E API.
        
        Args:
            path: API endpoint path (e.g., '/organizations/my-org/workspaces/ws-123')
            payload: Optional dictionary to be sent as JSON in request body
            
        Returns:
            TFCResponse: Wrapped response with data, status_code, and metadata
            
        Raises:
            HTTPError: If the request returns a 4xx or 5xx status code
            
        Examples:
            >>> response = requestor.delete('/workspaces/ws-123')
            >>> response = requestor.delete('/some-endpoint', {'force': True})
        """
        
        url = self._base_uri + path
        self._logger.debug(f"Sending HTTP DELETE to {url}")
        
        data = json.dumps(payload) if payload else None
        r = requests.delete(url=url, headers=self._headers, data=data, verify=self._verify)
        r.raise_for_status()
        return TFCResponse(r)

    def list_all(
        self,
        path,
        filters=None,
        include=None,
        search=None,
        query=None,
        since=None,
    ):
        """
        Fetch all pages of results from a paginated API endpoint.
        
        Automatically handles pagination by making multiple requests to retrieve
        all available data. Returns a TFCResponse object for consistency with
        other methods.
        
        Args:
            path: API endpoint path (e.g., '/organizations/my-org/workspaces')
            filters: List of filter strings in format ['[field]=value']
            include: Comma-separated list of related resources to include
            search: Dict of search parameters (name, tags, version, user, commit)
            query: General query string parameter
            since: Timestamp for filtering results
            
        Returns:
            TFCResponse: Response object containing:
                - data: Dict with 'data' and 'included' keys containing all results
                - status_code: 200 (aggregated results are always successful)
                - Standard TFCResponse interface (headers, exception, etc.)
                
        Note:
            This method may make many HTTP requests for large datasets.
            The returned response object represents the aggregated result,
            not the final HTTP response.
            
        Examples:
            >>> response = requestor.list_all('/organizations/my-org/workspaces')
            >>> response.status_code
            200
            >>> all_workspaces = response.data
            >>> workspaces = all_workspaces['data']
            >>> len(workspaces)  # Total count across all pages
            245
        """
        current_page_number = 1
        data = []
        included = []
        final_response = None  # Keep track of the last successful response
        
        while True:
            try:
                list_resp = self.get(
                    path=path, 
                    page_number=current_page_number,
                    page_size=MAX_PAGE_SIZE, 
                    filters=filters, 
                    include=include,
                    search=search, 
                    query=query, 
                    since=since
                )
                
                # Keep track of the final response for metadata
                final_response = list_resp
                
                resp_data = list_resp.json()
                
                # Handle case where there's no data
                if 'data' not in resp_data or not resp_data['data']:
                    break
                    
                # Add data from this page
                data.extend(resp_data['data'])
                
                # Add included data if present
                if 'included' in resp_data and resp_data['included']:
                    included.extend(resp_data['included'])
                    self._logger.debug("Found `included` block in list response.")
                
                # Determine if there are more pages
                total_pages = None
                
                # Try different pagination formats
                if 'meta' in resp_data and 'pagination' in resp_data['meta']:
                    self._logger.debug("Found `meta` block in list response.")
                    pagination = resp_data['meta']['pagination']
                    total_pages = pagination.get('total-pages')
                    
                    # Alternative: check if this is the last page
                    if pagination.get('current-page') == pagination.get('total-pages'):
                        break
                        
                elif 'pagination' in resp_data:
                    self._logger.debug("Found `pagination` block in list response.")
                    pagination = resp_data['pagination']
                    total_pages = pagination.get('total_pages')
                    
                # Check if we've reached the end
                if total_pages and current_page_number >= total_pages:
                    break
                    
                # If no pagination info, assume single page
                if total_pages is None:
                    self._logger.debug("No pagination info found, assuming single page.")
                    break
                    
                current_page_number += 1
                
                # Safety valve to prevent infinite loops
                if current_page_number > 1000:  # Adjust based on your API limits
                    self._logger.warning("Reached maximum page limit (1000), stopping pagination.")
                    break
                    
            except Exception as e:
                self._logger.error(f"Error fetching page {current_page_number}: {e}")
                raise
        
        # Create aggregated result
        aggregated_data = {
            'data': data,
            'included': included
        }
        
        # Create a mock response object that mimics a real HTTP response
        class MockResponse:
            def __init__(self, data, final_resp):
                self.status_code = 200  # Aggregated results are always "successful"
                self.headers = final_resp.headers if final_resp else {}
                self.url = final_resp.url if final_resp else f"{self._base_uri}{path}"
                self._json_data = data
                self.content = str(data).encode('utf-8')  # Basic content representation
                self.text = str(data)
                self.reason = "OK"
                
            def json(self):
                return self._json_data
                
            def raise_for_status(self):
                pass  # Aggregated results don't raise (they're always 200)
        
        mock_response = MockResponse(aggregated_data, final_response)
        return TFCResponse(mock_response)