#TC1 - End-to-end flow: create board → create list → create card → add checklist → complete item → archive card → delete board.
#TC2 - Verify cascading behavior: deleting a board removes access to its lists/cards (404 on subsequent fetch).
#TC3 - Response time assertion: key endpoints respond within an acceptable threshold (e.g., <1s).