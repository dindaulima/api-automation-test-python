class TestChecklists:
    #TC1 - Add a checklist to a card → verify created.
    def test_add_checklist_to_card(self, api_client, test_card):
        response = api_client.create_checklist(test_card["id"], name="pytest-checklist")

        assert response.status_code == 200
        checklist = response.json()
        assert checklist["name"] == "pytest-checklist"
        assert checklist["idCard"] == test_card["id"]

    #TC2 - Add checklist items → verify items appear with state: incomplete.
    def test_add_checklist_items(self, api_client, test_card):
        checklist = api_client.create_checklist(test_card["id"], name="pytest-checklist").json()

        item_response = api_client.add_checklist_item(checklist["id"], name="pytest-item")

        assert item_response.status_code == 200
        item = item_response.json()
        assert item["name"] == "pytest-item"
        assert item["state"] == "incomplete"

    #TC3 - Mark a checklist item complete → verify state change.
    def test_mark_checklist_item_complete(self, api_client, test_card):
        checklist = api_client.create_checklist(test_card["id"], name="pytest-checklist").json()
        item = api_client.add_checklist_item(checklist["id"], name="pytest-item").json()

        update_response = api_client.update_checklist_item_state(
            test_card["id"], item["id"], state="complete"
        )

        assert update_response.status_code == 200
        assert update_response.json()["state"] == "complete"

    #TC4 - Delete a checklist → verify removed from card.
    def test_delete_checklist_removes_it_from_card(self, api_client, test_card):
        checklist = api_client.create_checklist(test_card["id"], name="pytest-checklist").json()

        delete_response = api_client.delete_checklist(checklist["id"])
        assert delete_response.status_code == 200

        card_checklists = api_client.get_checklists_for_card(test_card["id"])
        checklist_ids = [cl["id"] for cl in card_checklists.json()]
        assert checklist["id"] not in checklist_ids
