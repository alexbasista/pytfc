import pytest
import pytfc
from os import getenv


@pytest.fixture
def client():
    client = pytfc.Client()
    return client

@pytest.fixture
def tfe_ghain():
    return getenv('TFE_GHAIN')
