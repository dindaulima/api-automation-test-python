import requests

from config import TRELLO_API_KEY, TRELLO_API_TOKEN, TRELLO_BASE_URL


class TrelloClient:
    def __init__(self):
        self.base_url = TRELLO_BASE_URL
        self.auth_params = {"key": TRELLO_API_KEY, "token": TRELLO_API_TOKEN}

    def _request(self, method, path, **kwargs):
        url = f"{self.base_url}{path}"
        params = kwargs.pop("params", {})
        params.update(self.auth_params)
        return requests.request(method, url, params=params, **kwargs)

    # --- Boards ---
    def create_board(self, name, **extra_params):
        return self._request("POST", "/boards", params={"name": name, **extra_params})

    def get_board(self, board_id):
        return self._request("GET", f"/boards/{board_id}")

    def update_board(self, board_id, **fields):
        return self._request("PUT", f"/boards/{board_id}", params=fields)

    def delete_board(self, board_id):
        return self._request("DELETE", f"/boards/{board_id}")

    def get_boards_for_member(self, member="me"):
        return self._request("GET", f"/members/{member}/boards")

    # --- Lists ---
    def create_list(self, board_id, name, **extra_params):
        return self._request(
            "POST", "/lists", params={"name": name, "idBoard": board_id, **extra_params}
        )

    def get_lists_for_board(self, board_id):
        return self._request("GET", f"/boards/{board_id}/lists")

    def update_list(self, list_id, **fields):
        return self._request("PUT", f"/lists/{list_id}", params=fields)

    # --- Cards ---
    def create_card(self, list_id, name, **extra_params):
        return self._request(
            "POST", "/cards", params={"name": name, "idList": list_id, **extra_params}
        )

    def get_card(self, card_id):
        return self._request("GET", f"/cards/{card_id}")

    def update_card(self, card_id, **fields):
        return self._request("PUT", f"/cards/{card_id}", params=fields)

    def delete_card(self, card_id):
        return self._request("DELETE", f"/cards/{card_id}")

    # --- Checklists ---
    def create_checklist(self, card_id, name, **extra_params):
        return self._request(
            "POST", "/checklists", params={"idCard": card_id, "name": name, **extra_params}
        )

    def add_checklist_item(self, checklist_id, name, **extra_params):
        return self._request(
            "POST", f"/checklists/{checklist_id}/checkItems", params={"name": name, **extra_params}
        )
