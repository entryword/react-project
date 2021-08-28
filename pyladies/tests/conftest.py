from datetime import datetime, timedelta
from random import choice, randint, sample, getrandbits
import pytest
from app import constant

FREQS = list(constant.FREQ_1_0.keys())
LEVELS = list(constant.LEVEL_1_0.keys())
HOSTS = list(constant.HOST_1_0.keys())
FIELDS = list(constant.FIELD_1_0.keys())
TYPE = list(constant.TYPE_1_0.keys())
CHANNEL = list(constant.CHANNEL_1_0.keys())
APPLY_LIMIT_1_0 = {
    "girl": "限女",
    "family": "親子",
    "no": "不限"
}
APPLY_LIMIT = list(APPLY_LIMIT_1_0.keys())
HOST_PLACE_1_0 = {
    0: "美國創新中心AIC",
    1: "臺北市婦女館",
    2: "天瓏書局CodingSpace TLCS",
    3: "松菸133號共創合作社"
}
HOST_PLACES = list(HOST_PLACE_1_0.keys())


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
            "topic_id": None,
            "date": random_date.strftime("%Y-%m-%d"),
            "start_time": "%02d:00" % random_clock,
            "end_time": "%02d:00" % (random_clock + 2)
        })
    return event_basics


@pytest.fixture()
def event_basic_info():
    event_basics = _get_event_basic_infos(length=1)
    return event_basics[0]


@pytest.fixture()
def event_basic_infos(request):
    length = 1
    if hasattr(request, 'param'):
        length = request.param
    return _get_event_basic_infos(length)


# event_info
def _get_event_infos(length=1):
    events = []
    for i in range(length):
        event_idx = i + 1
        events.append({
            "event_basic_id": None,
            "title": "event %s" % event_idx,
            "desc": "this is event %s" % event_idx,
            "fields": sample(FIELDS, randint(1, len(FIELDS))),
        })
    return events


@pytest.fixture()
def event_info():
    events = _get_event_infos(length=1)
    return events[0]


@pytest.fixture()
def event_infos(request):
    length = 1
    if hasattr(request, 'param'):
        length = request.param
    return _get_event_infos(length)


# speaker_info
def _get_speaker_infos(length=1, speaker_type='speaker'):
    speakers = []
    for i in range(length):
        speaker_idx = i + 1
        speakers.append({
            "name": "%s %s" % (speaker_type, speaker_idx),
            "photo": "https://pyladies.marsw.tw/img/speaker_%s_photo.png" % speaker_idx,
            "title": "%s title %s" % (speaker_type, speaker_idx),
            "major_related": bool(getrandbits(1)),
            "intro": "intro %s" % speaker_idx,
            "fields": sample(FIELDS, randint(1, len(FIELDS))),
            "links": _get_link_infos(randint(0, 3))
        })
    return speakers


def _get_link_infos(length=1):
    links = []
    for i in range(length):
        link_idx = i + 1
        links.append({
            "type": "link type %s" % link_idx,
            "url": "url %s" % link_idx
        })
    return links


@pytest.fixture()
def speaker_info():
    speakers = _get_speaker_infos(length=1, speaker_type='speaker')
    return speakers[0]


@pytest.fixture()
def speaker_infos(request):
    length = 1
    if hasattr(request, 'param'):
        length = request.param
    return _get_speaker_infos(length, speaker_type='speaker')


@pytest.fixture()
def assistant_info():
    speakers = _get_speaker_infos(length=1, speaker_type='assistant')
    return speakers[0]


@pytest.fixture()
def assistant_infos(request):
    length = 1
    if hasattr(request, 'param'):
        length = request.param
    return _get_speaker_infos(length, speaker_type='assistant')


# slide_resource
def _get_slide_resources(length=1):
    slides = []
    for i in range(length):
        slide_idx = i + 1
        slide_resource_type = choice(["slide", "resource"])
        slides.append({
            "type": slide_resource_type,
            "title": "%s title %s" % (slide_resource_type, slide_idx),
            "url": "http://tw.pyladies.com/slides/%s" % slide_idx,
        })
    return slides


@pytest.fixture()
def slide_resource():
    slides = _get_slide_resources(length=1)
    return slides[0]


@pytest.fixture()
def slide_resources(request):
    length = 1
    if hasattr(request, 'param'):
        length = request.param
    return _get_slide_resources(length)


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
    applies = []
    for _ in range(length):
        random_clock = randint(0, 21)
        applies.append({
            "host": choice(HOST_PLACES),
            "channel": choice(CHANNEL),
            "type": choice(TYPE),
            "start_time": "%02d:00" % random_clock,
            "end_time": "%02d:00" % (random_clock + 2),
            "price": u"一般150元，學生50元",
            "limit": choice(APPLY_LIMIT),
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


# member_info
def _get_member_info(idx):
    return {
        'name': 'Member%s' % idx,
        'mail': '%s@pyladies.tw' % idx,
        'is_student': True if idx % 3 == 0 else False if idx % 3 == 1 else None,
        'title': None if idx % 3 == 2 else 'title %s' % idx,
        'fields': [] if idx % 3 == 2 else sample(FIELDS, randint(1, len(FIELDS)))
    }


@pytest.fixture()
def member_info():
    return _get_member_info(1)


@pytest.fixture()
def member_infos(request):
    count = getattr(request, 'param', 1)
    return [_get_member_info(i + 1) for i in range(count)]
