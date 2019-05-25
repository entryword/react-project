schema_login = {
    "type": "object",
    "properties": {
        "username": {"type": "string", "minLength": 1, "maxLength": 64},
        "password": {"type": "string", "minLength": 1, "maxLength": 64}
    },
    "required": ["username", "password"]
}
