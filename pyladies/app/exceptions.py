class PyLadiesException(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code
        self.message = message

# [0~999] preserved
_msg = "Perform the action successfully."
OK = PyLadiesException(0, _msg)
_msg = "Unable to perform the action. Please check the format of input is correct, and try again."
INVALID_INPUT = PyLadiesException(1, _msg)

# [1000~1099] topic
_msg = "Unable to perform the action. Topic doesn't exist."
TOPIC_NOT_EXIST = PyLadiesException(1000, _msg)

_invalid_msg = "Invalid parameter '%s' to perform the action."
_msg = "Unable to perform the action."
TOPICLIST_INVALID_KEYWORD = PyLadiesException(1050, _invalid_msg % "keyword")
TOPICLIST_INVALID_LEVEL = PyLadiesException(1051, _invalid_msg % "level")
TOPICLIST_INVALID_FREQ = PyLadiesException(1052, _invalid_msg % "freq")
TOPICLIST_INVALID_HOST = PyLadiesException(1053, _invalid_msg % "host")
TOPICLIST_INVALID_FIELDS = PyLadiesException(1054, _invalid_msg % "fields")
TOPICLIST_ERROR = PyLadiesException(1055, _msg)

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

_invalid_msg = "Invalid parameter '%s' to perform the action."
_msg = "Unable to perform the action."
SPEAKERLIST_INVALID_KEYWORD = PyLadiesException(1450, _invalid_msg % "keyword")
SPEAKERLIST_INVALID_FIELDS = PyLadiesException(1451, _invalid_msg % "fields")
SPEAKERLIST_ERROR = PyLadiesException(1452, _msg)

# [1500~1599] place
_msg = "Unable to perform the action. Place doesn't exist."
PLACE_NOT_EXIST = PyLadiesException(1500, _msg)
_msg = "Unable to perform the action. Place name is duplicate."
PLACE_NAME_DUPLICATE = PyLadiesException(1501, _msg)

# [1600~1699] apply
_msg = "Unable to perform the action. Apply doesn't exist."
APPLY_NOT_EXIST = PyLadiesException(1600, _msg)

# [1700~1799] user
_msg = "Unable to perform the action. User doesn't exist."
USER_NOT_EXIST = PyLadiesException(1700, _msg)
_msg = "Failed to log in. Please check username and password are correct, and try again."
USER_LOGIN_FAILED = PyLadiesException(1701, _msg)
_msg = "Unable to perform the action. Please log in first."
USER_LOGIN_REQUIRED = PyLadiesException(1702, _msg)

# [1800~1899] role
_msg = "Unable to perform the action. Role doesn't exist."
ROLE_NOT_EXIST = PyLadiesException(1800, _msg)
_msg = "Unable to perform the action. Role name is duplicate."
ROLE_NAME_DUPLICATE = PyLadiesException(1801, _msg)

# [1900~1999] check in list
_msg = "Record is not exist"
RECORD_NOT_EXIST = PyLadiesException(1900, _msg)
RECORD_IS_EXIST = PyLadiesException(1901, _msg)
FILE_REQUIRED = PyLadiesException(1902, _msg)

# [8000~8099] routing
_msg = "Routing Not Found"
ROUTING_NOT_FOUND = PyLadiesException(8000, _msg)

# [9000~]
_msg = "Unexpected error occurs. If the issue is persistent, please contact the administrator."
UNEXPECTED_ERROR = PyLadiesException(9000, _msg)
