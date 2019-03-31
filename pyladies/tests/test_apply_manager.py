# coding=UTF-8

import unittest

import jsonschema
from pytest import raises

from app import create_app
from app.managers.apply import Manager as ApplyManager
from app.sqldb import DBWrapper


class InvalidInputTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.db.create_all()

    def tearDown(self):
        self.app.db.session.remove()
        self.app.db.drop_all()
        self.app_context.pop()

    def test_without_host_when_create(self):
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
            # "host": "婦女館",
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

            # test & assertion
            with raises(jsonschema.exceptions.ValidationError):
                ApplyManager.create_event_apply_info(input_event_apply)

    def test_without_type_when_create(self):
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
            # "type": "all",
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

            # test & assertion
            with raises(jsonschema.exceptions.ValidationError):
                ApplyManager.create_event_apply_info(input_event_apply)

    def test_not_specified_datetime_format_when_create(self):
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
            "start_time": "2019/11/23 08:00",
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

            # test & assertion
            with raises(ValueError):
                ApplyManager.create_event_apply_info(input_event_apply)

    def test_invalid_datetime_when_create(self):
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
            "end_time": "2019-13-01 23:00",
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

            # test & assertion
            with raises(ValueError):
                ApplyManager.create_event_apply_info(input_event_apply)
