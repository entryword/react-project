_cms_page_list = [
    "EventList",
    "Event",
    "EventRegister",
    "SpeakerList",
    "Speaker",
    "PlaceList",
    "Place",
    "UserList",
    "Role",
]

_properties_dict = {
    k: {"type": "integer", "minimum": 0, "maximum": 2} for k in _cms_page_list
}

schema_create = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 1, "maxLength": 100},
        "permission": {
            "type": "object",
            "properties": _properties_dict,
            "required": _cms_page_list,
        }
    },
    "required": ["name", "permission"]
}
