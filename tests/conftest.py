import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import MagicMock
import pytest

from src.main import api
from src.database import get_db


mock_session = MagicMock()


def override_get_db():
    try:
        yield mock_session
    finally:
        pass


api.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def mock_db_session():
    return mock_session