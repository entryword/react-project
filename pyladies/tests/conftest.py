import pytest


@pytest.fixture
def make_test_data():
    def _make_test_data(event_basic_info_number, event_apply_number):
        return_data = {
            'topic_info': {
                "name": "Flask",
                "desc": "This is description",
                "freq": 0,
                "level": 1,
                "host": 0,
                "fields": [0, 1, 2]
            },
            'event_basic_info': [],
            'event_apply': []
        }
        for i in range(event_basic_info_number):
            return_data['event_basic_info'].append(
                {
                    "topic_sn": None,
                    "date": "2017-01-01",
                    "start_time": "14:00",
                    "end_time": "16:00"
                }
            )
        apply_info_1 = {
            "host": "婦女館",
            "channel": 1,
            "type": "all",
            "price": {
                "default": 400,
                "student": 200
            },
            "url": "https://...",
            "qualification": "https://..."
        }

        apply_info_2 = {
            "host": "American Innovation Center 美國創新中心",
            "channel": 0,
            "type": "one",
            "price": {
                "default": 100,
                "student": 50
            },
            "url": "https://...",
            "qualification": "https://..."
        }
        for i in range(event_apply_number):
            return_data['event_apply'].append(
                {
                    "event_basic_sn": None,
                    "apply": [apply_info_1, apply_info_2],
                    "start_time": "2019-11-23 08:00",
                    "end_time": "2019-12-01 23:00",
                    "limit": {
                        "gender": "限女",
                        "age": "不限"
                    },
                    "limit_desc": "須上傳登錄成功截圖"
                }
            )
        return return_data

    return _make_test_data
