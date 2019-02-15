class PyLadiesException(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code
        self.message = message

# [0~999] preserved
_msg = "Perform the action successfully."
OK = PyLadiesException(0, _msg)

# [1000~1099] topic
_msg = "Unable to perform the action. Topic doesn't exist."
TOPIC_NOT_EXIST = PyLadiesException(1000, _msg)

# [1100~1199] event basic
_msg = "Unable to perform the action. EventBasic doesn't exist."
EVENTBASIC_NOT_EXIST = PyLadiesException(1100, _msg)

_invalid_msg = "Invalid parameter '%s' to perform the action."
_msg = "Unable to perform the action."
EVENTLIST_INVALID_KEYWORD = PyLadiesException(1150, _invalid_msg % "keyword")
EVENTLIST_INVALID_DATE = PyLadiesException(1151, _invalid_msg % "date")
EVENTLIST_INVALID_SORT = PyLadiesException(1152, _invalid_msg % "sort")
EVENTLIST_INVALID_ORDER = PyLadiesException(1153, _invalid_msg % "order")
EVENTLIST_ERROR = PyLadiesException(1154, _msg)

# [1200~1299] event info
_msg = "Unable to perform the action. EventInfo doesn't exist."
EVENTINFO_NOT_EXIST = PyLadiesException(1200, _msg)

# [1300~1399] slide resource
_msg = "Unable to perform the action. SlideResource doesn't exist."
SLIDERESOURCE_NOT_EXIST = PyLadiesException(1300, _msg)

# [1400~1499] speaker
_msg = "Unable to perform the action. Speaker doesn't exist."
SPEAKER_NOT_EXIST = PyLadiesException(1400, _msg)

# [1500~1599] place
_msg = "Unable to perform the action. Place doesn't exist."
PLACE_NOT_EXIST = PyLadiesException(1500, _msg)

# [8000~8099] routing
_msg = "Routing Not Found"
ROUTING_NOT_FOUND = PyLadiesException(8000, _msg)

# [9000~]
_msg = "Unexpected error occurs. If the issue is persistent, please contact the administrator."
UNEXPECTED_ERROR = PyLadiesException(9000, _msg)
