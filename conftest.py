import logging
import uuid
from urllib.parse import urlsplit

import pytest
import requests

from clients.trello_client import TrelloClient

logger = logging.getLogger("perf")
RESPONSE_TIME_THRESHOLD_MS = 1000


@pytest.fixture(autouse=True)
def assert_every_request_is_fast(monkeypatch):
    """Wraps requests.request so every HTTP call in every test is timed and asserted."""
    original_request = requests.request

    def timed_request(method, url, *args, **kwargs):
        response = original_request(method, url, *args, **kwargs)
        elapsed_ms = response.elapsed.total_seconds() * 1000
        redacted_url = urlsplit(url)._replace(query="").geturl()
        logger.info("%s %s took %.0fms", method, redacted_url, elapsed_ms)

        assert elapsed_ms < RESPONSE_TIME_THRESHOLD_MS, (
            f"{method} {redacted_url} took {elapsed_ms:.0f}ms "
            f"(threshold {RESPONSE_TIME_THRESHOLD_MS}ms)"
        )
        return response

    monkeypatch.setattr(requests, "request", timed_request)


@pytest.fixture(scope="session")
def api_client():
    return TrelloClient()


@pytest.fixture
def test_board(api_client):
    """Creates a fresh board for a test and deletes it afterward."""
    board_name = f"pytest-board-{uuid.uuid4().hex[:8]}"
    response = api_client.create_board(name=board_name)
    assert response.status_code == 200, f"Setup failed: {response.text}"
    board = response.json()

    yield board

    api_client.delete_board(board["id"])


@pytest.fixture
def test_list(api_client, test_board):
    """Creates a list on top of test_board."""
    list_name = f"pytest-list-{uuid.uuid4().hex[:8]}"
    response = api_client.create_list(test_board["id"], name=list_name)
    assert response.status_code == 200, f"Setup failed: {response.text}"
    return response.json()


@pytest.fixture
def test_card(api_client, test_list):
    """Creates a card on top of test_list."""
    card_name = f"pytest-card-{uuid.uuid4().hex[:8]}"
    response = api_client.create_card(test_list["id"], name=card_name)
    assert response.status_code == 200, f"Setup failed: {response.text}"
    return response.json()
