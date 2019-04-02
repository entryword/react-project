import pytest


def get_topic_info():
    return {
        "name": "Flask",
        "desc": "This is description",
        "freq": 0,
        "level": 1,
        "host": 0,
        "fields": [0, 1, 2]
    }


def get_event_basic(topic_sn):
    return {
        "topic_sn": topic_sn,
        "date": "2017-01-01",
        "start_time": "14:00",
        "end_time": "16:00"
    }


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
        for topic_sn in range(topic_info_number):
            test_data = {
                'topic_info': get_topic_info(),
                'event_list': []
            }
            manager.create_topic(test_data['topic_info'], autocommit=True)
            topic = manager.get_topic_by_name(test_data['topic_info']["name"])
            for event_basic_sn in range(event_basic_number):
                event = {
                    'event_basic': get_event_basic(topic.sn),
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
