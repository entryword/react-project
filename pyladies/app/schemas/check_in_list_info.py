

create_schema = {
    "type": "object",
    "properties": {
        "event_basic_sn": {"type": "integer"},
        "name": {"type": "string"},
        "mail": {"type": "string"},
        "phone": {"type": "string"},
        "ticket_type": {"type": "integer"},
        "ticket_amount": {"type": "integer"},
        "remark": {
            "anyOf": [
                {"type": "string"},
                {"type": "null"}
            ]
        },
        "status": {"type": "integer"}
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
        "name": {"type": "string"},
        "mail": {"type": "string"},
        "phone": {"type": "string"},
        "ticket_type": {"type": "integer"},
        "ticket_amount": {"type": "integer"},
        "remark": {
            "anyOf": [
                {"type": "string"},
                {"type": "null"}
            ]
        },
        "status": {"type": "integer"}
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