class PyLadiesException(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code
        self.message = message

# [0~999] preserved
OK = PyLadiesException(0, "Perform the action successfully.")

# [1000~1099] topic
TOPIC_NOT_EXIST = PyLadiesException(1000, "Unable to perform the action. Topic doesn't exist.")

# [1100~1199] event basic
EVENTBASIC_NOT_EXIST = PyLadiesException(1100, "Unable to perform the action. EventBasic doesn't exist.")

# [1200~1299] event info
EVENTINFO_NOT_EXIST = PyLadiesException(1200, "Unable to perform the action. EventInfo doesn't exist.")

# [1300~1399] slide resource
SLIDERESOURCE_NOT_EXIST = PyLadiesException(1300, "Unable to perform the action. SlideResource doesn't exist.")

# [1400~1499] speaker
SPEAKER_NOT_EXIST = PyLadiesException(1400, "Unable to perform the action. Speaker doesn't exist.")

# [1500~1599] place
PLACE_NOT_EXIST = PyLadiesException(1500, "Unable to perform the action. Place doesn't exist.")

# [8000~8099] routing
ROUTING_NOT_FOUND = PyLadiesException(8000, "Routing Not Found")

# [9000~]
UNEXPECTED_ERROR = PyLadiesException(9000, "Unexpected error occurs. If the issue is persistent, please contact the administrator.")