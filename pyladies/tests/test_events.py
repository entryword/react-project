# coding=UTF-8
from datetime import datetime, timedelta
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
            self.assertEqual(len(event_basics), 2)

            # test keyword event
            keyword = 'event'
            event_basics = manager.search_event_basics(keyword, date)
            self.assertEqual(len(event_basics), 2)

            # test keyword event 1
            keyword = 'event 1'
            event_basics = manager.search_event_basics(keyword, date)
            self.assertEqual(len(event_basics), 1)
            self.assertEqual(event_basics[0].event_info.title, "event 1")

            # test keyword topic
            keyword = 'topic'
            event_basics = manager.search_event_basics(keyword, date)
            self.assertEqual(len(event_basics), 2)

            # test keyword topic 1
            keyword = 'topic 1'
            event_basics = manager.search_event_basics(keyword, date)
            self.assertEqual(len(event_basics), 2)

            # test keyword topic 2
            keyword = 'topic 2'
            event_basics = manager.search_event_basics(keyword, date)
            self.assertEqual(len(event_basics), 0)

            # test keyword abc
            keyword = 'abc'
            event_basics = manager.search_event_basics(keyword, date)
            self.assertEqual(len(event_basics), 0)

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
            self.assertEqual(len(event_basics), 3)

            # test date 2019-01
            date = '2019-01'
            event_basics = manager.search_event_basics(keyword, date)
            self.assertEqual(len(event_basics), 1)
            self.assertEqual(event_basics[0].event_info.title, "event 1")

            # test date 2019-02
            date = '2019-02'
            event_basics = manager.search_event_basics(keyword, date)
            self.assertEqual(len(event_basics), 2)
            self.assertEqual(event_basics[0].event_info.title, "event 2")
            self.assertEqual(event_basics[1].event_info.title, "event 3")

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
            self.assertEqual(len(event_basics), 1)
            self.assertEqual(event_basics[0].event_info.title, "event 2")

            # test date 2019-02 and keyword event 1
            keyword = 'event 1'
            date = '2019-02'
            event_basics = manager.search_event_basics(keyword, date)
            self.assertEqual(len(event_basics), 0)

    def test_get_no_event_from_one_topic_because_of_no_event_basic(self):
        topic_info = {
            "name": "topic 1",
            "desc": "This is description",
            "freq": 0,
            "level": 1,
            "host": 0,
            "fields": [0, 1, 2]
        }

        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)

            # test
            test_events_from_distinct_topic = manager.get_events_from_distinct_topics(limit=4)

            # assertion
            self.assertEqual(len(test_events_from_distinct_topic), 0)

    def test_get_no_event_from_one_topic_because_of_no_event_info(self):
        def _get_future_date(interval=1):
            future_time = datetime.utcnow() + timedelta(days=interval, hours=8)
            return future_time.strftime("%Y-%m-%d")

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
            "date": _get_future_date(1),
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

            # test
            test_events_from_distinct_topic = manager.get_events_from_distinct_topics(limit=4)

            # assertion
            self.assertEqual(len(test_events_from_distinct_topic), 0)

    def test_get_no_event_from_one_topic_because_of_past_event(self):
        def _get_past_date(interval=1):
            past_time = datetime.utcnow() + timedelta(days=interval*(-1), hours=8)
            return past_time.strftime("%Y-%m-%d")

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
            "date": _get_past_date(1),
            "start_time": "14:00",
            "end_time": "16:00"
        }

        event_info_info = {
            "event_basic_sn": None,
            "title": "A class 1",
            "desc": "This is description of class 1",
            "fields": [0, 1]
        }

        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)

            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)

            event_info_info["event_basic_sn"] = topic.event_basics[0].sn
            manager.create_event_info(event_info_info, autocommit=True)

            # test
            test_events_from_distinct_topic = manager.get_events_from_distinct_topics(limit=4)

            # assertion
            self.assertEqual(len(test_events_from_distinct_topic), 0)

    def test_get_event_from_one_topic_with_only_one_future_event(self):
        def _get_future_date(interval=1):
            future_time = datetime.utcnow() + timedelta(days=interval, hours=8)
            return future_time.strftime("%Y-%m-%d")

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
            "date": _get_future_date(1),
            "start_time": "14:00",
            "end_time": "16:00"
        }

        event_info_info = {
            "event_basic_sn": None,
            "title": "A class 1",
            "desc": "This is description of class 1",
            "fields": [0, 1]
        }

        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)

            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)

            event_info_info["event_basic_sn"] = topic.event_basics[0].sn
            manager.create_event_info(event_info_info, autocommit=True)

            # test
            test_events_from_distinct_topic = manager.get_events_from_distinct_topics(limit=4)

            # assertion
            self.assertEqual(len(test_events_from_distinct_topic), 1)
            self.assertEqual(test_events_from_distinct_topic[0].date,
                             event_basic_info["date"])

    def test_get_event_from_one_topic_with_multiple_future_events(self):
        def _get_future_date(interval=1):
            future_time = datetime.utcnow() + timedelta(days=interval, hours=8)
            return future_time.strftime("%Y-%m-%d")

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
            "date": _get_future_date(1),
            "start_time": "14:00",
            "end_time": "16:00"
        }
        event_basic_info_2 = {
            "topic_sn": None,
            "date": _get_future_date(2),
            "start_time": "14:00",
            "end_time": "16:00"
        }

        event_info_info_1 = {
            "event_basic_sn": None,
            "title": "A class 1",
            "desc": "This is description of class 1",
            "fields": [0, 1]
        }
        event_info_info_2 = {
            "event_basic_sn": None,
            "title": "B class 1",
            "desc": "This is description of class 1",
            "fields": [0, 1]
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

            event_info_info_1["event_basic_sn"] = topic.event_basics[0].sn
            event_info_info_2["event_basic_sn"] = topic.event_basics[1].sn
            manager.create_event_info(event_info_info_1, autocommit=True)
            manager.create_event_info(event_info_info_2, autocommit=True)

            # test
            test_events_from_distinct_topic = manager.get_events_from_distinct_topics(limit=4)

            # assertion
            self.assertEqual(len(test_events_from_distinct_topic), 1)
            self.assertEqual(test_events_from_distinct_topic[0].date,
                             event_basic_info_1["date"])

    def test_get_events_from_four_distinct_level_topics(self):
        def _get_future_date(interval=1):
            future_time = datetime.utcnow() + timedelta(days=interval, hours=8)
            return future_time.strftime("%Y-%m-%d")

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
            "date": _get_future_date(1),
            "start_time": "14:00",
            "end_time": "16:00"
        }
        event_basic_info_2 = {
            "topic_sn": None,
            "date": _get_future_date(2),
            "start_time": "14:00",
            "end_time": "16:00"
        }
        event_basic_info_3 = {
            "topic_sn": None,
            "date": _get_future_date(3),
            "start_time": "14:00",
            "end_time": "16:00"
        }
        event_basic_info_4 = {
            "topic_sn": None,
            "date": _get_future_date(4),
            "start_time": "14:00",
            "end_time": "16:00"
        }

        event_info_info_1 = {
            "event_basic_sn": None,
            "title": "A class 1",
            "desc": "This is description of class 1",
            "fields": [0, 1]
        }
        event_info_info_2 = {
            "event_basic_sn": None,
            "title": "B class 1",
            "desc": "This is description of class 1",
            "fields": [0, 1]
        }
        event_info_info_3 = {
            "event_basic_sn": None,
            "title": "C class 1",
            "desc": "This is description of class 1",
            "fields": [0, 1]
        }
        event_info_info_4 = {
            "event_basic_sn": None,
            "title": "D class 1",
            "desc": "This is description of class 1",
            "fields": [0, 1]
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info_1, autocommit=True)
            manager.create_topic(topic_info_2, autocommit=True)
            manager.create_topic(topic_info_3, autocommit=True)
            manager.create_topic(topic_info_4, autocommit=True)

            topic_1 = manager.get_topic_by_name(topic_info_1["name"])
            topic_2 = manager.get_topic_by_name(topic_info_2["name"])
            topic_3 = manager.get_topic_by_name(topic_info_3["name"])
            topic_4 = manager.get_topic_by_name(topic_info_4["name"])
            event_basic_info_1["topic_sn"] = topic_1.sn
            event_basic_info_2["topic_sn"] = topic_2.sn
            event_basic_info_3["topic_sn"] = topic_3.sn
            event_basic_info_4["topic_sn"] = topic_4.sn
            manager.create_event_basic(event_basic_info_1, autocommit=True)
            manager.create_event_basic(event_basic_info_2, autocommit=True)
            manager.create_event_basic(event_basic_info_3, autocommit=True)
            manager.create_event_basic(event_basic_info_4, autocommit=True)

            event_info_info_1["event_basic_sn"] = topic_1.event_basics[0].sn
            event_info_info_2["event_basic_sn"] = topic_2.event_basics[0].sn
            event_info_info_3["event_basic_sn"] = topic_3.event_basics[0].sn
            event_info_info_4["event_basic_sn"] = topic_4.event_basics[0].sn
            manager.create_event_info(event_info_info_1, autocommit=True)
            manager.create_event_info(event_info_info_2, autocommit=True)
            manager.create_event_info(event_info_info_3, autocommit=True)
            manager.create_event_info(event_info_info_4, autocommit=True)

            # test
            test_events_from_distinct_topic = manager.get_events_from_distinct_topics(limit=4)

            # assertion
            self.assertEqual(len(test_events_from_distinct_topic), 4)
            self.assertEqual(test_events_from_distinct_topic[0].date,
                             event_basic_info_1["date"])
            self.assertEqual(test_events_from_distinct_topic[1].date,
                             event_basic_info_2["date"])
            self.assertEqual(test_events_from_distinct_topic[2].date,
                             event_basic_info_3["date"])
            self.assertEqual(test_events_from_distinct_topic[3].date,
                             event_basic_info_4["date"])

    def test_get_events_from_five_distinct_level_topics(self):
        def _get_future_date(interval=1):
            future_time = datetime.utcnow() + timedelta(days=interval, hours=8)
            return future_time.strftime("%Y-%m-%d")

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
        topic_info_5 = {
            "name": "topic 5",
            "desc": "This is description",
            "freq": 0,
            "level": 5,
            "host": 0,
            "fields": [0, 1, 2]
        }

        event_basic_info_1 = {
            "topic_sn": None,
            "date": _get_future_date(1),
            "start_time": "14:00",
            "end_time": "16:00"
        }
        event_basic_info_2 = {
            "topic_sn": None,
            "date": _get_future_date(2),
            "start_time": "14:00",
            "end_time": "16:00"
        }
        event_basic_info_3 = {
            "topic_sn": None,
            "date": _get_future_date(3),
            "start_time": "14:00",
            "end_time": "16:00"
        }
        event_basic_info_4 = {
            "topic_sn": None,
            "date": _get_future_date(4),
            "start_time": "14:00",
            "end_time": "16:00"
        }
        event_basic_info_5 = {
            "topic_sn": None,
            "date": _get_future_date(5),
            "start_time": "14:00",
            "end_time": "16:00"
        }

        event_info_info_1 = {
            "event_basic_sn": None,
            "title": "A class 1",
            "desc": "This is description of class 1",
            "fields": [0, 1]
        }
        event_info_info_2 = {
            "event_basic_sn": None,
            "title": "B class 1",
            "desc": "This is description of class 1",
            "fields": [0, 1]
        }
        event_info_info_3 = {
            "event_basic_sn": None,
            "title": "C class 1",
            "desc": "This is description of class 1",
            "fields": [0, 1]
        }
        event_info_info_4 = {
            "event_basic_sn": None,
            "title": "D class 1",
            "desc": "This is description of class 1",
            "fields": [0, 1]
        }
        event_info_info_5 = {
            "event_basic_sn": None,
            "title": "E class 1",
            "desc": "This is description of class 1",
            "fields": [0, 1]
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info_1, autocommit=True)
            manager.create_topic(topic_info_2, autocommit=True)
            manager.create_topic(topic_info_3, autocommit=True)
            manager.create_topic(topic_info_4, autocommit=True)
            manager.create_topic(topic_info_5, autocommit=True)

            topic_1 = manager.get_topic_by_name(topic_info_1["name"])
            topic_2 = manager.get_topic_by_name(topic_info_2["name"])
            topic_3 = manager.get_topic_by_name(topic_info_3["name"])
            topic_4 = manager.get_topic_by_name(topic_info_4["name"])
            topic_5 = manager.get_topic_by_name(topic_info_5["name"])
            event_basic_info_1["topic_sn"] = topic_1.sn
            event_basic_info_2["topic_sn"] = topic_2.sn
            event_basic_info_3["topic_sn"] = topic_3.sn
            event_basic_info_4["topic_sn"] = topic_4.sn
            event_basic_info_5["topic_sn"] = topic_5.sn
            manager.create_event_basic(event_basic_info_1, autocommit=True)
            manager.create_event_basic(event_basic_info_2, autocommit=True)
            manager.create_event_basic(event_basic_info_3, autocommit=True)
            manager.create_event_basic(event_basic_info_4, autocommit=True)
            manager.create_event_basic(event_basic_info_5, autocommit=True)

            event_info_info_1["event_basic_sn"] = topic_1.event_basics[0].sn
            event_info_info_2["event_basic_sn"] = topic_2.event_basics[0].sn
            event_info_info_3["event_basic_sn"] = topic_3.event_basics[0].sn
            event_info_info_4["event_basic_sn"] = topic_4.event_basics[0].sn
            event_info_info_5["event_basic_sn"] = topic_5.event_basics[0].sn
            manager.create_event_info(event_info_info_1, autocommit=True)
            manager.create_event_info(event_info_info_2, autocommit=True)
            manager.create_event_info(event_info_info_3, autocommit=True)
            manager.create_event_info(event_info_info_4, autocommit=True)
            manager.create_event_info(event_info_info_5, autocommit=True)

            # test
            test_events_from_distinct_topic = manager.get_events_from_distinct_topics(limit=4)

            # assertion
            self.assertEqual(len(test_events_from_distinct_topic), 4)
            self.assertEqual(test_events_from_distinct_topic[0].date,
                             event_basic_info_1["date"])
            self.assertEqual(test_events_from_distinct_topic[1].date,
                             event_basic_info_2["date"])
            self.assertEqual(test_events_from_distinct_topic[2].date,
                             event_basic_info_3["date"])
            self.assertEqual(test_events_from_distinct_topic[3].date,
                             event_basic_info_4["date"])

    def test_get_events_from_four_topics_but_two_are_same_level(self):
        def _get_future_date(interval=1):
            future_time = datetime.utcnow() + timedelta(days=interval, hours=8)
            return future_time.strftime("%Y-%m-%d")

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
            "level": 3,
            "host": 0,
            "fields": [0, 1, 2]
        }

        event_basic_info_1 = {
            "topic_sn": None,
            "date": _get_future_date(1),
            "start_time": "14:00",
            "end_time": "16:00"
        }
        event_basic_info_2 = {
            "topic_sn": None,
            "date": _get_future_date(2),
            "start_time": "14:00",
            "end_time": "16:00"
        }
        event_basic_info_3 = {
            "topic_sn": None,
            "date": _get_future_date(3),
            "start_time": "14:00",
            "end_time": "16:00"
        }
        event_basic_info_4 = {
            "topic_sn": None,
            "date": _get_future_date(4),
            "start_time": "14:00",
            "end_time": "16:00"
        }

        event_info_info_1 = {
            "event_basic_sn": None,
            "title": "A class 1",
            "desc": "This is description of class 1",
            "fields": [0, 1]
        }
        event_info_info_2 = {
            "event_basic_sn": None,
            "title": "B class 1",
            "desc": "This is description of class 1",
            "fields": [0, 1]
        }
        event_info_info_3 = {
            "event_basic_sn": None,
            "title": "C class 1",
            "desc": "This is description of class 1",
            "fields": [0, 1]
        }
        event_info_info_4 = {
            "event_basic_sn": None,
            "title": "D class 1",
            "desc": "This is description of class 1",
            "fields": [0, 1]
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info_1, autocommit=True)
            manager.create_topic(topic_info_2, autocommit=True)
            manager.create_topic(topic_info_3, autocommit=True)
            manager.create_topic(topic_info_4, autocommit=True)

            topic_1 = manager.get_topic_by_name(topic_info_1["name"])
            topic_2 = manager.get_topic_by_name(topic_info_2["name"])
            topic_3 = manager.get_topic_by_name(topic_info_3["name"])
            topic_4 = manager.get_topic_by_name(topic_info_4["name"])
            event_basic_info_1["topic_sn"] = topic_1.sn
            event_basic_info_2["topic_sn"] = topic_2.sn
            event_basic_info_3["topic_sn"] = topic_3.sn
            event_basic_info_4["topic_sn"] = topic_4.sn
            manager.create_event_basic(event_basic_info_1, autocommit=True)
            manager.create_event_basic(event_basic_info_2, autocommit=True)
            manager.create_event_basic(event_basic_info_3, autocommit=True)
            manager.create_event_basic(event_basic_info_4, autocommit=True)

            event_info_info_1["event_basic_sn"] = topic_1.event_basics[0].sn
            event_info_info_2["event_basic_sn"] = topic_2.event_basics[0].sn
            event_info_info_3["event_basic_sn"] = topic_3.event_basics[0].sn
            event_info_info_4["event_basic_sn"] = topic_4.event_basics[0].sn
            manager.create_event_info(event_info_info_1, autocommit=True)
            manager.create_event_info(event_info_info_2, autocommit=True)
            manager.create_event_info(event_info_info_3, autocommit=True)
            manager.create_event_info(event_info_info_4, autocommit=True)

            # test
            test_events_from_distinct_topic = manager.get_events_from_distinct_topics(limit=4)

            # assertion
            self.assertEqual(len(test_events_from_distinct_topic), 3)
            self.assertEqual(test_events_from_distinct_topic[0].date,
                             event_basic_info_1["date"])
            self.assertEqual(test_events_from_distinct_topic[1].date,
                             event_basic_info_2["date"])
            self.assertEqual(test_events_from_distinct_topic[2].date,
                             event_basic_info_3["date"])
