# coding=UTF-8

import unittest

from app import create_app
from app.exceptions import PyLadiesException
from app.exceptions import APPLY_NOT_EXIST
from app.sqldb import DBWrapper


class EventApplyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.db.create_all()

    def tearDown(self):
        self.app.db.session.remove()
        self.app.db.drop_all()
        self.app_context.pop()

    def test_create_event_apply(self):
        topic_info = {
            "name": "Flask",
            "desc": "This is description",
            "freq": 0,
            "level": 1,
            "host": 0,
            "fields": [0, 1, 2]
        }
        event_basic_info = {
            "topic_sn": None,
            "date": "2017-01-01",
            "start_time": "14:00",
            "end_time": "16:00"
        }

        apply_info_1 = {
            "host": "婦女館",
            "channel": 1,
            "type": "all",
            "start_time": "2019-11-23 08:00",
            "end_time": "2019-12-01 23:00",
            "price": u"一般人400元，學生200元",
            "limit": u"限女",
            "url": "https://...",
            "qualification": "https://..."
        }

        apply_info_2 = {
            "host": "American Innovation Center 美國創新中心",
            "channel": 0,
            "type": "one",
            "start_time": "2019-11-23 08:00",
            "end_time": "2019-12-01 23:00",
            "price": u"一般人100元，學生50元",
            "limit": u"限女",
            "url": "https://...",
            "qualification": "https://..."
        }

        input_event_apply = {
            "event_basic_sn": None,
            "apply": [apply_info_1, apply_info_2]
        }

        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_basic = topic.event_basics[0]
            input_event_apply["event_basic_sn"] = event_basic.sn

            # test
            manager.create_event_apply(input_event_apply, autocommit=True)
            event_apply = manager.get_event_apply_by_event_basic_sn(event_basic.sn)

            # test & assertion
            self.assertEquals(event_apply.event_basic_sn, event_basic.sn)
            self.assertEquals(event_apply.apply, input_event_apply["apply"])

    def test_update_event_apply(self):
        topic_info = {
            "name": "Flask",
            "desc": "This is description",
            "freq": 0,
            "level": 1,
            "host": 0,
            "fields": [0, 1, 2]
        }
        event_basic_info = {
            "topic_sn": None,
            "date": "2017-01-01",
            "start_time": "14:00",
            "end_time": "16:00"
        }

        apply_info = {
            "host": "婦女館",
            "channel": 1,
            "type": "all",
            "start_time": "2019-11-23 08:00",
            "end_time": "2019-12-01 23:00",
            "price": u"一般人400元，學生200元",
            "limit": u"限女",
            "url": "https://...",
            "qualification": "https://..."
        }

        apply_info_new = {
            "host": "American Innovation Center 美國創新中心",
            "channel": 0,
            "type": "one",
            "start_time": "2019-10-23 08:00",
            "end_time": "2019-12-01 23:00",
            "price": u"一般人100元，學生50元",
            "limit": u"限女",
            "url": "https://...",
            "qualification": "https://..."
        }

        input_event_apply = {
            "event_basic_sn": None,
            "apply": [apply_info]
        }

        update_info = {
            "apply": [apply_info_new]
        }

        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_basic = topic.event_basics[0]
            input_event_apply["event_basic_sn"] = event_basic.sn

            event_apply_sn = manager.create_event_apply(input_event_apply, autocommit=True)
            event_apply_before = manager.get_event_apply(event_apply_sn)
            event_basic_sn_before = event_apply_before.event_basic_sn
            apply_info_before = event_apply_before.apply

            # test
            manager.update_event_apply(event_apply_sn, update_info, autocommit=True)
            event_apply_after = manager.get_event_apply(event_apply_sn)
            event_basic_sn_after = event_apply_after.event_basic_sn
            apply_info_after = event_apply_after.apply

            # test & assertion
            self.assertEquals(event_basic_sn_before, event_basic_sn_after)
            self.assertEquals(apply_info_before, input_event_apply["apply"])
            self.assertEquals(apply_info_after, update_info["apply"])

    def test_delete_event_apply(self):
        topic_info = {
            "name": "Flask",
            "desc": "This is description",
            "freq": 0,
            "level": 1,
            "host": 0,
            "fields": [0, 1, 2]
        }
        event_basic_info = {
            "topic_sn": None,
            "date": "2017-01-01",
            "start_time": "14:00",
            "end_time": "16:00"
        }

        apply_info = {
            "host": "婦女館",
            "channel": 1,
            "type": "all",
            "start_time": "2019-11-23 08:00",
            "end_time": "2019-12-01 23:00",
            "price": u"一般人400元，學生200元",
            "limit": u"限女",
            "url": "https://...",
            "qualification": "https://..."
        }

        input_event_apply = {
            "event_basic_sn": None,
            "apply": [apply_info]
        }

        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_basic = topic.event_basics[0]
            input_event_apply["event_basic_sn"] = event_basic.sn

            event_apply_sn = manager.create_event_apply(input_event_apply, autocommit=True)

            # test
            manager.delete_event_apply(event_apply_sn, autocommit=True)

            # test & assertion
            with self.assertRaises(PyLadiesException) as cm:
                manager.get_event_apply(event_apply_sn)
            self.assertEquals(cm.exception, APPLY_NOT_EXIST)
