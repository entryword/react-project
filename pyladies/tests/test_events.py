import pytest
from datetime import datetime, timedelta

from app import create_app
from app.sqldb import DBWrapper


class TestEvents:
    def setup(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.db.create_all()

    def teardown(self):
        self.app.db.session.remove()
        self.app.db.drop_all()
        self.app_context.pop()

    @staticmethod
    def get_past_date(interval=1):
        past_time = datetime.utcnow() + timedelta(days=interval * (-1), hours=8)
        return past_time.strftime("%Y-%m-%d")

    @staticmethod
    def get_future_date(interval=1):
        future_time = datetime.utcnow() + timedelta(days=interval, hours=8)
        return future_time.strftime("%Y-%m-%d")

    @pytest.mark.parametrize('topic_infos', [2], indirect=True)
    @pytest.mark.parametrize('event_basic_infos', [2], indirect=True)
    def test_search_events_with_keywords(self, topic_infos, place_info, event_basic_infos):
        topics = [topic_infos[0], topic_infos[1]]
        event_basic_infos[0]['topic_sn'] = 1
        event_basic_infos[1]['topic_sn'] = 1
        event_basics = [event_basic_infos[0], event_basic_infos[1]]
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
            assert len(event_basics) == 2

            # test keyword event
            keyword = 'event'
            event_basics = manager.search_event_basics(keyword, date)
            assert len(event_basics) == 2

            # test keyword event 1
            keyword = 'event 1'
            event_basics = manager.search_event_basics(keyword, date)
            assert len(event_basics) == 1
            assert event_basics[0].event_info.title == "event 1"

            # test keyword topic
            keyword = 'topic'
            event_basics = manager.search_event_basics(keyword, date)
            assert len(event_basics) == 2

            # test keyword topic 1
            keyword = 'topic 1'
            event_basics = manager.search_event_basics(keyword, date)
            assert len(event_basics) == 2

            # test keyword topic 2
            keyword = 'topic 2'
            event_basics = manager.search_event_basics(keyword, date)
            assert len(event_basics) == 0

            # test keyword abc
            keyword = 'abc'
            event_basics = manager.search_event_basics(keyword, date)
            assert len(event_basics) == 0

    @pytest.mark.parametrize('topic_infos', [2], indirect=True)
    @pytest.mark.parametrize('event_basic_infos', [3], indirect=True)
    def test_search_events_with_date(self, topic_infos, place_info, event_basic_infos):
        topics = [topic_infos[0], topic_infos[1]]
        event_basic_infos[0]['topic_sn'] = 1
        event_basic_infos[1]['topic_sn'] = 1
        event_basic_infos[2]['topic_sn'] = 2
        event_basic_infos[0]['date'] = "2019-01-07"
        event_basic_infos[1]['date'] = "2019-02-03"
        event_basic_infos[2]['date'] = "2019-02-17"
        event_basics = [event_basic_infos[0], event_basic_infos[1], event_basic_infos[2]]
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
            assert len(event_basics) == 3

            # test date 2019-01
            date = '2019-01'
            event_basics = manager.search_event_basics(keyword, date)
            assert len(event_basics) == 1
            assert event_basics[0].event_info.title == "event 1"

            # test date 2019-02
            date = '2019-02'
            event_basics = manager.search_event_basics(keyword, date)
            assert len(event_basics) == 2
            assert event_basics[0].event_info.title == "event 2"
            assert event_basics[1].event_info.title == "event 3"

    @pytest.mark.parametrize('topic_infos', [2], indirect=True)
    @pytest.mark.parametrize('event_basic_infos', [3], indirect=True)
    def test_search_events_with_keywords_and_date(self, topic_infos, place_info, event_basic_infos):
        topics = [topic_infos[0], topic_infos[1]]
        event_basic_infos[0]['topic_sn'] = 1
        event_basic_infos[1]['topic_sn'] = 1
        event_basic_infos[2]['topic_sn'] = 2
        event_basic_infos[0]['date'] = "2019-01-07"
        event_basic_infos[1]['date'] = "2019-02-03"
        event_basic_infos[2]['date'] = "2019-02-17"
        event_basics = [event_basic_infos[0], event_basic_infos[1], event_basic_infos[2]]

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
            assert len(event_basics) == 1
            assert event_basics[0].event_info.title == "event 2"

            # test date 2019-02 and keyword event 1
            keyword = 'event 1'
            date = '2019-02'
            event_basics = manager.search_event_basics(keyword, date)
            assert len(event_basics) == 0

    def test_get_no_event_from_one_topic_because_of_no_event_basic(self, topic_info):
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)

            # test
            test_events_from_distinct_topic = manager.get_events_from_distinct_topics(limit=4)

            # assertion
            assert len(test_events_from_distinct_topic) == 0

    def test_get_no_event_from_one_topic_because_of_no_event_info(self, topic_info, event_basic_info):
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
            assert len(test_events_from_distinct_topic) == 0

    def test_get_no_event_from_one_topic_because_of_past_event(self, topic_info, event_basic_info):
        event_basic_info['date'] = self.get_past_date(1)
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
            assert len(test_events_from_distinct_topic) == 0

    def test_get_event_from_one_topic_with_only_one_future_event(self, topic_info, event_basic_info):
        event_basic_info['date'] = self.get_future_date(1)
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
            assert len(test_events_from_distinct_topic) == 1
            assert test_events_from_distinct_topic[0].date == event_basic_info["date"]

    @pytest.mark.parametrize('event_basic_infos', [2], indirect=True)
    def test_get_event_from_one_topic_with_multiple_future_events(self, topic_info, event_basic_infos):
        def _get_future_date(interval=1):
            future_time = datetime.utcnow() + timedelta(days=interval, hours=8)
            return future_time.strftime("%Y-%m-%d")

        event_basic_infos[0]['date'] = self.get_future_date(1)
        event_basic_infos[1]['date'] = self.get_future_date(2)
        event_basic_info_1 = event_basic_infos[0]
        event_basic_info_2 = event_basic_infos[1]
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
            assert len(test_events_from_distinct_topic) == 1
            assert test_events_from_distinct_topic[0].date == event_basic_info_1["date"]

    @pytest.mark.parametrize('topic_infos', [4], indirect=True)
    @pytest.mark.parametrize('event_basic_infos', [4], indirect=True)
    def test_get_events_from_four_distinct_level_topics(self, topic_infos, event_basic_infos):
        topic_info_1 = topic_infos[0]
        topic_info_1['level'] = 1
        topic_info_2 = topic_infos[1]
        topic_info_2['level'] = 2
        topic_info_3 = topic_infos[2]
        topic_info_3['level'] = 3
        topic_info_4 = topic_infos[3]
        topic_info_4['level'] = 4
        event_basic_infos[0]['date'] = self.get_future_date(1)
        event_basic_infos[1]['date'] = self.get_future_date(2)
        event_basic_infos[2]['date'] = self.get_future_date(3)
        event_basic_infos[3]['date'] = self.get_future_date(4)
        event_basic_info_1 = event_basic_infos[0]
        event_basic_info_2 = event_basic_infos[1]
        event_basic_info_3 = event_basic_infos[2]
        event_basic_info_4 = event_basic_infos[3]
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
            assert len(test_events_from_distinct_topic) == 4
            assert test_events_from_distinct_topic[0].date == event_basic_info_1["date"]
            assert test_events_from_distinct_topic[1].date == event_basic_info_2["date"]
            assert test_events_from_distinct_topic[2].date == event_basic_info_3["date"]
            assert test_events_from_distinct_topic[3].date == event_basic_info_4["date"]

    @pytest.mark.parametrize('topic_infos', [5], indirect=True)
    @pytest.mark.parametrize('event_basic_infos', [5], indirect=True)
    def test_get_events_from_five_distinct_level_topics(self, topic_infos, event_basic_infos):
        topic_info_1 = topic_infos[0]
        topic_info_1['level'] = 1
        topic_info_2 = topic_infos[1]
        topic_info_2['level'] = 2
        topic_info_3 = topic_infos[2]
        topic_info_3['level'] = 3
        topic_info_4 = topic_infos[3]
        topic_info_4['level'] = 4
        topic_info_5 = topic_infos[4]
        topic_info_5['level'] = 5
        event_basic_infos[0]['date'] = self.get_future_date(1)
        event_basic_infos[1]['date'] = self.get_future_date(2)
        event_basic_infos[2]['date'] = self.get_future_date(3)
        event_basic_infos[3]['date'] = self.get_future_date(4)
        event_basic_infos[4]['date'] = self.get_future_date(5)
        event_basic_info_1 = event_basic_infos[0]
        event_basic_info_2 = event_basic_infos[1]
        event_basic_info_3 = event_basic_infos[2]
        event_basic_info_4 = event_basic_infos[3]
        event_basic_info_5 = event_basic_infos[4]

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
            assert len(test_events_from_distinct_topic) == 4
            assert test_events_from_distinct_topic[0].date == event_basic_info_1["date"]
            assert test_events_from_distinct_topic[1].date == event_basic_info_2["date"]
            assert test_events_from_distinct_topic[2].date == event_basic_info_3["date"]
            assert test_events_from_distinct_topic[3].date == event_basic_info_4["date"]

    @pytest.mark.parametrize('topic_infos', [4], indirect=True)
    @pytest.mark.parametrize('event_basic_infos', [4], indirect=True)
    def test_get_events_from_four_topics_but_two_are_same_level(self, topic_infos, event_basic_infos):
        topic_info_1 = topic_infos[0]
        topic_info_1['level'] = 1
        topic_info_2 = topic_infos[1]
        topic_info_2['level'] = 2
        topic_info_3 = topic_infos[2]
        topic_info_3['level'] = 3
        topic_info_4 = topic_infos[3]
        topic_info_4['level'] = 3
        event_basic_infos[0]['date'] = self.get_future_date(1)
        event_basic_infos[1]['date'] = self.get_future_date(2)
        event_basic_infos[2]['date'] = self.get_future_date(3)
        event_basic_infos[3]['date'] = self.get_future_date(4)
        event_basic_info_1 = event_basic_infos[0]
        event_basic_info_2 = event_basic_infos[1]
        event_basic_info_3 = event_basic_infos[2]
        event_basic_info_4 = event_basic_infos[3]

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
            assert len(test_events_from_distinct_topic) == 3
            assert test_events_from_distinct_topic[0].date == event_basic_info_1["date"]
            assert test_events_from_distinct_topic[1].date == event_basic_info_2["date"]
            assert test_events_from_distinct_topic[2].date == event_basic_info_3["date"]
