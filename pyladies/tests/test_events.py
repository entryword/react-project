# coding=UTF-8

import unittest

from app import create_app
from app.sqldb import DBWrapper


class EventsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.db.create_all()

    def tearDown(self):
        self.app.db.session.remove()
        self.app.db.drop_all()
        self.app_context.pop()

    def test_search_events_with_keywords(self):
        topics = [
            {
                "name": "topic 1",
                "desc": "this is topic 1",
                "freq": 0,
                "level": 0,
                "host": 0,
                "fields": [0],
            },
            {
                "name": "topic 2",
                "desc": "this is topic 2",
                "freq": 0,
                "level": 0,
                "host": 0,
                "fields": [0],
            },
        ]
        place_info = {
            "name": "國立台灣大學",
            "addr": "台北市大安區羅斯福路四段1號",
            "map": "",
        }
        event_basics = [
            {
                "topic_sn": 1,
                "date": "2019-01-07",
                "start_time": "10:00",
                "end_time": "12:00",
                "place_sn": 1,
            },
            {
                "topic_sn": 1,
                "date": "2019-02-17",
                "start_time": "17:30",
                "end_time": "20:00",
                "place_sn": None,
            },
        ]
        event_infos = [
            {
                "event_basic_sn": 1,
                "title": "event 1",
                "desc": "this is event 1",
                "fields": [0, 1],
            },
            {
                "event_basic_sn": 2,
                "title": "event 2",
                "desc": "this is event 2",
                "fields": [0],
            },
        ]

        # preparation
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            for topic in topics:
                manager.create_topic(topic, autocommit=True)
            manager.create_place(place_info, autocommit=True)
            for event_basic in event_basics:
                manager.create_event_basic(event_basic, autocommit=True)
            for event_info in event_infos:
                manager.create_event_info(event_info, autocommit=True)

            # test
            date = ''

            # test keyword empty
            keyword = ''
            event_basics = manager.search_event_basics(keyword, date)
            self.assertEquals(len(event_basics), 2)

            # test keyword event
            keyword = 'event'
            event_basics = manager.search_event_basics(keyword, date)
            self.assertEquals(len(event_basics), 2)

            # test keyword event 1
            keyword = 'event 1'
            event_basics = manager.search_event_basics(keyword, date)
            self.assertEquals(len(event_basics), 1)
            self.assertEquals(event_basics[0].event_info.title, "event 1")

            # test keyword topic
            keyword = 'topic'
            event_basics = manager.search_event_basics(keyword, date)
            self.assertEquals(len(event_basics), 2)

            # test keyword topic 1
            keyword = 'topic 1'
            event_basics = manager.search_event_basics(keyword, date)
            self.assertEquals(len(event_basics), 2)

            # test keyword topic 2
            keyword = 'topic 2'
            event_basics = manager.search_event_basics(keyword, date)
            self.assertEquals(len(event_basics), 0)

            # test keyword abc
            keyword = 'abc'
            event_basics = manager.search_event_basics(keyword, date)
            self.assertEquals(len(event_basics), 0)

    def test_search_events_with_date_and_keyword(self):
        topics = [
            {
                "name": "topic 1",
                "desc": "this is topic 1",
                "freq": 0,
                "level": 0,
                "host": 0,
                "fields": [0],
            },
            {
                "name": "topic 2",
                "desc": "this is topic 2",
                "freq": 0,
                "level": 0,
                "host": 0,
                "fields": [0],
            },
        ]
        place_info = {
            "name": "國立台灣大學",
            "addr": "台北市大安區羅斯福路四段1號",
            "map": "",
        }
        event_basics = [
            {
                "topic_sn": 1,
                "date": "2019-01-07",
                "start_time": "10:00",
                "end_time": "12:00",
                "place_sn": 1,
            },
            {
                "topic_sn": 1,
                "date": "2019-02-03",
                "start_time": "17:30",
                "end_time": "20:00",
                "place_sn": None,
            },
            {
                "topic_sn": 2,
                "date": "2019-02-17",
                "start_time": "17:30",
                "end_time": "20:00",
                "place_sn": None,
            },
        ]
        event_infos = [
            {
                "event_basic_sn": 1,
                "title": "event 1",
                "desc": "this is event 1",
                "fields": [0, 1],
            },
            {
                "event_basic_sn": 2,
                "title": "event 2",
                "desc": "this is event 2",
                "fields": [0],
            },
            {
                "event_basic_sn": 3,
                "title": "event 3",
                "desc": "this is event 3",
                "fields": [0],
            },
        ]

        # preparation
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            for topic in topics:
                manager.create_topic(topic, autocommit=True)
            manager.create_place(place_info, autocommit=True)
            for event_basic in event_basics:
                manager.create_event_basic(event_basic, autocommit=True)
            for event_info in event_infos:
                manager.create_event_info(event_info, autocommit=True)

            # test
            keyword = ''

            # test date empty
            date = ''
            event_basics = manager.search_event_basics(keyword, date)
            self.assertEquals(len(event_basics), 3)

            # test date 2019-01
            date = '2019-01'
            event_basics = manager.search_event_basics(keyword, date)
            self.assertEquals(len(event_basics), 1)
            self.assertEquals(event_basics[0].event_info.title, "event 1")

            # test date 2019-02
            date = '2019-02'
            event_basics = manager.search_event_basics(keyword, date)
            self.assertEquals(len(event_basics), 2)
            self.assertEquals(event_basics[0].event_info.title, "event 2")
            self.assertEquals(event_basics[1].event_info.title, "event 3")

            # test date 2019-02 and keyword event 2
            keyword = 'event 2'
            date = '2019-02'
            event_basics = manager.search_event_basics(keyword, date)
            self.assertEquals(len(event_basics), 1)
            self.assertEquals(event_basics[0].event_info.title, "event 2")

            # test date 2019-02 and keyword event 1
            keyword = 'event 1'
            date = '2019-02'
            event_basics = manager.search_event_basics(keyword, date)
            self.assertEquals(len(event_basics), 0)
            