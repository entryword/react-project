# coding=UTF-8

import unittest

from app import create_app
from app.sqldb import DBWrapper
from app.exceptions import (
    EVENTLIST_INVALID_KEYWORD, EVENTLIST_INVALID_DATE,
    EVENTLIST_INVALID_SORT, EVENTLIST_INVALID_ORDER, )


class RESTfulAPIv1_0TestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.db.create_all()
        self.test_client = self.app.test_client()

    def tearDown(self):
        self.app.db.session.remove()
        self.app.db.drop_all()
        self.app_context.pop()

    def test_routing_not_found(self):
        rv = self.test_client.get("/topic/1")
        self.assertEquals(rv.status_code, 404)
        self.assertEquals(rv.json["info"]["code"], 8000)

    def test_topic_not_exist(self):
        rv = self.test_client.get("/v1.0/api/topic/1")
        self.assertEquals(rv.status_code, 200)
        self.assertEquals(rv.json["info"]["code"], 1000)

    def test_get_topic_without_event(self):
        info = {
            "name": "topic 1",
            "desc": "This is description",
            "freq": 0,
            "level": 1,
            "host": 0,
            "fields": [0, 1, 2]
        }

        # preparation
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(info, autocommit=True)

        # test
        rv = self.test_client.get("/v1.0/api/topic/1")
        self.assertEquals(rv.status_code, 200)
        self.assertEquals(rv.json["info"]["code"], 0)
        self.assertEquals(rv.json["data"]["name"], info["name"])
        self.assertEquals(rv.json["data"]["desc"], info["desc"])
        self.assertEquals(rv.json["data"]["freq"], info["freq"])
        self.assertEquals(rv.json["data"]["level"], info["level"])
        self.assertEquals(rv.json["data"]["host"], info["host"])
        self.assertEquals(rv.json["data"]["fields"], info["fields"])
        self.assertEquals(rv.json["data"]["events"], [])
        self.assertEquals(rv.json["data"]["speakers"], [])
        self.assertEquals(rv.json["data"]["assistants"], [])
        self.assertEquals(rv.json["data"]["slides"], [])

    def test_get_topic_with_event(self):
        place_info = {
            "name": "place 1",
            "addr": "台北市信義區光復南路133號",
            "map": "http://abc.com/map.html"
        }
        speaker_info = {
            "name": "speaker 1",
            "photo": "https://pyladies.marsw.tw/img/speaker_1_photo.png",
            "title": "Senior Engineer",
            "major_related": True,
            "intro": "",
            "fields": [3]
        }
        assistant_info = {
            "name": "speaker 2",
            "photo": "https://pyladies.marsw.tw/img/speaker_2_photo.png",
            "title": "Engineer",
            "major_related": True,
            "intro": "",
            "fields": [3]
        }
        slide_resources = [
            {
                "type": "slide",
                "title": "Flask Web Development - class 1",
                "url": "http://tw.pyladies.com/~maomao/1_flask.slides.html#/"
            },
            {
                "type": "resource",
                "title": "Source Code",
                "url": "https://github.com/win911/flask_class"
            }
        ]
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
        event_info_info = {
            "event_basic_sn": None,
            "title": "Flask class 1",
            "desc": "This is description of class 1",
            "fields": [0, 1],
            "slide_resources": slide_resources
        }

        # preparation
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            event_basic_info["topic_sn"] = 1
            manager.create_place(place_info, autocommit=True)
            event_basic_info["place_sn"] = 1
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_info_info["event_basic_sn"] = 1
            manager.create_speaker(speaker_info, autocommit=True)
            event_info_info["speaker_sns"] = [1]
            manager.create_speaker(assistant_info, autocommit=True)
            event_info_info["assistant_sns"] = [2]
            manager.create_event_info(event_info_info, autocommit=True)

        # test
        rv = self.test_client.get("/v1.0/api/topic/1")
        self.assertEquals(rv.status_code, 200)
        self.assertEquals(rv.json["info"]["code"], 0)
        self.assertEquals(len(rv.json["data"]["events"]), 1)
        self.assertEquals(rv.json["data"]["events"][0]["date"], event_basic_info["date"])
        self.assertEquals(rv.json["data"]["events"][0]["place_info"]["name"], place_info["name"])
        self.assertEquals(rv.json["data"]["events"][0]["place_info"]["addr"], place_info["addr"])
        self.assertEquals(rv.json["data"]["events"][0]["place_info"]["map"], place_info["map"])
        self.assertEquals(rv.json["data"]["events"][0]["title"], event_info_info["title"])
        self.assertEquals(len(rv.json["data"]["speakers"]), 1)
        self.assertEquals(rv.json["data"]["speakers"][0]["name"], speaker_info["name"])
        self.assertEquals(rv.json["data"]["speakers"][0]["photo"], speaker_info["photo"])
        self.assertEquals(len(rv.json["data"]["assistants"]), 1)
        self.assertEquals(rv.json["data"]["assistants"][0]["name"], assistant_info["name"])
        self.assertEquals(rv.json["data"]["assistants"][0]["photo"], assistant_info["photo"])
        self.assertEquals(len(rv.json["data"]["slides"]), 1)
        self.assertEquals(rv.json["data"]["slides"][0]["title"], slide_resources[0]["title"])
        self.assertEquals(rv.json["data"]["slides"][0]["url"], slide_resources[0]["url"])
        self.assertEquals(len(rv.json["data"]["resources"]), 1)
        self.assertEquals(rv.json["data"]["resources"][0]["title"], slide_resources[1]["title"])
        self.assertEquals(rv.json["data"]["resources"][0]["url"], slide_resources[1]["url"])

    def test_get_event_not_exist(self):
        rv = self.test_client.get("/v1.0/api/event/1")
        self.assertEquals(rv.status_code, 200)
        self.assertEquals(rv.json["info"]["code"], 1100)

    def test_get_event_without_details(self):
        place_info = {
            "name": "place 1",
            "addr": "台北市信義區光復南路133號",
            "map": "http://abc.com/map.html"
        }
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

        # preparation
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            event_basic_info["topic_sn"] = 1
            manager.create_place(place_info, autocommit=True)
            event_basic_info["place_sn"] = 1
            manager.create_event_basic(event_basic_info, autocommit=True)

        # test
        rv = self.test_client.get("/v1.0/api/event/1")
        self.assertEquals(rv.status_code, 200)
        self.assertEquals(rv.json["info"]["code"], 0)
        self.assertEquals(rv.json["data"]["topic_info"]["name"], topic_info["name"])
        self.assertEquals(rv.json["data"]["title"], None)
        self.assertEquals(rv.json["data"]["fields"], [])
        self.assertEquals(rv.json["data"]["desc"], None)
        self.assertEquals(rv.json["data"]["level"], topic_info["level"])
        self.assertEquals(rv.json["data"]["date"], event_basic_info["date"])
        self.assertEquals(rv.json["data"]["start_time"], event_basic_info["start_time"])
        self.assertEquals(rv.json["data"]["end_time"], event_basic_info["end_time"])
        self.assertEquals(rv.json["data"]["place_info"]["name"], place_info["name"])
        self.assertEquals(rv.json["data"]["place_info"]["addr"], place_info["addr"])
        self.assertEquals(rv.json["data"]["place_info"]["map"], place_info["map"])
        self.assertEquals(rv.json["data"]["host"], topic_info["host"])
        self.assertEquals(rv.json["data"]["speakers"], [])
        self.assertEquals(rv.json["data"]["assistants"], [])
        self.assertEquals(rv.json["data"]["slides"], [])

    def test_get_event_with_details(self):
        place_info = {
            "name": "place 1",
            "addr": "台北市信義區光復南路133號",
            "map": "http://abc.com/map.html"
        }
        speaker_info = {
            "name": "speaker 1",
            "photo": "https://pyladies.marsw.tw/img/speaker_1_photo.png",
            "title": "Senior Engineer",
            "major_related": True,
            "intro": "",
            "fields": [3]
        }
        assistant_info = {
            "name": "speaker 2",
            "photo": "https://pyladies.marsw.tw/img/speaker_2_photo.png",
            "title": "Engineer",
            "major_related": True,
            "intro": "",
            "fields": [0, 1]
        }
        slide_resources = [
            {
                "type": "slide",
                "title": "Flask Web Development - class 1",
                "url": "http://tw.pyladies.com/~maomao/1_flask.slides.html#/"
            },
            {
                "type": "resource",
                "title": "Source Code",
                "url": "https://github.com/win911/flask_class"
            }
        ]
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
        event_info_info = {
            "event_basic_sn": None,
            "title": "Flask class 1",
            "desc": "This is description of class 1",
            "fields": [0, 1],
            "slide_resources": slide_resources
        }

        # preparation
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            event_basic_info["topic_sn"] = 1
            manager.create_place(place_info, autocommit=True)
            event_basic_info["place_sn"] = 1
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_info_info["event_basic_sn"] = 1
            manager.create_speaker(speaker_info, autocommit=True)
            event_info_info["speaker_sns"] = [1]
            manager.create_speaker(assistant_info, autocommit=True)
            event_info_info["assistant_sns"] = [2]
            manager.create_event_info(event_info_info, autocommit=True)

        # test
        rv = self.test_client.get("/v1.0/api/event/1")
        self.assertEquals(rv.status_code, 200)
        self.assertEquals(rv.json["info"]["code"], 0)
        self.assertEquals(rv.json["data"]["title"], event_info_info["title"])
        self.assertEquals(rv.json["data"]["fields"], event_info_info["fields"])
        self.assertEquals(rv.json["data"]["desc"], event_info_info["desc"])
        self.assertEquals(len(rv.json["data"]["speakers"]), 1)
        self.assertEquals(rv.json["data"]["speakers"][0]["name"], speaker_info["name"])
        self.assertEquals(rv.json["data"]["speakers"][0]["photo"], speaker_info["photo"])
        self.assertEquals(len(rv.json["data"]["assistants"]), 1)
        self.assertEquals(rv.json["data"]["assistants"][0]["name"], assistant_info["name"])
        self.assertEquals(rv.json["data"]["assistants"][0]["photo"], assistant_info["photo"])
        self.assertEquals(len(rv.json["data"]["slides"]), 1)
        self.assertEquals(rv.json["data"]["slides"][0]["title"], slide_resources[0]["title"])
        self.assertEquals(rv.json["data"]["slides"][0]["url"], slide_resources[0]["url"])
        self.assertEquals(len(rv.json["data"]["resources"]), 1)
        self.assertEquals(rv.json["data"]["resources"][0]["title"], slide_resources[1]["title"])
        self.assertEquals(rv.json["data"]["resources"][0]["url"], slide_resources[1]["url"])

    def test_search_events(self):
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

            # test invalid keyword parameters
            rv = self.test_client.get("/v1.0/api/events?keyword=abcdefghijklmnopqrstuvwxyz12345")
            self.assertEquals(rv.status_code, 200)
            self.assertEquals(rv.json["info"]["code"], EVENTLIST_INVALID_KEYWORD.code)

            # test invalid date parameters
            rv = self.test_client.get("/v1.0/api/events?date=123")
            self.assertEquals(rv.status_code, 200)
            self.assertEquals(rv.json["info"]["code"], EVENTLIST_INVALID_DATE.code)

            # test invalid sort parameters
            rv = self.test_client.get("/v1.0/api/events?sort=123")
            self.assertEquals(rv.status_code, 200)
            self.assertEquals(rv.json["info"]["code"], EVENTLIST_INVALID_SORT.code)

            # test invalid order parameters
            rv = self.test_client.get("/v1.0/api/events?order=123")
            self.assertEquals(rv.status_code, 200)
            self.assertEquals(rv.json["info"]["code"], EVENTLIST_INVALID_ORDER.code)

            # test default parameters
            # keyword = '', date = '', sort = 'date', order='asc'
            rv = self.test_client.get("/v1.0/api/events")
            self.assertEquals(rv.status_code, 200)
            self.assertEquals(rv.json["info"]["code"], 0)
            self.assertEquals(len(rv.json["data"]["events"]), 2)
            self.assertEquals(rv.json["data"]["events"][0]["event"]["title"], "event 1")

            # test empty parameters
            rv = self.test_client.get("/v1.0/api/events?keyword=&date=&sort=&order=")
            self.assertEquals(rv.status_code, 200)
            self.assertEquals(rv.json["info"]["code"], 0)
            self.assertEquals(len(rv.json["data"]["events"]), 2)
            self.assertEquals(rv.json["data"]["events"][0]["event"]["title"], "event 1")

            # test order desc
            rv = self.test_client.get("/v1.0/api/events?order=desc")
            self.assertEquals(rv.status_code, 200)
            self.assertEquals(rv.json["info"]["code"], 0)
            self.assertEquals(len(rv.json["data"]["events"]), 2)
            self.assertEquals(rv.json["data"]["events"][0]["event"]["title"], "event 2")

            # test topic keyword with date
            rv = self.test_client.get("/v1.0/api/events?keyword=topic 1&date=2019-01")
            self.assertEquals(rv.status_code, 200)
            self.assertEquals(rv.json["info"]["code"], 0)
            self.assertEquals(len(rv.json["data"]["events"]), 1)
            self.assertEquals(rv.json["data"]["events"][0]["event"]["title"], "event 1")

            # test event keyword with date
            rv = self.test_client.get("/v1.0/api/events?keyword=event 2&date=2019-01")
            self.assertEquals(rv.status_code, 200)
            self.assertEquals(rv.json["info"]["code"], 0)
            self.assertEquals(len(rv.json["data"]["events"]), 0)

    def test_get_definitions(self):
        rv = self.test_client.get("/v1.0/api/definitions")
        self.assertEquals(rv.status_code, 200)
        self.assertEquals(rv.json["info"]["code"], 0)
        self.assertEquals(len(rv.json["data"]["field"]), 12)
        self.assertEquals(len(rv.json["data"]["freq"]), 3)
        self.assertEquals(len(rv.json["data"]["level"]), 4)
        self.assertEquals(len(rv.json["data"]["host"]), 3)
        self.assertEquals(len(rv.json["data"]["status"]), 2)
        self.assertEquals(len(rv.json["data"]["weekday"]), 7)
        self.assertEquals(len(rv.json["data"]["time"]), 3)
        self.assertEquals(len(rv.json["data"]["channel"]), 2)
        self.assertEquals(len(rv.json["data"]["type"]), 2)

    def test_get_definition(self):
        rv = self.test_client.get("/v1.0/api/definition/field")
        self.assertEquals(rv.status_code, 200)
        self.assertEquals(rv.json["info"]["code"], 0)
        self.assertEquals(len(rv.json["data"]), 12)

        rv = self.test_client.get("/v1.0/api/definition/freq")
        self.assertEquals(rv.status_code, 200)
        self.assertEquals(rv.json["info"]["code"], 0)
        self.assertEquals(len(rv.json["data"]), 3)

        rv = self.test_client.get("/v1.0/api/definition/level")
        self.assertEquals(rv.status_code, 200)
        self.assertEquals(rv.json["info"]["code"], 0)
        self.assertEquals(len(rv.json["data"]), 4)

        rv = self.test_client.get("/v1.0/api/definition/host")
        self.assertEquals(rv.status_code, 200)
        self.assertEquals(rv.json["info"]["code"], 0)
        self.assertEquals(len(rv.json["data"]), 3)

        rv = self.test_client.get("/v1.0/api/definition/status")
        self.assertEquals(rv.status_code, 200)
        self.assertEquals(rv.json["info"]["code"], 0)
        self.assertEquals(len(rv.json["data"]), 2)

        rv = self.test_client.get("/v1.0/api/definition/weekday")
        self.assertEquals(rv.status_code, 200)
        self.assertEquals(rv.json["info"]["code"], 0)
        self.assertEquals(len(rv.json["data"]), 7)

        rv = self.test_client.get("/v1.0/api/definition/time")
        self.assertEquals(rv.status_code, 200)
        self.assertEquals(rv.json["info"]["code"], 0)
        self.assertEquals(len(rv.json["data"]), 3)

        rv = self.test_client.get("/v1.0/api/definition/channel")
        self.assertEquals(rv.status_code, 200)
        self.assertEquals(rv.json["info"]["code"], 0)
        self.assertEquals(len(rv.json["data"]), 2)

        rv = self.test_client.get("/v1.0/api/definition/type")
        self.assertEquals(rv.status_code, 200)
        self.assertEquals(rv.json["info"]["code"], 0)
        self.assertEquals(len(rv.json["data"]), 2)

    def test_get_places(self):
        places = [
            {
                "name": "place 1",
                "addr": "台北市信義區光復南路133號",
                "map": "http://abc.com/map1.html"
            },
            {
                "name": "place 2",
                "addr": "台北市萬華區艋舺大道101號",
                "map": "http://abc.com/map2.html"
            },
            {
                "name": "place 3",
                "addr": "台北市大安區和平東路二段50號",
                "map": "http://abc.com/map3.html"
            }
        ]

        # preparation
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            for place in places:
                manager.create_place(place, autocommit=True)

        # test
        rv = self.test_client.get("/v1.0/api/places")
        self.assertEquals(rv.status_code, 200)
        self.assertEquals(rv.json["info"]["code"], 0)
        self.assertEquals(rv.json["data"]["places"][1]["name"], places[1]["name"])
        self.assertEquals(rv.json["data"]["places"][1]["addr"], places[1]["addr"])
        self.assertEquals(rv.json["data"]["places"][1]["map"], places[1]["map"])
        self.assertEquals(len(rv.json["data"]["places"]), 3)

    def test_get_event_apply_info(self):
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
            "price_default": 400,
            "price_student": 200,
            "url": "https://...",
            "qualification": "https://..."
        }

        apply_info_2 = {
            "host": "American Innovation Center 美國創新中心",
            "channel": 0,
            "type": "one",
            "price_default": 100,
            "price_student": 50,
            "url": "https://...",
            "qualification": "https://..."
        }

        input_event_apply = {
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
        rv = self.test_client.get("/v1.0/api/apply_info/" + str(event_apply_sn))
        self.assertEquals(rv.status_code, 200)
        self.assertEquals(rv.json["info"]["code"], 0)
        self.assertEquals(rv.json["data"], input_event_apply)

    def test_get_event_apply_info_by_event_basic_sn(self):
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
            "price_default": 400,
            "price_student": 200,
            "url": "https://...",
            "qualification": "https://..."
        }

        apply_info_2 = {
            "host": "American Innovation Center 美國創新中心",
            "channel": 0,
            "type": "one",
            "price_default": 100,
            "price_student": 50,
            "url": "https://...",
            "qualification": "https://..."
        }

        input_event_apply = {
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

        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_basic = topic.event_basics[0]
            input_event_apply["event_basic_sn"] = event_basic.sn
            manager.create_event_apply(input_event_apply, autocommit=True)

        # test
        rv = self.test_client.get("/v1.0/api/event/"
                                  + str(input_event_apply["event_basic_sn"]) + "/apply_info")
        self.assertEquals(rv.status_code, 200)
        self.assertEquals(rv.json["info"]["code"], 0)
        self.assertEquals(rv.json["data"], input_event_apply)

    def test_get_event_apply_info_but_event_not_exist(self):
        rv = self.test_client.get("/v1.0/api/apply_info/0")
        self.assertEquals(rv.status_code, 200)
        self.assertEquals(rv.json["info"]["code"], 1600)

    def test_get_event_apply_info_by_event_basic_sn_but_event_not_exist(self):
        rv = self.test_client.get("/v1.0/api/event/0/apply_info")
        self.assertEquals(rv.status_code, 200)
        self.assertEquals(rv.json["info"]["code"], 1600)
