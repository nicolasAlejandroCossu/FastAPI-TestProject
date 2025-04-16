import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from fastapi.testclient import TestClient
from src.main import api
from src.models.user_model import User
from sqlalchemy.exc import IntegrityError


client = TestClient(api)

payload = {
        "id": 1,
        "username": "testuser",
        "firstname": "John",
        "lastname": "Doe",
        "age": 30,
        "gender": "M",
        "country": "USA"
    }

test_user = User(**payload)


"""
---- POST USER UNIT TEST ----
"""
    
def test_create_user(mock_db_session):
    
    mock_db_session.reset_mock()
    mock_db_session.refresh.return_value = test_user

    response = client.post("/users/", json=payload)

    assert response.status_code == 201
    assert response.json()["message"] == "User created"

    mock_db_session.add.assert_called()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called()


def test_create_user_integrity_error(mock_db_session):
    
    mock_db_session.reset_mock()
    mock_db_session.commit.side_effect = IntegrityError("Simulated integrity error", None, None)

    response = client.post("/users/", json=payload)

    assert response.status_code == 409
    assert "already exists" in response.json()["message"]

    mock_db_session.add.assert_called()
    mock_db_session.commit.assert_called_once()


"""
---- DELETE USER UNIT TEST ----
"""


def test_delete_user(mock_db_session):
    
    mock_db_session.reset_mock()
    mock_db_session.commit.side_effect = None
    mock_db_session.query().filter().first.return_value = test_user
    
    response = client.delete("/users/1")
    
    assert response.status_code == 200
    
    mock_db_session.delete.assert_called_once()
    mock_db_session.commit.assert_called_once()