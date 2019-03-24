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

    def test_search_events_with_date(self):
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

    def test_search_events_with_keywords_and_date(self):
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

    def test_get_events_from_distinct_topics(self):
        topic_info_1 = {
            "name": "topic 1",
            "desc": "This is description",
            "freq": 0,
            "level": 1,
            "host": 0,
            "fields": [0, 1, 2]
        }
        topic_info_2 = {
            "name": "topic 2",
            "desc": "This is description",
            "freq": 0,
            "level": 2,
            "host": 0,
            "fields": [0, 1, 2]
        }
        topic_info_3 = {
            "name": "topic 3",
            "desc": "This is description",
            "freq": 0,
            "level": 3,
            "host": 0,
            "fields": [0, 1, 2]
        }
        topic_info_4 = {
            "name": "topic 4",
            "desc": "This is description",
            "freq": 0,
            "level": 4,
            "host": 0,
            "fields": [0, 1, 2]
        }
        event_basic_info_1 = {
            "topic_sn": None,
            "date": "2020-01-01",
            "start_time": "14:00",
            "end_time": "16:00"
        }
        event_basic_info_2 = {
            "topic_sn": None,
            "date": "2020-03-08",
            "start_time": "14:00",
            "end_time": "16:00"
        }
        event_basic_info_3 = {
            "topic_sn": None,
            "date": "2020-05-25",
            "start_time": "14:00",
            "end_time": "16:00"
        }
        event_basic_info_4 = {
            "topic_sn": None,
            "date": "2020-10-30",
            "start_time": "14:00",
            "end_time": "16:00"
        }

        event_info_1 = {
            "event_basic_sn": None,
            "title": "Flask class 1",
            "desc": "This is description of class 1",
            "fields": [0, 1]
        }
        event_info_2 = {
            "event_basic_sn": None,
            "title": "Flask class 2",
            "desc": "This is description of class 2",
            "fields": [0, 1]
        }
        event_info_3 = {
            "event_basic_sn": None,
            "title": "Flask class 3",
            "desc": "This is description of class 3",
            "fields": [0, 1]
        }
        event_info_4 = {
            "event_basic_sn": None,
            "title": "Flask class 4",
            "desc": "This is description of class 4",
            "fields": [0, 1]
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)

            topic_1 = manager.create_topic(topic_info_1, autocommit=True)
            topic_2 = manager.create_topic(topic_info_2, autocommit=True)
            topic_3 = manager.create_topic(topic_info_3, autocommit=True)
            topic_4 = manager.create_topic(topic_info_4, autocommit=True)

            event_basic_info_1["topic_sn"] = topic_1
            event_basic_info_2["topic_sn"] = topic_2
            event_basic_info_3["topic_sn"] = topic_3
            event_basic_info_4["topic_sn"] = topic_4

            event_basic_1_id = manager.create_event_basic(event_basic_info_1, autocommit=True)
            event_basic_2_id = manager.create_event_basic(event_basic_info_2, autocommit=True)
            event_basic_3_id = manager.create_event_basic(event_basic_info_3, autocommit=True)
            event_basic_4_id = manager.create_event_basic(event_basic_info_4, autocommit=True)

            event_info_1["event_basic_sn"] = event_basic_1_id
            event_info_2["event_basic_sn"] = event_basic_2_id
            event_info_3["event_basic_sn"] = event_basic_3_id
            event_info_4["event_basic_sn"] = event_basic_4_id

            manager.create_event_info(event_info_1, autocommit=True)
            manager.create_event_info(event_info_2, autocommit=True)
            manager.create_event_info(event_info_3, autocommit=True)
            manager.create_event_info(event_info_4, autocommit=True)

        # test ＆ assertion
        rv = self.test_client.get("/v1.0/api/events_from_distinct_topics")

        self.assertEquals(rv.status_code, 200)
        self.assertEquals(rv.json["info"]["code"], 0)
        ans_1 = {
            "topic_info": {
                "name": topic_info_1["name"],
                "id": topic_1,
            },
            "event_info": {
                "title": event_info_1["title"],
                "level": topic_info_1["level"],
                "date": event_basic_info_1["date"],
                "start_time": event_basic_info_1["start_time"],
                "end_time": event_basic_info_1["end_time"],
                "event_basic_id": event_basic_1_id
            }
        }
        ans_2 = {
            "topic_info": {
                "name": topic_info_2["name"],
                "id": topic_2,
            },
            "event_info": {
                "title": event_info_2["title"],
                "level": topic_info_2["level"],
                "date": event_basic_info_2["date"],
                "start_time": event_basic_info_2["start_time"],
                "end_time": event_basic_info_2["end_time"],
                "event_basic_id": event_basic_2_id
            }
        }
        ans_3 = {
            "topic_info": {
                "name": topic_info_3["name"],
                "id": topic_3,
            },
            "event_info": {
                "title": event_info_3["title"],
                "level": topic_info_3["level"],
                "date": event_basic_info_3["date"],
                "start_time": event_basic_info_3["start_time"],
                "end_time": event_basic_info_3["end_time"],
                "event_basic_id": event_basic_3_id
            }
        }
        ans_4 = {
            "topic_info": {
                "name": topic_info_4["name"],
                "id": topic_4,
            },
            "event_info": {
                "title": event_info_4["title"],
                "level": topic_info_4["level"],
                "date": event_basic_info_4["date"],
                "start_time": event_basic_info_4["start_time"],
                "end_time": event_basic_info_4["end_time"],
                "event_basic_id": event_basic_4_id
            }
        }
        self.assertEquals(rv.json["data"]["events"][0], ans_1)
        self.assertEquals(rv.json["data"]["events"][1], ans_2)
        self.assertEquals(rv.json["data"]["events"][2], ans_3)
        self.assertEquals(rv.json["data"]["events"][3], ans_4)
