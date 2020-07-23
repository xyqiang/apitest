import pytest
import requests

@pytest.fixture
def init_session():
    return requests.sessions.Session()