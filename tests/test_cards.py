#TC1 - Create a card on a valid list
def test_create_card_on_a_valid_list(api_client, test_list, test_card):
    assert test_card["name"].startswith("pytest-card-")
    assert test_card["idList"] == test_list["id"]
    assert test_card["due"] is None


#TC2 - Create a card with a due date
def test_create_card_with_due_date(api_client, test_list):
    due_date = "2026-12-31T00:00:00.000Z"

    response = api_client.create_card(test_list["id"], name="pytest-card-due", due=due_date)

    assert response.status_code == 200
    assert response.json()["due"] == due_date


#TC3 - Get a card by ID
def test_get_card_by_id(api_client, test_card):
    response = api_client.get_card(test_card["id"])

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == test_card["id"]
    assert body["name"] == test_card["name"]


#TC4 - Update card name/description
def test_update_card_name_and_description(api_client, test_card):
    new_name = "renamed-pytest-card"
    new_desc = "updated by pytest"

    update_response = api_client.update_card(test_card["id"], name=new_name, desc=new_desc)
    assert update_response.status_code == 200

    get_response = api_client.get_card(test_card["id"])
    body = get_response.json()
    assert body["name"] == new_name
    assert body["desc"] == new_desc


#TC5 - Move a card to a different list
def test_move_card_to_different_list(api_client, test_board, test_card):
    other_list_response = api_client.create_list(test_board["id"], name="pytest-other-list")
    other_list = other_list_response.json()

    update_response = api_client.update_card(test_card["id"], idList=other_list["id"])

    assert update_response.status_code == 200
    assert update_response.json()["idList"] == other_list["id"]


#TC6 - Archive a card
def test_archive_card_sets_closed_true(api_client, test_card):
    update_response = api_client.update_card(test_card["id"], closed="true")

    assert update_response.status_code == 200
    assert update_response.json()["closed"] is True


#TC7 - Delete a card
def test_delete_card_removes_it(api_client, test_card):
    delete_response = api_client.delete_card(test_card["id"])
    assert delete_response.status_code == 200

    get_response = api_client.get_card(test_card["id"])
    assert get_response.status_code == 404


#TC8 - Create a card on a non-existent list -> 404
def test_create_card_on_nonexistent_list_is_rejected(api_client):
    response = api_client.create_card("000000000000000000000000", name="pytest-card")

    assert response.status_code == 404


#TC9 - Add a label to a card → verify label appears in card's labels.
def test_add_label_to_card(api_client, test_board, test_card):
    label_response = api_client.create_label(test_board["id"], name="pytest-label", color="green")
    label = label_response.json()

    add_response = api_client.add_label_to_card(test_card["id"], label["id"])
    assert add_response.status_code == 200

    get_response = api_client.get_card(test_card["id"])
    label_ids = [lbl["id"] for lbl in get_response.json()["labels"]]

    assert label["id"] in label_ids


#TC10 - Add a member to a card → verify idMembers updated.
def test_add_member_to_card(api_client, test_card):
    me = api_client.get_current_member().json()

    add_response = api_client.add_member_to_card(test_card["id"], me["id"])
    assert add_response.status_code == 200

    get_response = api_client.get_card(test_card["id"])
    assert me["id"] in get_response.json()["idMembers"]


#TC11 - Add a comment to a card → verify comment appears in card actions.
def test_add_comment_to_card(api_client, test_card):
    comment_text = "this is a pytest comment"

    add_response = api_client.add_comment_to_card(test_card["id"], comment_text)
    assert add_response.status_code == 200

    actions_response = api_client.get_card_actions(test_card["id"], filter="commentCard")
    comments = [action["data"]["text"] for action in actions_response.json()]
    assert comment_text in comments


#TC12 - Create card with invalid due date format → expect 400.
def test_create_card_with_invalid_due_date_is_rejected(api_client, test_list):
    response = api_client.create_card(test_list["id"], name="pytest-card-bad-due", due="not-a-date")

    assert response.status_code == 400
