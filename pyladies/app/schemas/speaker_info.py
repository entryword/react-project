schema_create = {
    "type": "object",
    "properties": {
        "data": {
            "required": [
                "name",
                "title",
            ],
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "title": {"type": "string"},
                "major_related": {"type": "boolean"},
                "fields": {
                    "type": "array",
                    "items": {
                        "type": "integer"
                    }
                },
                "intro": {"type": "string"},
                "links": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "type": {"type": "string"},
                            "url": {"type": "string"}
                        }
                    }
                },
                "photo": {"type": "string"},
            }
        },
    },
}
