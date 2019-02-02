# coding=UTF-8

import unittest

from app import create_app
from app.sqldb import DBWrapper


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

    def test_get_definitions(self):
        rv = self.test_client.get("/v1.0/api/definitions")
        self.assertEquals(rv.status_code, 200)
        self.assertEquals(rv.json["info"]["code"], 0)
        self.assertEquals(len(rv.json["data"]["field"]), 12)
        self.assertEquals(len(rv.json["data"]["freq"]), 3)
        self.assertEquals(len(rv.json["data"]["level"]), 4)
        self.assertEquals(len(rv.json["data"]["host"]), 3)

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

    def test_event_not_exist(self):
        rv = self.test_client.get("/v1.0/api/apply/1")
        self.assertEquals(rv.status_code, 200)
        self.assertEquals(rv.json["info"]["code"], 1000)

    def test_routing_not_fount(self):
        rv = self.test_client.get("/v1.0/api/apply/1")
        self.assertEquals(rv.status_code, 404)
        self.assertEquals(rv.json["info"]["code"], 8000)
    
    def test_get_event_apply_info(self):
        price_info = {
            "default": 100,
            "student": 50
        }
        apply_info_data = [
            {
                "channel":0,
                "type": "one",
                "price":price_info,
                "url": "https://tw.pyladies.com/",
                "qualification": "https://tw.pyladies.com/"
            },
            {
                "channel":1,
                "type": "all",
                "price":price_info,
                "url": "https://tw.pyladies.com/",
                "qualification": ""
            }
        ]
        limit_detail = {
            "gender": "限女",
            "age": "不限"
        }
        event_apply = {
            "event_basic_id":None,
            "host": "American Innovation Center 美國創新中心",
            "start_time": "2019-01-23 08:00",
            "end_time": "2019-01-31 20:00",
            "apply": apply_info_data,
            "limit": limit_detail,
            "limit_desc": "須上傳安裝完成畫面"
            }

        # preparation
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            manager.create_price(price_info, autocommit=True)
            manager.create_apply_info(apply_info_data, autocommit=True)
            manager.create_limit_detail(limit_detail, autocommit=True)
            manager.create_event_apply(event_apply, autocommit=True)
            event_apply["event_basic_id"] = 1

        # test
        rv = self.test_client.get("/v1.0/api/apply/")
        self.assertEquals(rv.status_code, 200)
        self.assertEquals(rv.json["info"]["code"], 0)
        self.assertEquals(rv.json["data"]["event_apply"]["host"], event_apply["host"])
        self.assertEquals(rv.json["data"]["event_apply"]["start_time"], event_apply["start_time"])
        self.assertEquals(rv.json["data"]["event_apply"]["end_time"], event_apply["end_time"])
        self.assertEquals(len(rv.json["data"]["event_apply"]["apply"]), 2)
