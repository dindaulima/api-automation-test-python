import logging
from urllib.parse import urlsplit

logger = logging.getLogger(__name__)

RESPONSE_TIME_THRESHOLD_MS = 1000


def _log_response_time(response):
    redacted_url = urlsplit(response.request.url)._replace(query="").geturl()
    elapsed_ms = response.elapsed.total_seconds() * 1000
    logger.info("%s %s took %.0fms", response.request.method, redacted_url, elapsed_ms)
    return elapsed_ms


#TC1 - Response time assertion for Board (<1000ms).
def test_get_board_response_time_within_threshold(api_client, test_board):
    response = api_client.get_board(test_board["id"])
    elapsed_ms = _log_response_time(response)

    assert response.status_code == 200
    assert elapsed_ms < RESPONSE_TIME_THRESHOLD_MS

#TC2 - Response time assertion for List (<1000ms).
def test_get_list_response_time_within_threshold(api_client, test_board, test_list):
    response = api_client.get_lists_for_board(test_board["id"])
    elapsed_ms = _log_response_time(response)

    assert response.status_code == 200
    assert elapsed_ms < RESPONSE_TIME_THRESHOLD_MS

#TC3 - Response time assertion for Card (<1000ms).
def test_get_card_response_time_within_threshold(api_client, test_card):
    response = api_client.get_card(test_card["id"])
    elapsed_ms = _log_response_time(response)

    assert response.status_code == 200
    assert elapsed_ms < RESPONSE_TIME_THRESHOLD_MS
