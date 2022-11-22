import functools
from pytfc import exceptions

# Constants
DEFAULT_LOG_LEVEL = 'WARNING'

def validate_ws_is_set(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # before function call
        if not kwargs.get('name') and not args[0].ws:
            raise exceptions.MissingWorkspace
        return func(*args, **kwargs)
        # after function call
    return wrapper

def validate_ws_id_is_set(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # before function call
        if not kwargs.get('ws_id') and not args[0].ws_id:
            raise exceptions.MissingWorkspace
        return func(*args, **kwargs)
        # after function call
    return wrapper