from datetime import datetime, timedelta
from random import choice, randint, sample
import pytest
from app import constant

FREQS = list(constant.FREQ_1_0.keys())
LEVELS = list(constant.LEVEL_1_0.keys())
HOSTS = list(constant.HOST_1_0.keys())
FIELDS = list(constant.FIELD_1_0.keys())

# topc_info
def _get_topic_infos(length=1):
    topics = []
    for i in range(length):
        topic_idx = i + 1
        topics.append({
            "name": "topic %s" % topic_idx,
            "desc": "This is description %s" % topic_idx,
            "freq": choice(FREQS),
            "level": choice(LEVELS),
            "host": choice(HOSTS),
            "fields": sample(FIELDS, randint(1, len(FIELDS))),
        })
    return topics

@pytest.fixture()
def topic_info():
    topics = _get_topic_infos(length=1)
    return topics[0]

@pytest.fixture()
def topic_infos(request):
    length = 1
    if hasattr(request, 'param'):
        length = request.param
    return _get_topic_infos(length)

# event_basic_info
def _get_event_basic_infos(length=1):
    event_basics = []
    for _ in range(length):
        random_date = datetime.now() + timedelta(days=randint(1, 365))
        random_clock = randint(0, 21)
        event_basics.append({
            "topic_sn": None,
            "date": random_date.strftime("%Y-%m-%d"),
            "start_time": "%02d:00" % random_clock,
            "end_time": "%02d:00" % (random_clock + 2)
        })
    return event_basics

@pytest.fixture()
def event_basic_info(request):
    event_basics = _get_event_basic_infos(length=1)
    return event_basics[0]

@pytest.fixture()
def event_basic_infos(request):
    length = 1
    if hasattr(request, 'param'):
        length = request.param
    return _get_event_basic_infos(length)

# place_info
def _get_place_infos(length):
    places = []
    for i in range(length):
        place_idx = i + 1
        places.append({
            "name": "place %s" % place_idx,
            "addr": "地址 %s" % place_idx,
            "map": "https://www.google.com/maps/place/place %s" % place_idx
        })
    return places

@pytest.fixture()
def place_info():
    places = _get_place_infos(length=1)
    return places[0]

@pytest.fixture()
def place_infos(request):
    length = 1
    if hasattr(request, 'param'):
        length = request.param
    return _get_place_infos(length)

# apply_info
def _get_apply_infos(length):
    # note: this version only return 1 or 2 apply_infos
    applies = [{
        "host": "婦女館",
        "channel": 1,
        "type": "all",
        "start_time": "2019-11-23 08:00",
        "end_time": "2019-12-01 23:00",
        "price": u"一般人400元，學生200元",
        "limit": u"限女",
        "url": "https://...",
        "qualification": "https://..."
    }]

    if length == 1:
        return applies

    applies.append({
        "host": "American Innovation Center 美國創新中心",
        "channel": 0,
        "type": "one",
        "start_time": "2019-10-23 08:00",
        "end_time": "2019-12-01 23:00",
        "price": u"一般人100元，學生50元",
        "limit": u"限女",
        "url": "https://...",
        "qualification": "https://..."
    })
    return applies

@pytest.fixture()
def apply_info():
    applies = _get_apply_infos(length=1)
    return applies[0]

@pytest.fixture()
def apply_infos(request):
    length = 1
    if hasattr(request, 'param'):
        length = request.param
    return _get_apply_infos(length)