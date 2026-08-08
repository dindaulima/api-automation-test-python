BOARD_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "closed", "url"],
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "closed": {"type": "boolean"},
        "url": {"type": "string"},
    },
}

LIST_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "closed", "idBoard"],
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "closed": {"type": "boolean"},
        "idBoard": {"type": "string"},
    },
}

CARD_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "closed", "idList", "idBoard", "due", "desc", "labels", "idMembers"],
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "closed": {"type": "boolean"},
        "idList": {"type": "string"},
        "idBoard": {"type": "string"},
        "due": {"type": ["string", "null"]},
        "desc": {"type": "string"},
        "labels": {"type": "array"},
        "idMembers": {"type": "array"},
    },
}

CHECKLIST_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "idCard", "checkItems"],
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "idCard": {"type": "string"},
        "checkItems": {"type": "array"},
    },
}
