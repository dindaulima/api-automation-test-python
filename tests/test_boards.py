import jsonschema
import requests

from config import TRELLO_API_KEY, TRELLO_BASE_URL
from schemas import BOARD_SCHEMA


# TC1 - Create board with valid name
def test_create_board_with_valid_name(api_client, test_board):
    assert test_board["name"].startswith("pytest-board-")
    assert test_board["closed"] is False
    assert "id" in test_board


#TC2 - Get board by ID
def test_get_board_by_id(api_client, test_board):
    response = api_client.get_board(test_board["id"])

    assert response.status_code == 200
    body = response.json()
    jsonschema.validate(body, BOARD_SCHEMA)
    assert body["id"] == test_board["id"]
    assert body["name"] == test_board["name"]


# TC3 - Update board name
def test_update_board_name(api_client, test_board):
    new_name = "renamed-pytest-board"

    update_response = api_client.update_board(test_board["id"], name=new_name)
    assert update_response.status_code == 200

    get_response = api_client.get_board(test_board["id"])
    assert get_response.json()["name"] == new_name


# TC4 - Create board with empty name → 400
def test_create_board_with_empty_name_is_rejected(api_client):
    response = api_client.create_board(name="")

    assert response.status_code == 400


# TC5 - Get board with non-existent ID → 404
def test_get_nonexistent_board_returns_404(api_client):
    response = api_client.get_board("000000000000000000000000")

    assert response.status_code == 404


# TC6 - Delete board → verify it's gone
def test_delete_board_removes_it(api_client, test_board):
    delete_response = api_client.delete_board(test_board["id"])
    assert delete_response.status_code == 200

    get_response = api_client.get_board(test_board["id"])
    assert get_response.status_code == 404


# TC7 - Get board with invalid token → 401
def test_get_board_with_invalid_token_returns_401(test_board):
    response = requests.get(
        f"{TRELLO_BASE_URL}/boards/{test_board['id']}",
        params={"key": TRELLO_API_KEY, "token": "invalid_token_0000000000"},
    )

    assert response.status_code == 401
