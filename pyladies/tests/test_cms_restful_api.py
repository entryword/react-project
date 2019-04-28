# coding=UTF-8

import json

from app import create_app
from app.sqldb import DBWrapper


class TestCreateEvent:
    def setup(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.db.create_all()
        self.test_client = self.app.test_client()

    def teardown(self):
        self.app.db.session.remove()
        self.app.db.drop_all()
        self.app_context.pop()

    def test_success(self, topic_info, place_info):
        speaker_info = {
            "name": "speaker 1",
            "photo": "https://pyladies.marsw.tw/img/speaker_1_photo.png",
            "title": "Senior Engineer",
            "major_related": True,
            "intro": "",
            "fields": [3],
        }
        assistant_info = {
            "name": "speaker 2",
            "photo": "https://pyladies.marsw.tw/img/speaker_2_photo.png",
            "title": "Engineer",
            "major_related": True,
            "intro": "",
            "fields": [3],
        }

        postdata = {
            "data": {
                "title": "XXXX",
                "topic_id": None,
                "start_date": "2019-03-09",
                "start_time": "14:00",
                "end_date": "2019-03-09",
                "end_time": "17:00",
                "place_id": None,
                "desc": "XXXX",
                "speaker_ids": [1],
                "assistant_ids": [2],
                "field_ids": [1, 2],
            }
        }
        # preparation
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            manager.create_place(place_info, autocommit=True)
            manager.create_speaker(speaker_info, autocommit=True)
            manager.create_speaker(assistant_info, autocommit=True)

            topic = manager.get_topic_by_name(topic_info["name"])
            place = manager.get_place_by_name(place_info["name"])
            postdata["data"]["topic_id"] = topic.sn
            postdata["data"]["place_id"] = place.sn

        # post test
        rv = self.test_client.post(
            "/cms/api/event",
            headers={"Content-Type": "application/json"},
            data=json.dumps(postdata),
            content_type="application/json",
        )
        # api assertion
        assert rv.status_code == 200
        assert rv.json["info"]["code"] == 0
        assert rv.json["data"]["id"] == 1
        event_basic_sn = rv.json["data"]["id"]

        # event assertion
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            event_basic = manager.get_event_basic(event_basic_sn)
            assert event_basic.topic.name == topic_info["name"]
            assert event_basic.place.name == place_info["name"]
            assert event_basic.place.map == place_info["map"]
            assert event_basic.date == postdata["data"]["start_date"]
            assert event_basic.start_time == postdata["data"]["start_time"]
            assert event_basic.end_time == postdata["data"]["end_time"]


class TestGetEvents:
    def setup(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.db.create_all()
        self.test_client = self.app.test_client()

    def teardown(self):
        self.app.db.session.remove()
        self.app.db.drop_all()
        self.app_context.pop()

    def _preparation_for_one_event(self, topic, event_basic, event_info, place, speaker=None, apply=None):
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            topic_sn = manager.create_topic(topic, autocommit=True)
            place_sn = manager.create_place(place, autocommit=True)
            event_basic.update({
                "topic_sn": topic_sn,
                "place_sn": place_sn
            })
            event_basic_sn = manager.create_event_basic(event_basic, autocommit=True)
            event_info["event_basic_sn"] = event_basic_sn
            if speaker:
                speaker_sn = manager.create_speaker(speaker, autocommit=True)
                event_info["speaker_sns"] = [speaker_sn]
            manager.create_event_info(event_info, autocommit=True)
            if apply:
                apply["event_basic_sn"] = event_basic_sn
                manager.create_event_apply(apply, autocommit=True)

    def test_one_event(self, topic_info, event_basic_info, place_info, apply_info):
        event_info_info = {
            "event_basic_sn": None,
            "title": "Flask class 1",
            "desc": "This is description of class 1",
            "fields": [0, 1]
        }
        speaker_info = {
            "name": "speaker 1",
            "photo": "https://pyladies.marsw.tw/img/speaker_1_photo.png",
            "title": "Senior Engineer",
            "major_related": True,
            "intro": "",
            "fields": [3]
        }
        event_apply_info = {
            "event_basic_sn": None,
            "apply": [apply_info]
        }
        self._preparation_for_one_event(topic_info, event_basic_info, event_info_info,
                                        place_info, speaker_info, event_apply_info)

        # test
        rv = self.test_client.get("/cms/api/events")

        # assertion
        expected_result = {
            "date": event_basic_info["date"],
            "event_apply_exist": 1,
            "id": event_info_info["event_basic_sn"],
            "place": {
                "name": place_info["name"]
            },
            "speaker_exist": 1,
            "title": event_info_info["title"],
            "topic": {
                "name": topic_info["name"]
            },
            "end_time": event_basic_info["end_time"],
            "start_time": event_basic_info["start_time"]
        }
        assert len(rv.json["data"]) == 1
        assert rv.json["data"][0] == expected_result

    def test_one_event_without_apply(self, topic_info, event_basic_info, place_info):
        event_info_info = {
            "event_basic_sn": None,
            "title": "Flask class 1",
            "desc": "This is description of class 1",
            "fields": [0, 1]
        }
        speaker_info = {
            "name": "speaker 1",
            "photo": "https://pyladies.marsw.tw/img/speaker_1_photo.png",
            "title": "Senior Engineer",
            "major_related": True,
            "intro": "",
            "fields": [3]
        }
        self._preparation_for_one_event(topic_info, event_basic_info, event_info_info,
                                        place_info, speaker_info, None)

        # test
        rv = self.test_client.get("/cms/api/events")

        # assertion
        assert rv.json["data"][0]["event_apply_exist"] == 0
        assert rv.json["data"][0]["speaker_exist"] == 1

    def test_one_event_without_speaker(self, topic_info, event_basic_info, place_info, apply_info):
        event_info_info = {
            "event_basic_sn": None,
            "title": "Flask class 1",
            "desc": "This is description of class 1",
            "fields": [0, 1]
        }
        event_apply_info = {
            "event_basic_sn": None,
            "apply": [apply_info]
        }
        self._preparation_for_one_event(topic_info, event_basic_info, event_info_info,
                                        place_info, None, event_apply_info)

        # test
        rv = self.test_client.get("/cms/api/events")

        # assertion
        assert rv.json["data"][0]["event_apply_exist"] == 1
        assert rv.json["data"][0]["speaker_exist"] == 0

    def test_one_event_without_speaker_and_apply(self, topic_info, event_basic_info, place_info):
        event_info_info = {
            "event_basic_sn": None,
            "title": "Flask class 1",
            "desc": "This is description of class 1",
            "fields": [0, 1]
        }
        self._preparation_for_one_event(topic_info, event_basic_info, event_info_info, place_info)

        # test
        rv = self.test_client.get("/cms/api/events")

        # assertion
        assert rv.json["data"][0]["event_apply_exist"] == 0
        assert rv.json["data"][0]["speaker_exist"] == 0


class TestGetPlaces:
    def setup(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.db.create_all()
        self.test_client = self.app.test_client()

    def teardown(self):
        self.app.db.session.remove()
        self.app.db.drop_all()
        self.app_context.pop()

    def test_get_places(self):
        places = [
            {
                "name": "place 1",
                "addr": "台北市信義區光復南路133號",
                "map": "http://abc.com/map1.html",
            },
            {
                "name": "place 2",
                "addr": "台北市萬華區艋舺大道101號",
                "map": "http://abc.com/map2.html",
            },
            {
                "name": "place 3",
                "addr": "台北市大安區和平東路二段50號",
                "map": "http://abc.com/map3.html",
            },
        ]

        # preparation
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            for place in places:
                manager.create_place(place, autocommit=True)

        # test
        rv = self.test_client.get("/cms/api/places")

        #assert
        assert rv.json["info"]["code"] == 0
        assert len(rv.json["data"]) == 3
        assert rv.json["data"][0]["name"] == places[0]["name"]
        assert rv.json["data"][1]["addr"] == places[1]["addr"]
        assert rv.json["data"][2]["id"] == 3
