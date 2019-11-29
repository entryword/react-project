# coding=UTF-8

import json
import pytest
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

import pytest
from app import create_app
from app.sqldb import DBWrapper
from app.sqldb.models import User


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
        self.app.db.engine.dispose()
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
        self.app.db.engine.dispose()
        self.app_context.pop()

    @staticmethod
    def get_future_date(interval=1):
        future_time = datetime.utcnow() + timedelta(days=interval, hours=8)
        return future_time.strftime("%Y-%m-%d")

    def _preparation_for_event(self, topic_info, event_basic_infos, event_infos, place, speaker=None, apply=None):
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            topic_sn = manager.create_topic(topic_info, autocommit=True)
            place_sn = manager.create_place(place, autocommit=True)
            if speaker:
                speaker_sn = manager.create_speaker(speaker, autocommit=True)
            else:
                speaker_sn = None
            for event_basic_info, event_info in \
                    zip(event_basic_infos, event_infos):
                event_basic_info['topic_sn'] = topic_sn
                event_basic_info['place_sn'] = place_sn
                event_basic_sn = manager.create_event_basic(event_basic_info, autocommit=True)
                if apply:
                    apply["event_basic_sn"] = event_basic_sn
                    manager.create_event_apply(apply, autocommit=True)
                event_info['event_basic_sn'] = event_basic_sn
                event_info["speaker_sns"] = [speaker_sn]
                manager.create_event_info(event_info, autocommit=True)

    def test_one_event(self, event_info, speaker_info, topic_info, event_basic_info, place_info, apply_info):
        event_apply_info = {
            "event_basic_sn": None,
            "apply": [apply_info]
        }
        self._preparation_for_event(topic_info, [event_basic_info], [event_info],
                                    place_info, speaker_info, event_apply_info)

        # test
        rv = self.test_client.get("/cms/api/events")

        # assertion
        expected_result = {
            "date": event_basic_info["date"],
            "event_apply_exist": 1,
            "id": event_info["event_basic_sn"],
            "place": {
                "name": place_info["name"]
            },
            "speaker_exist": 1,
            "title": event_info["title"],
            "topic": {
                "name": topic_info["name"]
            },
            "end_time": event_basic_info["end_time"],
            "start_time": event_basic_info["start_time"]
        }
        assert len(rv.json["data"]) == 1
        assert rv.json["data"][0] == expected_result

    def test_one_event_without_apply(self, topic_info, event_basic_info, event_info, speaker_info, place_info):
        self._preparation_for_event(topic_info, [event_basic_info], [event_info], place_info, speaker_info, None)

        # test
        rv = self.test_client.get("/cms/api/events")

        # assertion
        assert rv.json["data"][0]["event_apply_exist"] == 0
        assert rv.json["data"][0]["speaker_exist"] == 1

    def test_one_event_without_speaker(self, topic_info, event_basic_info, event_info, place_info, apply_info):
        event_apply_info = {
            "event_basic_sn": None,
            "apply": [apply_info]
        }
        self._preparation_for_event(topic_info, [event_basic_info], [event_info], place_info, None, event_apply_info)

        # test
        rv = self.test_client.get("/cms/api/events")

        # assertion
        assert rv.json["data"][0]["event_apply_exist"] == 1
        assert rv.json["data"][0]["speaker_exist"] == 0

    def test_one_event_without_speaker_and_apply(self, event_info, topic_info, event_basic_info, place_info):
        self._preparation_for_event(topic_info, [event_basic_info], [event_info], place_info)

        # test
        rv = self.test_client.get("/cms/api/events")

        # assertion
        assert rv.json["data"][0]["event_apply_exist"] == 0
        assert rv.json["data"][0]["speaker_exist"] == 0

    @pytest.mark.parametrize('event_basic_infos', [2], indirect=True)
    @pytest.mark.parametrize('event_infos', [2], indirect=True)
    def test_events(self, topic_info, event_basic_infos, event_infos, place_info, speaker_info, apply_info):
        # preparation
        event_apply_info = {
            "event_basic_sn": None,
            "apply": [apply_info]
        }
        self._preparation_for_event(topic_info, event_basic_infos, event_infos,
                                    place_info, speaker_info, event_apply_info)

        # test
        rv = self.test_client.get("/cms/api/events")

        # assertion
        assert len(rv.json["data"]) == 2
        for i in range(2):
            expected_result = {
                "date": event_basic_infos[i]["date"],
                "event_apply_exist": 1,
                "id": event_infos[i]["event_basic_sn"],
                "place": {
                    "name": place_info["name"]
                },
                "speaker_exist": 1,
                "title": event_infos[i]["title"],
                "topic": {
                    "name": topic_info["name"]
                },
                "end_time": event_basic_infos[i]["end_time"],
                "start_time": event_basic_infos[i]["start_time"]
            }
            assert rv.json["data"][i] == expected_result

    @pytest.mark.parametrize('event_basic_infos', [2], indirect=True)
    @pytest.mark.parametrize('event_infos', [2], indirect=True)
    def test_events_without_apply(self, event_infos, speaker_info, topic_info, event_basic_infos, place_info):
        self._preparation_for_event(topic_info, event_basic_infos, event_infos, place_info, speaker_info, None)

        # test
        rv = self.test_client.get("/cms/api/events")

        # assertion
        assert rv.json["data"][0]["event_apply_exist"] == 0
        assert rv.json["data"][0]["speaker_exist"] == 1

    @pytest.mark.parametrize('event_basic_infos', [2], indirect=True)
    @pytest.mark.parametrize('event_infos', [2], indirect=True)
    def test_events_without_speaker(self, event_infos, topic_info, event_basic_infos, place_info, apply_info):
        event_apply_info = {
            "event_basic_sn": None,
            "apply": [apply_info]
        }
        self._preparation_for_event(topic_info, event_basic_infos, event_infos, place_info, None, event_apply_info)

        # test
        rv = self.test_client.get("/cms/api/events")

        # assertion
        assert rv.json["data"][0]["event_apply_exist"] == 1
        assert rv.json["data"][0]["speaker_exist"] == 0

    @pytest.mark.parametrize('event_basic_infos', [2], indirect=True)
    @pytest.mark.parametrize('event_infos', [2], indirect=True)
    def test_events_without_speaker_and_apply(self, event_infos, topic_info, event_basic_infos, place_info):
        self._preparation_for_event(topic_info, event_basic_infos, event_infos, place_info)

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
        self.app.db.engine.dispose()
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

        # assert
        assert rv.json["info"]["code"] == 0
        assert len(rv.json["data"]) == 3
        assert rv.json["data"][0]["name"] == places[0]["name"]
        assert rv.json["data"][1]["addr"] == places[1]["addr"]
        assert rv.json["data"][2]["id"] == 3


class TestGetSlides:
    def setup(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.db.create_all()
        self.test_client = self.app.test_client()

    def teardown(self):
        self.app.db.session.remove()
        self.app.db.drop_all()
        self.app.db.engine.dispose()
        self.app_context.pop()

    def test_get_slides(self):
        slide_1 = {
            "title": "Dive into Pinkoi 2013 活動投影片",
            "type": "slide",
            "url": "https://speakerdeck.com/mosky/dive-into-pinkoi-2013"
        }
        slide_2 = {
            "title": "ihower 的 Git 教室",
            "type": "resource",
            "url": "https://ihower.tw/git/"
        }
        # preparation
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            manager.create_slide_resource(slide_1, autocommit=True)
            manager.create_slide_resource(slide_2, autocommit=True)
        # test
        rv = self.test_client.get("/cms/api/slides")

        # assertion
        assert rv.json["data"][0]["id"] == 1
        assert rv.json["data"][0]["type"] == "slide"
        assert rv.json["data"][0]["title"] == "Dive into Pinkoi 2013 活動投影片"
        assert rv.json["data"][0]["url"] == "https://speakerdeck.com/mosky/dive-into-pinkoi-2013"
        assert rv.json["data"][1]["id"] == 2
        assert rv.json["data"][1]["type"] == "resource"
        assert rv.json["data"][1]["title"] == "ihower 的 Git 教室"
        assert rv.json["data"][1]["url"] == "https://ihower.tw/git/"


class TestGetSpeakers:
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

    @pytest.mark.parametrize('speaker_infos', [3], indirect=True)
    def test_get_speakers(self, speaker_infos):
        # preparation
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            for speaker in speaker_infos:
                manager.create_speaker(speaker, autocommit=True)

        # test
        rv = self.test_client.get("/cms/api/speakers")

        #assert
        assert rv.json["info"]["code"] == 0
        assert len(rv.json["data"]) == 3
        for i in range(3):
            assert rv.json["data"][i]["name"] == speaker_infos[i]["name"]


class TestGetTopics:
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

    @pytest.mark.parametrize('topic_infos', [3], indirect=True)
    def test_get_topics(self, topic_infos):
        # preparation
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            for topic in topic_infos:
                manager.create_topic(topic, autocommit=True)

        # test
        rv = self.test_client.get("/cms/api/topics")

        #assert
        assert rv.json["info"]["code"] == 0
        assert len(rv.json["data"]) == 3
        assert rv.json["data"][0]["name"] == topic_infos[0]["name"]
        assert rv.json["data"][1]["name"] == topic_infos[1]["name"]
        assert rv.json["data"][2]["name"] == topic_infos[2]["name"]


class TestCreateSlideResource:
    def setup(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.db.create_all()
        self.test_client = self.app.test_client()

    def teardown(self):
        self.app.db.session.remove()
        self.app.db.drop_all()
        self.app.db.engine.dispose()
        self.app_context.pop()

    def test_success(self):
        slide_info = {
            "type": "slide",
            "title": "TEST_SLIDE2",
            "url": "http://789101112"
        }

        # post
        rv = self.test_client.post(
            "/cms/api/slide",
            headers={"Content-Type": "application/json"},
            content_type="application/json",
            data=json.dumps({'data': slide_info}),
        )

        # api assertion
        assert rv.status_code == 200
        assert rv.json["info"]["code"] == 0
        assert rv.json["data"]["id"] == 1
        assert rv.json["data"]["title"] == slide_info["title"]
        assert rv.json["data"]["type"] == slide_info["type"]
        assert rv.json["data"]["url"] == slide_info["url"]


class TestLogin:
    def setup(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.db.create_all()
        self.test_client = self.app.test_client()

    def teardown(self):
        self.app.db.session.remove()
        self.app.db.drop_all()
        self.app.db.engine.dispose()
        self.app_context.pop()

    def create_new_user(self, login_info):
        user_info = {
            "name": login_info["username"],
            "password_hash": generate_password_hash(login_info["password"], method="pbkdf2:sha1")
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            obj = User(**user_info)
            db_sess.add(obj)
            db_sess.commit()

    def test_invalid_input(self):
        login_info = {
            "username": "pyladies",
            "password": ""
        }

        rv = self.test_client.post("/cms/api/login", json=login_info)

        assert rv.json["info"]["code"] == 1

    def test_user_not_exist(self):
        login_info = {
            "username": "pyladies",
            "password": "test123456"
        }

        rv = self.test_client.post("/cms/api/login", json=login_info)

        assert rv.json["info"]["code"] == 1701

    def test_wrong_password(self):
        login_info = {
            "username": "pyladies",
            "password": "test123456"
        }
        self.create_new_user(login_info)

        login_info["password"] = "12345678"
        rv = self.test_client.post("/cms/api/login", json=login_info)

        assert rv.json["info"]["code"] == 1701

    def test_success(self):
        login_info = {
            "username": "pyladies",
            "password": "test123456"
        }
        self.create_new_user(login_info)

        rv = self.test_client.post("/cms/api/login", json=login_info)

        assert rv.json["info"]["code"] == 0


class TestLogout:
    def setup(self):
        self.app = create_app('test2')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.db.create_all()
        self.test_client = self.app.test_client()

    def teardown(self):
        self.app.db.session.remove()
        self.app.db.drop_all()
        self.app.db.engine.dispose()
        self.app_context.pop()

    def create_new_user(self, login_info):
        user_info = {
            "name": login_info["username"],
            "password_hash": generate_password_hash(login_info["password"], method="pbkdf2:sha1")
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            obj = User(**user_info)
            db_sess.add(obj)
            db_sess.commit()

    def test_not_login(self):
        rv = self.test_client.put("/cms/api/logout")

        assert rv.json["info"]["code"] == 1702

    def test_success(self):
        login_info = {
            "username": "pyladies",
            "password": "test123456"
        }
        self.create_new_user(login_info)
        self.test_client.post("/cms/api/login", json=login_info)

        rv = self.test_client.put("/cms/api/logout")

        assert rv.json["info"]["code"] == 0


class TestGetEvent:
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
        testurl = "/cms/api/event/"+str(event_info_info["event_basic_sn"])
        rv = self.test_client.get(testurl)

        # assertion
        assert rv.json["data"]["start_time"] == event_basic_info["start_time"]
        assert rv.json["data"]["end_time"] == event_basic_info["end_time"]
        assert rv.json["data"]["topic_id"] == event_basic_info["topic_sn"]
        assert rv.json["data"]["place_info"]["id"] == event_basic_info["place_sn"]
        assert rv.json["data"]["title"] == event_info_info["title"]
        assert rv.json["data"]["desc"] == event_info_info["desc"]
        assert rv.json["data"]["fields"] == event_info_info["fields"]
        assert rv.json["data"]["speakers"][0]["name"] == speaker_info["name"]
        assert rv.json["data"]["apply"][0]["host"] == apply_info["host"]
        assert rv.json["data"]["apply"][0]["channel"] == apply_info["channel"]
        assert rv.json["data"]["slide_resources"] == []

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
        testurl = "/cms/api/event/"+str(event_info_info["event_basic_sn"])
        rv = self.test_client.get(testurl)

        # assertion
        assert rv.json["data"]["start_time"] == event_basic_info["start_time"]
        assert rv.json["data"]["end_time"] == event_basic_info["end_time"]
        assert rv.json["data"]["topic_id"] == event_basic_info["topic_sn"]
        assert rv.json["data"]["place_info"]["id"] == event_basic_info["place_sn"]
        assert rv.json["data"]["title"] == event_info_info["title"]
        assert rv.json["data"]["desc"] == event_info_info["desc"]
        assert rv.json["data"]["fields"] == event_info_info["fields"]
        assert rv.json["data"]["speakers"][0]["name"] == speaker_info["name"]
        assert rv.json["data"]["apply"] == []
        assert rv.json["data"]["slide_resources"] == []

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
        testurl = "/cms/api/event/"+str(event_info_info["event_basic_sn"])
        rv = self.test_client.get(testurl)
        # assertion
        assert rv.json["data"]["start_time"] == event_basic_info["start_time"]
        assert rv.json["data"]["end_time"] == event_basic_info["end_time"]
        assert rv.json["data"]["topic_id"] == event_basic_info["topic_sn"]
        assert rv.json["data"]["place_info"]["id"] == event_basic_info["place_sn"]
        assert rv.json["data"]["title"] == event_info_info["title"]
        assert rv.json["data"]["desc"] == event_info_info["desc"]
        assert rv.json["data"]["fields"] == event_info_info["fields"]
        assert rv.json["data"]["speakers"] == []
        assert rv.json["data"]["apply"][0]["host"] == apply_info["host"]
        assert rv.json["data"]["apply"][0]["channel"] == apply_info["channel"]
        assert rv.json["data"]["slide_resources"] == []

    def test_one_event_without_speaker_and_apply(self, topic_info, event_basic_info, place_info):
        event_info_info = {
            "event_basic_sn": None,
            "title": "Flask class 1",
            "desc": "This is description of class 1",
            "fields": [0, 1]
        }
        self._preparation_for_one_event(topic_info, event_basic_info, event_info_info, place_info)

        # test
        testurl = "/cms/api/event/"+str(event_info_info["event_basic_sn"])
        rv = self.test_client.get(testurl)

        # assertion
        assert rv.json["data"]["start_time"] == event_basic_info["start_time"]
        assert rv.json["data"]["end_time"] == event_basic_info["end_time"]
        assert rv.json["data"]["topic_id"] == event_basic_info["topic_sn"]
        assert rv.json["data"]["place_info"]["id"] == event_basic_info["place_sn"]
        assert rv.json["data"]["title"] == event_info_info["title"]
        assert rv.json["data"]["desc"] == event_info_info["desc"]
        assert rv.json["data"]["fields"] == event_info_info["fields"]
        assert rv.json["data"]["speakers"] == []
        assert rv.json["data"]["apply"] == []
        assert rv.json["data"]["slide_resources"] == []


class TestPutEvent:
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
        self._preparation_for_one_event(topic_info, event_basic_info, event_info_info,
                                        place_info, speaker_info)
        putdata = {
            "data": {
                "title": "XXXX",
                "topic_id": event_basic_info["topic_sn"],
                "start_date": "2019-03-09",
                "start_time": "14:00",
                "end_date": "2019-03-09",
                "end_time": "17:00",
                "place_id": event_basic_info["place_sn"],
                "desc": "XXXX",
                "speaker_ids": [1],
                "assistant_ids": [2],
                "field_ids": [1, 2],
                "slide_resource_ids":[1,2,3],
                "apply": [apply_info]
            }
        }

        # test 1
        testurl = "/cms/api/event/"+str(event_info_info["event_basic_sn"])
        rv = self.test_client.put(
            testurl,
            headers={"Content-Type": "application/json"},
            data=json.dumps(putdata),
            content_type="application/json",
        )

        # assertion 1
        assert rv.json["data"]["id"] == event_info_info["event_basic_sn"]

        # test 2
        testurl = "/cms/api/event/"+str(event_info_info["event_basic_sn"])
        rv = self.test_client.get(testurl)

        # assertion 2
        assert rv.json["data"]["start_time"] == putdata["data"]["start_time"]
        assert rv.json["data"]["end_time"] == putdata["data"]["end_time"]
        assert rv.json["data"]["topic_id"] == putdata["data"]["topic_id"]
        assert rv.json["data"]["place_info"]["id"] == putdata["data"]["place_id"]
        assert rv.json["data"]["title"] == putdata["data"]["title"]
        assert rv.json["data"]["desc"] == putdata["data"]["desc"]
        assert rv.json["data"]["fields"] == putdata["data"]["field_ids"]
        assert len(rv.json["data"]["speakers"]) == 1
        assert rv.json["data"]["speakers"][0]["name"] == speaker_info["name"]
        assert rv.json["data"]["assistants"] == []
        assert len(rv.json["data"]["apply"]) == 1
        assert rv.json["data"]["apply"][0]["host"] == apply_info["host"]
        assert rv.json["data"]["apply"][0]["channel"] == apply_info["channel"]
        assert rv.json["data"]["slide_resources"] == []


class TestCreatePlace:
    def setup(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.db.create_all()
        self.test_client = self.app.test_client()

    def teardown(self):
        self.app.db.session.remove()
        self.app.db.drop_all()
        self.app.db.engine.dispose()
        self.app_context.pop()

    def test_success(self):
        place_info = {
            "name": "place 1",
            "addr": "台北市信義區光復南路133號",
            "map": "http://abc.com/map1.html"
        }

        # post
        rv = self.test_client.post(
            "/cms/api/place",
            headers={"Content-Type": "application/json"},
            content_type="application/json",
            data=json.dumps({'data': place_info}),
        )

        # api assertion
        assert rv.status_code == 200
        assert rv.json["info"]["code"] == 0
        assert rv.json["data"]["id"] == 1


class TestPutPlace:
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


    def test_one_place(self, place_info):
        places = {
                "name": "place 1",
                "addr": "台北市信義區光復南路133號",
                "map": "http://abc.com/map1.html",
            }

        # preparation
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            place_sn = manager.create_place(place, autocommit=True)


        putdata = {
            "data": {
                "name": "place 2",
                "addr": "台北市萬華區艋舺大道101號",
                "map": "http://abc.com/map2.html"
            }
        }

        # test 1
        testurl = "/cms/api/place/"+str(place_sn)
        rv = self.test_client.put(
            testurl,
            headers={"Content-Type": "application/json"},
            data=json.dumps(putdata),
            content_type="application/json",
        )

        # api assertion
        assert rv.status_code == 200
        assert rv.json["info"]["code"] == 0


        # test 2
        testurl = "/cms/api/place/"+str(place_sn)
        rv = self.test_client.get(testurl)

        # assertion 2
        assert rv.status_code == 200
        assert rv.json["info"]["code"] == 0
        assert rv.json["data"]["name"] == putdata["data"]["name"]
        assert rv.json["data"]["addr"] == putdata["data"]["addr"]
        assert rv.json["data"]["map"] == putdata["data"]["map"]

class TestGetPlace:
    def setup(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.db.create_all()
        self.test_client = self.app.test_client()

    def teardown(self):
        self.app.db.session.remove()
        self.app.db.drop_all()
        self.app.db.engine.dispose()
        self.app_context.pop()

    def test_get_place(self):

        places = {
                "name": "place 1",
                "addr": "台北市信義區光復南路133號",
                "map": "http://abc.com/map1.html",
         }
        # preparation
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            place_sn = manager.create_place(place, autocommit=True)

        # test
        rv = self.test_client.get("/cms/api/place/"+str(place_sn))

        # assert
        assert rv.json["info"]["code"] == 0
        assert len(rv.json["data"]) == 3
        assert rv.json["data"]["name"] == place["name"]
        assert rv.json["data"]]["addr"] == place["addr"]
        assert rv.json["data"]["id"] == str(place_sn)