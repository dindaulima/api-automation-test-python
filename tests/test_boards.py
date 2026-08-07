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
