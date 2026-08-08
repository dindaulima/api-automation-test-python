import jsonschema

from schemas import CHECKLIST_SCHEMA


#TC1 - Add a checklist to a card
def test_add_checklist_to_card(api_client, test_card):
    response = api_client.create_checklist(test_card["id"], name="pytest-checklist")

    assert response.status_code == 200
    checklist = response.json()
    jsonschema.validate(checklist, CHECKLIST_SCHEMA)
    assert checklist["name"] == "pytest-checklist"
    assert checklist["idCard"] == test_card["id"]


#TC2 - Add checklist items
def test_add_checklist_items(api_client, test_card):
    checklist = api_client.create_checklist(test_card["id"], name="pytest-checklist").json()

    item_response = api_client.add_checklist_item(checklist["id"], name="pytest-item")

    assert item_response.status_code == 200
    item = item_response.json()
    assert item["name"] == "pytest-item"
    assert item["state"] == "incomplete"


#TC3 - Mark a checklist item complete
def test_mark_checklist_item_complete(api_client, test_card):
    checklist = api_client.create_checklist(test_card["id"], name="pytest-checklist").json()
    item = api_client.add_checklist_item(checklist["id"], name="pytest-item").json()

    update_response = api_client.update_checklist_item_state(
        test_card["id"], item["id"], state="complete"
    )

    assert update_response.status_code == 200
    assert update_response.json()["state"] == "complete"


#TC4 - Delete a checklist
def test_delete_checklist_removes_it_from_card(api_client, test_card):
    checklist = api_client.create_checklist(test_card["id"], name="pytest-checklist").json()

    delete_response = api_client.delete_checklist(checklist["id"])
    assert delete_response.status_code == 200

    card_checklists = api_client.get_checklists_for_card(test_card["id"])
    checklist_ids = [cl["id"] for cl in card_checklists.json()]
    assert checklist["id"] not in checklist_ids
