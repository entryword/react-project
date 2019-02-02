# coding=UTF-8

import unittest


from app import create_app
from app.managers import apply

class EventInfoTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.db.create_all()

    def tearDown(self):
        self.app.db.session.remove()
        self.app.db.drop_all()
        self.app_context.pop()

    def test_create_and_get_event_apply_info(self):
        # prepare
        input_event_apply_info = {
            "event_basic_id": 128,
            "host": "American Innovation Center 美國創新中心",
            "start_time": "2019-11-23 08:00",
            "end_time": "2019-12-01 23:00",
            "apply": [
                {
                    "channel": 0,
                    "type": "one",
                    "price": {
                        "default": 100,
                        "student": 50
                    },
                    "url": "https://...",
                    "qualification": ""
                },
                {
                    "channel": 1,
                    "type": "all",
                    "price": {
                        "default": 400,
                        "student": 200
                    },
                    "url": "https://...",
                    "qualification": "https://..."
                }
            ],
            "limit": {
                "gender": "限女",
                "age": "不限"
            },
            "limit_desc": "須上傳登錄成功截圖"
        }

        # test
        manager = apply.Manager()
        manager.create_event_apply_info(input_event_apply_info)
        result_event_apply_info = \
            manager.get_event_apply_info(input_event_apply_info["event_basic_id"])
        # assertion
        self.assertEquals(result_event_apply_info, input_event_apply_info)
