import requests

from config import TRELLO_API_KEY, TRELLO_BASE_URL

class TestLists:
    #TC1 - Create a list on a valid board → correct name and idBoard.
    def test_create_list_on_a_valid_board(self, api_client, test_board, test_list):
        assert test_list["name"].startswith("pytest-list-")
        assert test_board["id"] == test_list["idBoard"]

    #TC2 - Create a list on a non-existent board → Trello returns 401
    def test_create_list_on_nonexistent_board_is_rejected(self, api_client):
        response = api_client.create_list("000000000000000000000000", name="pytest-list")

        assert response.status_code == 401

    #TC3 - Get all lists on a board → newly created list is present.
    def test_get_lists_for_board_includes_new_list(self, api_client, test_board, test_list):
        response = api_client.get_lists_for_board(test_board["id"])

        assert response.status_code == 200
        list_ids = [lst["id"] for lst in response.json()]
        print(list_ids)
        assert test_list["id"] in list_ids

    #TC4 - Archive (close) a list → verify closed: true.
    def test_archive_list_sets_closed_true(self, api_client, test_list):
        update_response = api_client.update_list(test_list["id"], closed="true")
        assert update_response.status_code == 200
        assert update_response.json()["closed"] is True

    #TC5 - Rename a list → verify updated name via GET.
    def test_rename_list(self, api_client, test_board, test_list):
        new_name = "renamed-pytest-list"

        update_response = api_client.update_list(test_list["id"], name=new_name)
        assert update_response.status_code == 200

        get_response = api_client.get_lists_for_board(test_board["id"])
        lists_by_id = {lst["id"]: lst for lst in get_response.json()}
        assert lists_by_id[test_list["id"]]["name"] == new_name

    #TC6 - Create a list with missing name param → expect 400.
    def test_create_list_without_name_is_rejected(self, api_client, test_board):
        response = api_client.create_list(test_board["id"], name="")

        assert response.status_code == 400