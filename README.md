# Trello API Automation Tests

API automation test suite for the [Trello API](https://developer.atlassian.com/cloud/trello/), built with `pytest` and `requests`.

## Tech Stack

- **pytest** — test runner
- **requests** — HTTP client
- **python-dotenv** — loads credentials from `.env`
- **pytest-html** — generates HTML test reports
- **jsonschema** — (optional) response schema validation

## Project Structure

```
.
├── .env                     # Trello credentials (not committed)
├── config.py                # loads env vars, fails fast if missing
├── conftest.py               # shared fixtures (api_client, test_board, test_list)
├── pytest.ini
├── requirements.txt
├── clients/
│   └── trello_client.py      # thin wrapper around the Trello REST API
└── tests/
    └── test_boards.py        # board create/get/update + negative cases
```

## Setup

1. Create a virtual environment and activate it:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Get your Trello credentials from https://trello.com/power-ups/admin:
   - **API Key** — shown on your Power-Up's "API Key" tab
   - **Token** — generated via the "Token" link on the same page (NOT the API secret)

4. Fill in `.env`:
   ```
   TRELLO_API_KEY=your_api_key
   TRELLO_API_TOKEN=your_token
   TRELLO_BASE_URL=https://api.trello.com/1
   ```

## Running Tests

Run the full suite:
```bash
pytest
```

Run with an HTML report:
```bash
pytest --html=report.html --self-contained-html
```

Run a single file or test:
```bash
pytest tests/test_boards.py
pytest tests/test_boards.py::test_create_board_with_valid_name
```

## How Test Data Works

- Fixtures in `conftest.py` create disposable resources (e.g. a uniquely named board via `test_board`) before each test and delete them afterward, so tests don't leave data on your Trello account or interfere with each other.
- Board/list/card names used mid-test are currently hardcoded per test case; this will move to a shared data module as more parametrized/negative cases are added.

## Test Coverage

| Resource | File | Status |
|---|---|---|
| Boards | `tests/test_boards.py` | 7 scenarios implemented |
| Lists | `tests/test_lists.py` | 6 scenarios implemented |
| Cards | `tests/test_cards.py` | in progress |
| Checklists | `tests/test_checklists.py` | in progress |
| Negative/Auth | `tests/test_negative_cases.py` | planned |
