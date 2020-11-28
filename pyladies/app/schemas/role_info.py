cms_page_list = [
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
permission_constraint = {"type": "integer", "minimum": 0, "maximum": 2}
properties_dict = {}
_ = [properties_dict.update({k: permission_constraint}) for k in cms_page_list]

schema_create = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 1, "maxLength": 100},
        "permission": {
            "type": "object",
            "properties": properties_dict,
            "required": cms_page_list,
        }
    },
    "required": ["name", "permission"]
}
