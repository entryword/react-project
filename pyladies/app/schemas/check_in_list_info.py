from app.constant import TICKET_TYPE_1_0, CHECK_IN_LIST_STATUS_1_0

create_schema = {
    "type": "object",
    "properties": {
        "event_basic_sn": {"type": "integer"},
        "name": {
            "type": "string",
            "minLength": 1
        },
        "mail": {
            "type": "string",
            "minLength": 1
        },
        "phone": {
            "type": "string",
            "minLength": 1
        },
        "ticket_type": {"type": "integer", "enum": list(TICKET_TYPE_1_0.keys())},
        "ticket_amount": {"type": "integer"},
        "remark": {
            "anyOf": [
                {"type": "string"},
                {"type": "null"}
            ]
        },
        "status": {"type": "integer", "enum": list(CHECK_IN_LIST_STATUS_1_0.keys())}
    },
    "required": [
        "event_basic_sn",
        "name",
        "mail",
        "phone",
        "ticket_type",
        "ticket_amount",
        "remark",
        "status"
    ]
}

update_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "minLength": 1
        },
        "mail": {
            "type": "string",
            "minLength": 1
        },
        "phone": {
            "type": "string",
            "minLength": 1
        },
        "ticket_type": {"type": "integer", "enum": list(TICKET_TYPE_1_0.keys())},
        "ticket_amount": {"type": "integer"},
        "remark": {
            "anyOf": [
                {"type": "string"},
                {"type": "null"}
            ]
        },
        "status": {"type": "integer", "enum": list(CHECK_IN_LIST_STATUS_1_0.keys())}
    },
    "required": [
        "name",
        "mail",
        "phone",
        "ticket_type",
        "ticket_amount",
        "remark",
        "status"
    ]
}