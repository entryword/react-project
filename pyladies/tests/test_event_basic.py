# coding=UTF-8

import unittest

from sqlalchemy.exc import IntegrityError

from app import create_app
from app.exceptions import PyLadiesException
from app.exceptions import EVENTBASIC_NOT_EXIST
from app.sqldb import DBWrapper


class EventBasicTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.db.create_all()

    def tearDown(self):
        self.app.db.session.remove()
        self.app.db.drop_all()
        self.app_context.pop()

    def test_create_event_basic_without_place(self):
        topic_info = {
            "name": "topic 1",
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
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn

            # test
            manager.create_event_basic(event_basic_info, autocommit=True)

            # assertion
            event_basic_sn = topic.event_basics[0].sn
            event_basic = manager.get_event_basic(event_basic_sn)
            self.assertEquals(event_basic.topic.name, topic_info["name"])
            self.assertEquals(event_basic.place, None)
            self.assertEquals(event_basic.date, event_basic_info["date"])
            self.assertEquals(event_basic.start_time, event_basic_info["start_time"])
            self.assertEquals(event_basic.end_time, event_basic_info["end_time"])

    def test_create_event_basic_with_place(self):
        topic_info = {
            "name": "topic 1",
            "desc": "This is description",
            "freq": 0,
            "level": 1,
            "host": 0,
            "fields": [0, 1, 2]
        }
        place_info = {
            "name": "place 1",
            "addr": "台北市信義區光復南路133號",
            "map": "http://abc.com/map.html"
        }
        event_basic_info = {
            "topic_sn": None,
            "date": "2017-01-01",
            "start_time": "14:00",
            "end_time": "16:00"
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            manager.create_place(place_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            place = manager.get_place_by_name(place_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            event_basic_info["place_sn"] = place.sn

            # test
            manager.create_event_basic(event_basic_info, autocommit=True)

            # assertion
            event_basic_sn = topic.event_basics[0].sn
            event_basic = manager.get_event_basic(event_basic_sn)
            self.assertEquals(event_basic.topic.name, topic_info["name"])
            self.assertEquals(event_basic.place.name, place_info["name"])
            self.assertEquals(event_basic.place.map, place_info["map"])
            self.assertEquals(event_basic.date, event_basic_info["date"])
            self.assertEquals(event_basic.start_time, event_basic_info["start_time"])
            self.assertEquals(event_basic.end_time, event_basic_info["end_time"])

    def test_create_event_basic_with_not_existed_topic(self):
        event_basic_info = {
            "topic_sn": 100,
            "date": "2017-01-01",
            "start_time": "14:00",
            "end_time": "16:00"
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)

            # test & assertion
            with self.assertRaises(IntegrityError) as cm:
                manager.create_event_basic(event_basic_info, autocommit=True)
            error_msg = str(cm.exception)
            self.assertIn("foreign key", error_msg.lower())

    def test_update_event_basic(self):
        topic_info = {
            "name": "topic 1",
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
        new_event_basic_info = {
            "topic_sn": None,
            "date": "2017-02-01",
            "start_time": "10:00",
            "end_time": "12:00"
        }
        place_info = {
            "name": "place 1",
            "addr": "台北市信義區光復南路133號",
            "map": "http://abc.com/map.html"
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            new_event_basic_info["topic_sn"] = topic.sn
            manager.create_place(place_info, autocommit=True)
            place = manager.get_place_by_name(place_info["name"])
            new_event_basic_info["place_sn"] = place.sn
            manager.create_event_basic(event_basic_info, autocommit=True)

            # test
            manager.update_event_basic(1, new_event_basic_info, autocommit=True)

            # assertion
            event_basic_sn = topic.event_basics[0].sn
            event_basic = manager.get_event_basic(event_basic_sn)
            self.assertEquals(event_basic.date, new_event_basic_info["date"])
            self.assertEquals(event_basic.start_time, new_event_basic_info["start_time"])
            self.assertEquals(event_basic.end_time, new_event_basic_info["end_time"])
            self.assertEquals(event_basic.place.name, place_info["name"])
            self.assertEquals(event_basic.place.map, place_info["map"])

    def test_change_place(self):
        topic_info = {
            "name": "topic 1",
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
        place_info = {
            "name": "place 1",
            "addr": "台北市信義區光復南路133號",
            "map": "http://abc.com/map.html"
        }
        new_event_basic_info = {
            "topic_sn": None,
            "date": "2017-01-01",
            "start_time": "14:00",
            "end_time": "16:00"
        }
        new_place_info = {
            "name": "place 2",
            "addr": "台北市萬華區艋舺大道101號",
            "map": "http://abc.p2.com/map.html"
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            new_event_basic_info["topic_sn"] = topic.sn
            manager.create_place(place_info, autocommit=True)
            place = manager.get_place_by_name(place_info["name"])
            event_basic_info["place_sn"] = place.sn
            manager.create_place(new_place_info, autocommit=True)
            new_place = manager.get_place_by_name(new_place_info["name"])
            new_event_basic_info["place_sn"] = new_place.sn
            manager.create_event_basic(event_basic_info, autocommit=True)

            # test
            manager.update_event_basic(1, new_event_basic_info, autocommit=True)

            # assertion 1
            event_basic_sn = topic.event_basics[0].sn
            event_basic = manager.get_event_basic(event_basic_sn)
            self.assertEquals(event_basic.date, new_event_basic_info["date"])
            self.assertEquals(event_basic.start_time, new_event_basic_info["start_time"])
            self.assertEquals(event_basic.end_time, new_event_basic_info["end_time"])
            self.assertEquals(event_basic.place.name, new_place_info["name"])
            self.assertEquals(event_basic.place.map, new_place_info["map"])

            # assertion 2
            row_count = db_sess.execute("SELECT COUNT(*) FROM place").scalar()
            self.assertEquals(row_count, 2)

    def test_delete_event_basic(self):
        topic_info = {
            "name": "topic 1",
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
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_basic_sn = topic.event_basics[0].sn

            # test
            manager.delete_event_basic(event_basic_sn, autocommit=True)

            # assertion
            with self.assertRaises(PyLadiesException) as cm:
                manager.get_event_basic(event_basic_sn)
            self.assertEquals(cm.exception, EVENTBASIC_NOT_EXIST)

    def test_delete_topic(self):
        topic_info = {
            "name": "topic 1",
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
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            event_basic_info["topic_sn"] = 1
            manager.create_event_basic(event_basic_info, autocommit=True)

            # test
            manager.delete_topic(1, autocommit=True)

            # assertion
            with self.assertRaises(PyLadiesException) as cm:
                manager.get_event_basic(1)
            self.assertEquals(cm.exception, EVENTBASIC_NOT_EXIST)

    def test_get_event_basic_by_sn(self):
        topic_info = {
            "name": "topic 1",
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
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_basic_sn = topic.event_basics[0].sn

            # test & assertion 1
            event_basic = manager.get_event_basic(event_basic_sn)
            self.assertEquals(event_basic.date, event_basic_info["date"])

            # test & assertion 2
            with self.assertRaises(PyLadiesException) as cm:
                not_exist_event_basic_sn = event_basic_sn + 1
                manager.get_event_basic(not_exist_event_basic_sn)
            self.assertEquals(cm.exception, EVENTBASIC_NOT_EXIST)

    def test_get_event_basics_by_topic(self):
        topic_info = {
            "name": "topic 1",
            "desc": "This is description",
            "freq": 0,
            "level": 1,
            "host": 0,
            "fields": [0, 1, 2]
        }
        event_basic_info_1 = {
            "topic_sn": None,
            "date": "2017-01-01",
            "start_time": "14:00",
            "end_time": "16:00"
        }
        event_basic_info_2 = {
            "topic_sn": None,
            "date": "2017-01-08",
            "start_time": "14:00",
            "end_time": "16:00"
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info_1["topic_sn"] = topic.sn
            event_basic_info_2["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info_1, autocommit=True)
            manager.create_event_basic(event_basic_info_2, autocommit=True)

            # test & assertion
            self.assertEquals(len(topic.event_basics), 2)
            self.assertEquals(topic.event_basics[0].date, event_basic_info_1["date"])
            self.assertEquals(topic.event_basics[1].date, event_basic_info_2["date"])
