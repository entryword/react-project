from app.constant import CHANNEL_1_0, TYPE_1_0


schema_create = {
    "type": "object",
    "properties": {
        "event_basic_id": {"type": "integer", "minimum": 1},
        "apply": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "host": {"type": "string", "minLength": 1, "maxLength": 100},
                    "channel": {"type": "integer", "enum": list(CHANNEL_1_0.keys())},
                    "type": {"type": "string", "enum": list(TYPE_1_0.keys())},
                    "start_time": {"type": "string", "minLength": 1},
                    "end_time": {"type": "string", "minLength": 1},
                    "price": {"type": "string", "minLength": 1},
                    "limit": {"type": "string", "minLength": 1},
                    "url": {"type": "string"},
                    "qualification": {"type": "string"}
                },
                "required": ["host", "channel", "type", "start_time", "end_time", "price", "limit", "url"]
            },
            "uniqueItems": True,
            "minItems": 1
        }
    },
    "required": ["event_basic_id", "apply"]
}
