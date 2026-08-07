import pytest
import requests

from config import TRELLO_API_KEY, TRELLO_API_TOKEN, TRELLO_BASE_URL


#TC1 - Missing API key → 401.
def test_missing_api_key_returns_401():
    response = requests.get(
        f"{TRELLO_BASE_URL}/members/me", params={"token": TRELLO_API_TOKEN}
    )

    assert response.status_code == 401


#TC2 - Missing token → 400.
def test_missing_token_returns_400():
    response = requests.get(
        f"{TRELLO_BASE_URL}/members/me", params={"key": TRELLO_API_KEY}
    )

    assert response.status_code == 400


#TC3 - Invalid key/token combo → 401.
def test_invalid_key_and_token_returns_401():
    response = requests.get(
        f"{TRELLO_BASE_URL}/members/me",
        params={"key": "invalidkey123", "token": "invalidtoken123"},
    )

    assert response.status_code == 401


#TC4 - invalid board ID → 400.
def test_malformed_board_id_returns_400(api_client):
    response = api_client.get_board("not-a-valid-id")

    assert response.status_code == 400


#TC5 - Wrong HTTP method on a read-only path → 404.
# DELETE isn't a supported verb on /members/me
def test_delete_on_members_me_returns_404():
    response = requests.delete(
        f"{TRELLO_BASE_URL}/members/me",
        params={"key": TRELLO_API_KEY, "token": TRELLO_API_TOKEN},
    )

    assert response.status_code == 404


#TC6 - SQL/script injection-style strings in name fields → stored safely as plain text, not executed.
def test_injection_style_name_is_stored_as_plain_text(api_client):
    payload = "<script>alert(1)</script>'; DROP TABLE users; --"

    response = api_client.create_board(name=payload)

    assert response.status_code == 200
    board = response.json()
    assert board["name"] == payload

    api_client.delete_board(board["id"])
