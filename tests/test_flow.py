import logging
import uuid
from urllib.parse import urlsplit

logger = logging.getLogger(__name__)

RESPONSE_TIME_THRESHOLD_MS = 1000


def _log_response_time(response):
    redacted_url = urlsplit(response.request.url)._replace(query="").geturl()
    elapsed_ms = response.elapsed.total_seconds() * 1000
    logger.info("%s %s took %.0fms", response.request.method, redacted_url, elapsed_ms)
    return elapsed_ms


#TC1 - End-to-end flow: create board → create list → create card → add checklist → complete item → archive card → delete board.
def test_end_to_end_board_to_card_flow(api_client):
    board = api_client.create_board(name=f"pytest-flow-board-{uuid.uuid4().hex[:8]}").json()

    list_response = api_client.create_list(board["id"], name="pytest-flow-list")
    assert list_response.status_code == 200
    trello_list = list_response.json()

    card_response = api_client.create_card(trello_list["id"], name="pytest-flow-card")
    assert card_response.status_code == 200
    card = card_response.json()

    checklist_response = api_client.create_checklist(card["id"], name="pytest-flow-checklist")
    assert checklist_response.status_code == 200
    checklist = checklist_response.json()

    item_response = api_client.add_checklist_item(checklist["id"], name="pytest-flow-item")
    assert item_response.status_code == 200
    item = item_response.json()

    complete_response = api_client.update_checklist_item_state(card["id"], item["id"], state="complete")
    assert complete_response.status_code == 200
    assert complete_response.json()["state"] == "complete"

    archive_response = api_client.update_card(card["id"], closed="true")
    assert archive_response.status_code == 200
    assert archive_response.json()["closed"] is True

    delete_response = api_client.delete_board(board["id"])
    assert delete_response.status_code == 200


#TC2 - Verify cascading behavior: deleting a board removes access to its lists/cards (404 on subsequent fetch).
def test_deleting_board_cascades_to_lists_and_cards(api_client, test_board, test_list, test_card):
    delete_response = api_client.delete_board(test_board["id"])
    assert delete_response.status_code == 200

    assert api_client.get_board(test_board["id"]).status_code == 404
    assert api_client.get_lists_for_board(test_board["id"]).status_code == 404
    assert api_client.get_card(test_card["id"]).status_code == 404


#TC3 - Response time assertion: key endpoints respond within an acceptable threshold (<1000ms).
def test_get_board_response_time_within_threshold(api_client, test_board):
    response = api_client.get_board(test_board["id"])
    elapsed_ms = _log_response_time(response)

    assert response.status_code == 200
    assert elapsed_ms < RESPONSE_TIME_THRESHOLD_MS


def test_get_card_response_time_within_threshold(api_client, test_card):
    response = api_client.get_card(test_card["id"])
    elapsed_ms = _log_response_time(response)

    assert response.status_code == 200
    assert elapsed_ms < RESPONSE_TIME_THRESHOLD_MS
