from random import randint
import pytest

# topc_info
def _get_topic_infos(length=1):
    topics = []
    for i in range(length):
        topic_idx = i + 1
        topics.append({
            "name": "topic %s" % topic_idx,
            "desc": "This is description %s" % topic_idx,
            "freq": randint(0, 3),
            "level": randint(0, 3),
            "host": randint(0, 3),
            "fields": [i + 1 for i in range(randint(1, 4))]
        })
    return topics

@pytest.fixture()
def topic_info():
    topic_infos = _get_topic_infos(length=1)
    return topic_infos[0]

@pytest.fixture()
def topic_infos(request):
    length = 1
    if hasattr(request, 'param'):
        length = request.param
    return _get_topic_infos(length)

# event_basic_info
def _get_event_basic_info(topic_sn=None):
    return {
        "topic_sn": topic_sn,
        "date": "2017-01-01",
        "start_time": "14:00",
        "end_time": "16:00"
    }

@pytest.fixture()
def event_basic_info(request):
    topic_sn = None
    if hasattr(request, 'param'):
        topic_sn = request.param
    return _get_event_basic_info(topic_sn)

# place_info
@pytest.fixture()
def place_info():
    return {
        "name": "place 1",
        "addr": "台北市信義區光復南路133號",
        "map": "http://abc.com/map.html"
    }

# apply_info
def _get_apply_infos(length):
    # note: this version only return 1 or 2 apply_infos
    apply_infos = [{
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
        return apply_infos

    apply_infos.append({
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
    return apply_infos

@pytest.fixture()
def apply_info():
    apply_infos = _get_apply_infos(length=1)
    return apply_infos[0]

@pytest.fixture()
def apply_infos(request):
    length = 1
    if hasattr(request, 'param'):
        length = request.param
    return _get_apply_infos(length)


def get_event_info(event_basic_sn):
    return {
        "event_basic_sn": event_basic_sn,
        "title": "Flask class 1",
        "desc": "This is description of class 1",
        "fields": [0, 1]
    }

def get_apply_info(channel):
    return {
        "host": "婦女館",
        "channel": channel,
        "type": "all",
        "price": {
            "default": 400,
            "student": 200
        },
        "url": "https://...",
        "qualification": "https://..."
    }


def get_apply_info_list(number):
    return [get_apply_info(channel) for channel in range(1, number+1)]


def get_event_apply(event_basic_sn, channel_number):
    return {
        "event_basic_sn": event_basic_sn,
        "apply": get_apply_info_list(channel_number),
        "start_time": "2019-11-23 08:00",
        "end_time": "2019-12-01 23:00",
        "limit": {
            "gender": "限女",
            "age": "不限"
        },
        "limit_desc": "須上傳登錄成功截圖"
    }


@pytest.fixture
def make_test_data():
    def _make_test_data(manager, topic_info_number,
                        event_basic_number, event_info_number, event_apply_number, channel_number):
        test_data_list = []
        for _ in range(topic_info_number):
            test_data = {
                'topic_info': _get_topic_infos(length=1),
                'event_list': []
            }
            manager.create_topic(test_data['topic_info'], autocommit=True)
            topic = manager.get_topic_by_name(test_data['topic_info']["name"])
            for _ in range(event_basic_number):
                event = {
                    'event_basic': _get_event_basic_info(topic.sn),
                    'event_info': [],
                    'event_apply': []
                }
                manager.create_event_basic(event['event_basic'], autocommit=True)
                event_basic = topic.event_basics[0]
                for i in range(event_info_number):
                    event_info = get_event_info(event_basic.sn)
                    event['event_info'].append(event_info)
                    manager.create_event_info(event_info, autocommit=True)

                for i in range(event_apply_number):
                    event_apply = get_event_apply(event_basic.sn, channel_number[i])
                    event['event_apply'].append(event_apply)
                    manager.create_event_apply(event_apply, autocommit=True)

                test_data['event_list'].append(event)

            test_data_list.append(test_data)

        return test_data_list

    return _make_test_data
