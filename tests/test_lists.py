import jsonschema

from schemas import LIST_SCHEMA


#TC1 - Create a list on a valid board
def test_create_list_on_a_valid_board(api_client, test_board, test_list):
    assert test_list["name"].startswith("pytest-list-")
    assert test_board["id"] == test_list["idBoard"]


#TC2 - Create a list on a non-existent board → 401
def test_create_list_on_nonexistent_board_is_rejected(api_client):
    response = api_client.create_list("000000000000000000000000", name="pytest-list")

    assert response.status_code == 401


#TC3 - Get all lists on a board → newly created list is present.
def test_get_lists_for_board_includes_new_list(api_client, test_board, test_list):
    response = api_client.get_lists_for_board(test_board["id"])

    assert response.status_code == 200
    lists = response.json()
    for lst in lists:
        jsonschema.validate(lst, LIST_SCHEMA)
    list_ids = [lst["id"] for lst in lists]
    assert test_list["id"] in list_ids


#TC4 - Archive (close) a list
def test_archive_list_sets_closed_true(api_client, test_list):
    update_response = api_client.update_list(test_list["id"], closed="true")
    assert update_response.status_code == 200
    assert update_response.json()["closed"] is True


#TC5 - Rename a list
def test_rename_list(api_client, test_board, test_list):
    new_name = "renamed-pytest-list"

    update_response = api_client.update_list(test_list["id"], name=new_name)
    assert update_response.status_code == 200

    get_response = api_client.get_lists_for_board(test_board["id"])
    lists_by_id = {lst["id"]: lst for lst in get_response.json()}
    assert lists_by_id[test_list["id"]]["name"] == new_name


#TC6 - Create a list with missing name param → 400.
def test_create_list_without_name_is_rejected(api_client, test_board):
    response = api_client.create_list(test_board["id"], name="")

    assert response.status_code == 400
