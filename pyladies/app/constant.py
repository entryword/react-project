# encoding: UTF-8

FIELD_1_0 = {
    -1: "Not Specified",
    0: "Data Science",
    1: "Web",
    2: "Crawler",
    3: "Deep Learning",
    4: "Optimization",
    5: "Tutorial",
    6: "Application",
    7: "Experience",
    8: "Party",
    9: "IoT",
    10: "Finance",
    11: "Bot",
}

FREQ_1_0 = {
    0: "系列活動",
    1: "工作坊",
    2: "單次活動"
}

LEVEL_1_0 = {
    0: "無程式基礎者",
    1: "入門 - 了解基礎語法 (物件與命名、if else、加減乘除、def、....)",
    2: "進階 - 熟悉基礎語法與基本資料型態 (list、dict、tuple、…)",
    3: "精通 - 熟悉產生器、裝飾器、OOP，並有專案開發經驗"
}

HOST_1_0 = {
    0: "PyLadies 主辦",
    1: "PyLadies 合辦",
    2: "PyLadies 受邀"
}

STATUS_1_0 = {
    0: "已結束",
    1: "未來活動"
}

WEEKDAY_1_0 = {
    0: "Sunday",
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday"
}

TIME_1_0 = {
    0: "上午 (00:00-11:59)",
    1: "下午 (12:00-16:59)",
    2: "晚上 (17:00-23:59)"
}

CHANNEL_1_0 = {
    0: "Meetup",
    1: "Accupass"
}

TYPE_1_0 = {
    "one": "每次分開報名",
    "all": "一次報名整系列"
}

ACCESS_TYPE_1_0 = {
    0: "No Access",
    1: "Read",
    2: "Write"
}

class CheckInListStatus:
    CHECK_IN = 1
    NO_CHECK_IN = 0


class TicketType:
    COMMON = 1  # 一般人
    STUDENT = 2  # 學生
    OTHER = 3  # 其他


TICKET_TYPE_1_0 = {
    TicketType.COMMON: "Common",
    TicketType.STUDENT: "Student",
    TicketType.OTHER: "Other"
}


CHECK_IN_LIST_STATUS_1_0 = {
    CheckInListStatus.CHECK_IN: "Check In",
    CheckInListStatus.NO_CHECK_IN: "No Check In"
}


DEFINITION_1_0 = {
    "field": FIELD_1_0,
    "freq": FREQ_1_0,
    "level": LEVEL_1_0,
    "host": HOST_1_0,
    "status": STATUS_1_0,
    "weekday": WEEKDAY_1_0,
    "time": TIME_1_0,
    "channel": CHANNEL_1_0,
    "type": TYPE_1_0,
    "access_type": ACCESS_TYPE_1_0,
    "ticket_type": TICKET_TYPE_1_0,
    "check_in_list_status": CHECK_IN_LIST_STATUS_1_0
}

DEFAULT_PLACE_ID = 37
DEFAULT_FIELD_ID = -1

class UserType:
    ADMIN = 'Admin'
    MEMBER = 'Member'
