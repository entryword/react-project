schema_create = {
    "type": "object",
    "properties": {
        "topic_id": {
            "anyOf": [
                {"type": "integer"},
                {"type": "null"}
            ]
        },
        "start_date": {"type": "string"},
        "start_time": {"type": "string"},
        "end_time": {"type": "string"},
        "place_id": {
            "anyOf": [
                {"type": "integer"},
                {"type": "null"}
            ]
        },
        "title": {"type": "string"},
        "desc": {"type": "string"},
        "field_ids": {
            "type": "array",
            "items": {
                "type": "number"
            }
        },
        "speaker_ids": {
            "type": "array",
            "items": {
                "type": "number"
            }
        },
        "assistant_ids": {
            "type": "array",
            "items": {
                "type": "number"
            }
        }
    },
    "required": [
        "start_date",
        "start_time",
        "end_time",
        "title",
        "desc",
        "field_ids",
        "speaker_ids",
        "assistant_ids",
    ]
}
