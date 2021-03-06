# coding=UTF-8

import json
import copy
from datetime import datetime, timedelta

from flask import session
import pytest
from werkzeug.security import generate_password_hash

from app import create_app
from app.constant import DEFAULT_PLACE_ID
from app.exceptions import PLACE_NAME_DUPLICATE, EVENTBASIC_NOT_EXIST, OK, TOPIC_ASSOCIATED_WITH_EXISTED_EVENT
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

        payload = {
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
        # preparation
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            manager.create_place(place_info, autocommit=True)
            manager.create_speaker(speaker_info, autocommit=True)
            manager.create_speaker(assistant_info, autocommit=True)

            topic = manager.get_topic_by_name(topic_info["name"])
            place = manager.get_place_by_name(place_info["name"])
            payload["topic_id"] = topic.id
            payload["place_id"] = place.id

        # post test
        rv = self.test_client.post(
            "/cms/api/event",
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
            content_type="application/json",
        )
        # api assertion
        assert rv.status_code == 200
        assert rv.json["info"]["code"] == OK.code
        assert rv.json["data"]["id"] == 1
        event_basic_id = rv.json["data"]["id"]

        # event assertion
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            event_basic = manager.get_event_basic(event_basic_id)
            assert event_basic.topic.name == topic_info["name"]
            assert event_basic.place.name == place_info["name"]
            assert event_basic.place.map == place_info["map"]
            assert event_basic.date == payload["start_date"]
            assert event_basic.start_time == payload["start_time"]
            assert event_basic.end_time == payload["end_time"]


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
            topic_id = manager.create_topic(topic_info, autocommit=True)
            place_id = manager.create_place(place, autocommit=True)
            if speaker:
                speaker_id = manager.create_speaker(speaker, autocommit=True)
            else:
                speaker_id = None
            for event_basic_info, event_info in \
                    zip(event_basic_infos, event_infos):
                event_basic_info['topic_id'] = topic_id
                event_basic_info['place_id'] = place_id
                event_basic_id = manager.create_event_basic(event_basic_info, autocommit=True)
                if apply:
                    apply["event_basic_id"] = event_basic_id
                    manager.create_event_apply(apply, autocommit=True)
                event_info['event_basic_id'] = event_basic_id
                event_info["speaker_ids"] = [speaker_id]
                manager.create_event_info(event_info, autocommit=True)

    def test_one_event(self, event_info, speaker_info, topic_info, event_basic_info, place_info, apply_info):
        event_apply_info = {
            "event_basic_id": None,
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
            "id": event_info["event_basic_id"],
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
            "event_basic_id": None,
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
            "event_basic_id": None,
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
                "id": event_infos[i]["event_basic_id"],
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
            "event_basic_id": None,
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
                "addr": "??????????????????????????????133???",
                "map": "http://abc.com/map1.html",
            },
            {
                "name": "place 2",
                "addr": "??????????????????????????????101???",
                "map": "http://abc.com/map2.html",
            },
            {
                "name": "place 3",
                "addr": "????????????????????????????????????50???",
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
            "title": "Dive into Pinkoi 2013 ???????????????",
            "type": "slide",
            "url": "https://speakerdeck.com/mosky/dive-into-pinkoi-2013"
        }
        slide_2 = {
            "title": "ihower ??? Git ??????",
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
        assert rv.json["data"][0]["title"] == "Dive into Pinkoi 2013 ???????????????"
        assert rv.json["data"][0]["url"] == "https://speakerdeck.com/mosky/dive-into-pinkoi-2013"
        assert rv.json["data"][1]["id"] == 2
        assert rv.json["data"][1]["type"] == "resource"
        assert rv.json["data"][1]["title"] == "ihower ??? Git ??????"
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

        # assert
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

        assert rv.json["info"]["code"] == 0
        assert len(rv.json["data"]) == 3
        assert rv.json["data"][0]["name"] == topic_infos[0]["name"]
        assert rv.json["data"][1]["name"] == topic_infos[1]["name"]
        assert rv.json["data"][2]["name"] == topic_infos[2]["name"]


class TestGetTopic:
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

    def test_get_topic(self, topic_info):
        # preparation
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])

        # test
        testurl = "/cms/api/topic/"+str(topic.id)
        rv = self.test_client.get(testurl)

        assert rv.json["data"]["name"] == topic_info["name"]
        assert rv.json["data"]["desc"] == topic_info["desc"]
        assert rv.json["data"]["freq"] == topic_info["freq"]
        assert rv.json["data"]["level"] == topic_info["level"]
        assert rv.json["data"]["host"] == topic_info["host"]
        assert rv.json["data"]["fields"] == topic_info["fields"]


class TestCreateTopic:
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

    def test_create_topic(self, topic_info):

        # test 1
        rv = self.test_client.post(
            "/cms/api/topic",
            headers={"Content-Type": "application/json"},
            content_type="application/json",
            data=json.dumps({"data": topic_info})
        )

        # api assertion
        assert rv.status_code == 200
        assert rv.json["info"]["code"] == 0
        assert rv.json["data"]["id"] == 1

        # test 2
        test_url = "/cms/api/topic/1"
        rv = self.test_client.get(test_url)

        # assertion 2
        assert rv.status_code == 200
        assert rv.json["info"]["code"] == 0
        assert rv.json["data"]["name"] == topic_info["name"]
        assert rv.json["data"]["desc"] == topic_info["desc"]
        assert rv.json["data"]["freq"] == topic_info["freq"]
        assert rv.json["data"]["level"] == topic_info["level"]
        assert rv.json["data"]["host"] == topic_info["host"]
        assert rv.json["data"]["fields"] == topic_info["fields"]


class TestPutTopic:
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

    def test_put_topic(self, topic_info):
        # preparation
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])

        put_data = {
            "name": "New topic 1",
            "desc": "This is new topic 1",
            "freq": 1,
            "level": 1,
            "host": 1,
            "fields": [1],
        }

        # test 1
        test_url = "/cms/api/topic/" + str(topic.id)
        rv = self.test_client.put(
            test_url,
            headers={"Content-Type": "application/json"},
            content_type="application/json",
            data=json.dumps({"data": put_data})
        )

        # api assertion
        assert rv.status_code == 200
        assert rv.json["info"]["code"] == 0

        # test 2
        test_url = "/cms/api/topic/" + str(topic.id)
        rv = self.test_client.get(test_url)

        # assertion 2
        assert rv.status_code == 200
        assert rv.json["info"]["code"] == 0
        assert rv.json["data"]["name"] == put_data["name"]
        assert rv.json["data"]["desc"] == put_data["desc"]
        assert rv.json["data"]["freq"] == put_data["freq"]
        assert rv.json["data"]["level"] == put_data["level"]
        assert rv.json["data"]["host"] == put_data["host"]
        assert rv.json["data"]["fields"] == put_data["fields"]



class TestDeleteTopic:
    def setup(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.db.create_all()
        self.test_client = self.app.test_client()
        self.create_default_place()

    def teardown(self):
        self.app.db.session.remove()
        self.app.db.drop_all()
        self.app_context.pop()

    def create_default_place(self):
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            place_info = {
                "id": DEFAULT_PLACE_ID,
                "name": "default place",
                "addr": "default place addr",
                "map": "default place map",
            }
            manager.create_place(place_info, autocommit=True)

    def test_delete_not_exist_topic(self):
        testurl = "/cms/api/topic/1234"
        rv = self.test_client.delete(testurl)
        assert rv.json["info"]["code"] == 0

    def test_delete_one_topic(self, topic_info):
        # preparation
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])

            testurl = "/cms/api/topic/"+str(topic.id)
            rv = self.test_client.get(testurl)
            assert rv.json["data"]

            rv = self.test_client.delete(testurl)
            assert rv.json["info"]["code"] == 0

    def test_delete_topic_has_event(self, topic_info, event_basic_info, event_info):
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_id"] = topic.id
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_info["event_basic_id"] = topic.event_basics[0].id
            manager.create_event_info(event_info, autocommit=True)

            # test
            testurl = "/cms/api/topic/" + str(topic.id)
            rv = self.test_client.get(testurl)
            assert rv.json["data"]

            rv = self.test_client.delete(testurl)
            assert rv.json["info"]["code"] == TOPIC_ASSOCIATED_WITH_EXISTED_EVENT.code


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
            "password_hash": generate_password_hash(login_info["password"], method="pbkdf2:sha1"),
            "mail": login_info["mail"],
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            obj = User(**user_info)
            db_sess.add(obj)
            db_sess.commit()

    def test_invalid_input(self):
        login_info = {
            "username": "pyladies",
            "password": "",
            "mail": "ut@pyladies.com",
        }

        rv = self.test_client.post("/cms/api/login", json=login_info)

        assert rv.json["info"]["code"] == 1

    def test_user_not_exist(self):
        login_info = {
            "username": "pyladies",
            "password": "test123456",
            "mail": "ut@pyladies.com",
        }

        rv = self.test_client.post("/cms/api/login", json=login_info)

        assert rv.json["info"]["code"] == 1701

    def test_wrong_password(self):
        login_info = {
            "username": "pyladies",
            "password": "test123456",
            "mail": "ut@pyladies.com",
        }
        self.create_new_user(login_info)

        login_info["password"] = "12345678"
        rv = self.test_client.post("/cms/api/login", json=login_info)

        assert rv.json["info"]["code"] == 1701

    def test_success(self):
        login_info = {
            "username": "pyladies",
            "password": "test123456",
            "mail": "ut@pyladies.com",
        }
        self.create_new_user(login_info)

        with self.test_client as c:
            rv = c.post("/cms/api/login", json=login_info)

            assert rv.json["info"]["code"] == 0
            assert session['user_type'] == 'Admin'


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
            "password_hash": generate_password_hash(login_info["password"], method="pbkdf2:sha1"),
            "mail": login_info["mail"],
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
            "password": "test123456",
            "mail": "ut@pyladies.com",
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
            topic_id = manager.create_topic(topic, autocommit=True)
            place_id = manager.create_place(place, autocommit=True)
            event_basic.update({
                "topic_id": topic_id,
                "place_id": place_id
            })
            event_basic_id = manager.create_event_basic(event_basic, autocommit=True)
            event_info["event_basic_id"] = event_basic_id
            if speaker:
                speaker_id = manager.create_speaker(speaker, autocommit=True)
                event_info["speaker_ids"] = [speaker_id]
            manager.create_event_info(event_info, autocommit=True)
            if apply:
                apply["event_basic_id"] = event_basic_id
                manager.create_event_apply(apply, autocommit=True)

    def test_one_event(self, topic_info, event_basic_info, place_info, apply_info):
        event_info_info = {
            "event_basic_id": None,
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
            "event_basic_id": None,
            "apply": [apply_info]
        }
        self._preparation_for_one_event(topic_info, event_basic_info, event_info_info,
                                        place_info, speaker_info, event_apply_info)

        # test
        testurl = "/cms/api/event/" + str(event_info_info["event_basic_id"])
        rv = self.test_client.get(testurl)

        # assertion
        assert rv.json["data"]["start_time"] == event_basic_info["start_time"]
        assert rv.json["data"]["end_time"] == event_basic_info["end_time"]
        assert rv.json["data"]["topic_id"] == event_basic_info["topic_id"]
        assert rv.json["data"]["place_info"]["id"] == event_basic_info["place_id"]
        assert rv.json["data"]["title"] == event_info_info["title"]
        assert rv.json["data"]["desc"] == event_info_info["desc"]
        assert rv.json["data"]["fields"] == event_info_info["fields"]
        assert rv.json["data"]["speakers"][0]["name"] == speaker_info["name"]
        assert rv.json["data"]["apply"][0]["host"] == apply_info["host"]
        assert rv.json["data"]["apply"][0]["channel"] == apply_info["channel"]
        assert rv.json["data"]["slide_resources"] == []

    def test_one_event_without_apply(self, topic_info, event_basic_info, place_info):
        event_info_info = {
            "event_basic_id": None,
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
        testurl = "/cms/api/event/" + str(event_info_info["event_basic_id"])
        rv = self.test_client.get(testurl)

        # assertion
        assert rv.json["data"]["start_time"] == event_basic_info["start_time"]
        assert rv.json["data"]["end_time"] == event_basic_info["end_time"]
        assert rv.json["data"]["topic_id"] == event_basic_info["topic_id"]
        assert rv.json["data"]["place_info"]["id"] == event_basic_info["place_id"]
        assert rv.json["data"]["title"] == event_info_info["title"]
        assert rv.json["data"]["desc"] == event_info_info["desc"]
        assert rv.json["data"]["fields"] == event_info_info["fields"]
        assert rv.json["data"]["speakers"][0]["name"] == speaker_info["name"]
        assert rv.json["data"]["apply"] == []
        assert rv.json["data"]["slide_resources"] == []

    def test_one_event_without_speaker(self, topic_info, event_basic_info, place_info, apply_info):
        event_info_info = {
            "event_basic_id": None,
            "title": "Flask class 1",
            "desc": "This is description of class 1",
            "fields": [0, 1]
        }
        event_apply_info = {
            "event_basic_id": None,
            "apply": [apply_info]
        }
        self._preparation_for_one_event(topic_info, event_basic_info, event_info_info,
                                        place_info, None, event_apply_info)

        # test
        testurl = "/cms/api/event/" + str(event_info_info["event_basic_id"])
        rv = self.test_client.get(testurl)
        # assertion
        assert rv.json["data"]["start_time"] == event_basic_info["start_time"]
        assert rv.json["data"]["end_time"] == event_basic_info["end_time"]
        assert rv.json["data"]["topic_id"] == event_basic_info["topic_id"]
        assert rv.json["data"]["place_info"]["id"] == event_basic_info["place_id"]
        assert rv.json["data"]["title"] == event_info_info["title"]
        assert rv.json["data"]["desc"] == event_info_info["desc"]
        assert rv.json["data"]["fields"] == event_info_info["fields"]
        assert rv.json["data"]["speakers"] == []
        assert rv.json["data"]["apply"][0]["host"] == apply_info["host"]
        assert rv.json["data"]["apply"][0]["channel"] == apply_info["channel"]
        assert rv.json["data"]["slide_resources"] == []

    def test_one_event_without_speaker_and_apply(self, topic_info, event_basic_info, place_info):
        event_info_info = {
            "event_basic_id": None,
            "title": "Flask class 1",
            "desc": "This is description of class 1",
            "fields": [0, 1]
        }
        self._preparation_for_one_event(topic_info, event_basic_info, event_info_info, place_info)

        # test
        testurl = "/cms/api/event/" + str(event_info_info["event_basic_id"])
        rv = self.test_client.get(testurl)

        # assertion
        assert rv.json["data"]["start_time"] == event_basic_info["start_time"]
        assert rv.json["data"]["end_time"] == event_basic_info["end_time"]
        assert rv.json["data"]["topic_id"] == event_basic_info["topic_id"]
        assert rv.json["data"]["place_info"]["id"] == event_basic_info["place_id"]
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
            topic_id = manager.create_topic(topic, autocommit=True)
            place_id = manager.create_place(place, autocommit=True)
            event_basic.update({
                "topic_id": topic_id,
                "place_id": place_id
            })
            event_basic_id = manager.create_event_basic(event_basic, autocommit=True)
            event_info["event_basic_id"] = event_basic_id
            if speaker:
                speaker_id = manager.create_speaker(speaker, autocommit=True)
                event_info["speaker_ids"] = [speaker_id]
            manager.create_event_info(event_info, autocommit=True)
            if apply:
                apply["event_basic_id"] = event_basic_id
                manager.create_event_apply(apply, autocommit=True)

    def test_one_event(self, topic_info, event_basic_info, place_info, apply_info):
        event_info_info = {
            "event_basic_id": None,
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
        payload = {
            "title": "XXXX",
            "topic_id": event_basic_info["topic_id"],
            "start_date": "2019-03-09",
            "start_time": "14:00",
            "end_date": "2019-03-09",
            "end_time": "17:00",
            "place_id": event_basic_info["place_id"],
            "desc": "XXXX",
            "speaker_ids": [1],
            "assistant_ids": [2],
            "field_ids": [1, 2],
            "slide_resource_ids": [1, 2, 3],
            "apply": [apply_info]
        }

        # test 1
        test_url = "/cms/api/event/{e_id}".format(e_id=event_info_info["event_basic_id"])
        rv = self.test_client.put(
            test_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
            content_type="application/json",
        )
        print('#' * 50, rv.json)

        # assertion 1
        assert rv.json["data"]["id"] == event_info_info["event_basic_id"]

        # test 2
        rv = self.test_client.get(test_url)

        # assertion 2
        assert rv.json["data"]["start_time"] == payload["start_time"]
        assert rv.json["data"]["end_time"] == payload["end_time"]
        assert rv.json["data"]["topic_id"] == payload["topic_id"]
        assert rv.json["data"]["place_info"]["id"] == payload["place_id"]
        assert rv.json["data"]["title"] == payload["title"]
        assert rv.json["data"]["desc"] == payload["desc"]
        assert rv.json["data"]["fields"] == payload["field_ids"]
        assert len(rv.json["data"]["speakers"]) == 1
        assert rv.json["data"]["speakers"][0]["name"] == speaker_info["name"]
        assert rv.json["data"]["assistants"] == []
        assert len(rv.json["data"]["apply"]) == 1
        assert rv.json["data"]["apply"][0]["host"] == apply_info["host"]
        assert rv.json["data"]["apply"][0]["channel"] == apply_info["channel"]
        assert rv.json["data"]["slide_resources"] == []


class TestDeleteEvent:
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
            topic_id = manager.create_topic(topic, autocommit=True)
            place_id = manager.create_place(place, autocommit=True)
            event_basic.update({
                "topic_id": topic_id,
                "place_id": place_id
            })
            event_basic_id = manager.create_event_basic(event_basic, autocommit=True)
            event_info["event_basic_id"] = event_basic_id
            if speaker:
                speaker_id = manager.create_speaker(speaker, autocommit=True)
                event_info["speaker_ids"] = [speaker_id]
            manager.create_event_info(event_info, autocommit=True)
            if apply:
                apply["event_basic_id"] = event_basic_id
                manager.create_event_apply(apply, autocommit=True)

    def test_one_event(self, topic_info, event_basic_info, place_info, apply_info):
        # preparation
        event_info_info = {
            "event_basic_id": None,
            "title": "Flask class 1",
            "desc": "This is description of class 1",
            "fields": [0, 1]
        }
        self._preparation_for_one_event(topic_info, event_basic_info, event_info_info,
                                        place_info)

        testurl = "/cms/api/event/" + str(event_info_info["event_basic_id"])
        rv = self.test_client.get(testurl)
        assert rv.json["info"]["code"] == 0
        assert rv.json["data"]

        # test
        rv = self.test_client.delete(testurl)

        # assertion
        assert rv.json["info"]["code"] == 0
        rv = self.test_client.get(testurl)
        assert rv.json["info"]["code"] == EVENTBASIC_NOT_EXIST.code

    def test_no_event(self):
        testurl = "/cms/api/event/1234"
        rv = self.test_client.get(testurl)
        assert rv.json["info"]["code"] == EVENTBASIC_NOT_EXIST.code

        rv = self.test_client.delete(testurl)
        assert rv.json["info"]["code"] == 0


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
            "addr": "??????????????????????????????133???",
            "map": "http://abc.com/map1.html"
        }

        # test 1
        rv = self.test_client.post(
            "/cms/api/place",
            headers={"Content-Type": "application/json"},
            content_type="application/json",
            data=json.dumps(place_info),
        )

        # api assertion
        assert rv.status_code == 200
        assert rv.json["info"]["code"] == 0
        assert rv.json["data"]["id"] == 1

        # test 2
        test_url = "/cms/api/place/1"
        rv = self.test_client.get(test_url)

        # assertion 2
        assert rv.status_code == 200
        assert rv.json["info"]["code"] == 0
        assert rv.json["data"]["name"] == place_info["name"]
        assert rv.json["data"]["addr"] == place_info["addr"]
        assert rv.json["data"]["map"] == place_info["map"]

    def test_duplicate_place_name(self):
        # preparation
        place_info = {
            "name": "place 1",
            "addr": "??????????????????????????????133???",
            "map": "http://abc.com/map1.html"
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            manager.create_place(place_info, autocommit=True)

        # test
        place_info_2 = {
            "name": "place 1",
            "addr": "??????????????????????????????134???",
            "map": "http://abc.com/map2.html"
        }
        rv = self.test_client.post(
            "/cms/api/place",
            headers={"Content-Type": "application/json"},
            content_type="application/json",
            data=json.dumps(place_info_2),
        )

        # assertion
        assert rv.status_code == 200
        assert rv.json["info"]["code"] == PLACE_NAME_DUPLICATE.code


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
        # preparation
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            place_id = manager.create_place(place_info, autocommit=True)

        payload = {
            "name": "place 2",
            "addr": "??????????????????????????????101???",
            "map": "http://abc.com/map2.html"
        }

        # test 1
        test_url = "/cms/api/place/{place_id}".format(place_id=place_id)
        rv = self.test_client.put(
            test_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
            content_type="application/json",
        )

        # api assertion
        assert rv.status_code == 200
        assert rv.json["info"]["code"] == OK.code

        rv = self.test_client.get(test_url)

        # assertion 2
        assert rv.status_code == 200
        assert rv.json["info"]["code"] == OK.code
        assert rv.json["data"]["name"] == payload["name"]
        assert rv.json["data"]["addr"] == payload["addr"]
        assert rv.json["data"]["map"] == payload["map"]

    def test_duplicate_place_name(self):
        # preparation
        place_info = {
            "name": "place 1",
            "addr": "??????????????????????????????133???",
            "map": "http://abc.com/map1.html"
        }
        place_info_2 = {
            "name": "place 2",
            "addr": "??????????????????????????????134???",
            "map": "http://abc.com/map2.html"
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            manager.create_place(place_info, autocommit=True)
            place_id = manager.create_place(place_info_2, autocommit=True)

        payload = {
            **place_info_2.copy(),
            "name": place_info["name"]
        }

        test_url = "/cms/api/place/{place_id}".format(place_id=place_id)
        rv = self.test_client.put(
            test_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
            content_type="application/json",
        )

        # assertion
        assert rv.status_code == 200
        assert rv.json["info"]["code"] == PLACE_NAME_DUPLICATE.code


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
        place = {
            "name": "place 1",
            "addr": "??????????????????????????????133???",
            "map": "http://abc.com/map1.html",
        }
        # preparation
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            place_id = manager.create_place(place, autocommit=True)

        # test
        rv = self.test_client.get("/cms/api/place/" + str(place_id))

        # assert
        assert rv.json["info"]["code"] == 0
        assert len(rv.json["data"]) == 4
        assert rv.json["data"]["id"] == place_id
        assert rv.json["data"]["name"] == place["name"]
        assert rv.json["data"]["addr"] == place["addr"]
        assert rv.json["data"]["map"] == place["map"]

class TestCreateSpeaker:
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

    def test_create_speaker(self, speaker_info):

        # test 1
        rv = self.test_client.post(
            "/cms/api/speaker",
            headers={"Content-Type": "application/json"},
            content_type="application/json",
            data=json.dumps({"data": speaker_info})
        )

        # api assertion
        assert rv.status_code == 200
        assert rv.json["info"]["code"] == 0
        assert rv.json["data"]["id"] == 1

        # test 2
        test_url = "/cms/api/speaker/1"
        rv = self.test_client.get(test_url)

        # assertion 2
        assert rv.status_code == 200
        assert rv.json["info"]["code"] == 0
        assert rv.json["data"]["name"] == speaker_info["name"]
        assert rv.json["data"]["photo"] == speaker_info["photo"]
        assert rv.json["data"]["title"] == speaker_info["title"]
        assert rv.json["data"]["major_related"] == speaker_info["major_related"]
        assert rv.json["data"]["intro"] == speaker_info["intro"]
        assert rv.json["data"]["fields"] == speaker_info["fields"]
        assert rv.json["data"]["links"] == speaker_info["links"]

class TestGetSpeaker:
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

    def test_get_speaker(self, speaker_info):

        speaker = copy.deepcopy(speaker_info)
        # preparation
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            manager.create_speaker(speaker, autocommit=True)

        # test
        rv = self.test_client.get("/cms/api/speaker/1")

        #assert
        assert rv.json["info"]["code"] == 0
        assert rv.json["data"]["name"] == speaker_info["name"]
        assert rv.json["data"]["photo"] == speaker_info["photo"]
        assert rv.json["data"]["title"] == speaker_info["title"]
        assert rv.json["data"]["major_related"] == speaker_info["major_related"]
        assert rv.json["data"]["intro"] == speaker_info["intro"]
        assert rv.json["data"]["fields"] == speaker_info["fields"]
        assert rv.json["data"]["links"] == speaker_info["links"]

class TestPutSpeaker:
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

    def test_put_speaker(self, speaker_info):
        # preparation
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            speaker_id = manager.create_speaker(speaker_info, autocommit=True)

        put_data = {
            "name": "speaker 2",
            "photo": "https://pyladies.marsw.tw/img/speaker_2_photo.png",
            "title": "Senior Engineer",
            "major_related": True,
            "intro": "introduction",
            "fields": [4],
            "links": [{"type": "GitHub", "url": "http://github.com/speaker2"}]
        }

        # test 1
        test_url = "/cms/api/speaker/" + str(speaker_id)
        rv = self.test_client.put(
            test_url,
            headers={"Content-Type": "application/json"},
            content_type="application/json",
            data=json.dumps({"data": put_data})
        )

        # api assertion
        assert rv.status_code == 200
        assert rv.json["info"]["code"] == 0

        # test 2
        test_url = "/cms/api/speaker/" + str(speaker_id)
        rv = self.test_client.get(test_url)
        print(rv.json)

        # assertion 2
        assert rv.status_code == 200
        assert rv.json["info"]["code"] == 0
        assert rv.json["data"]["name"] == put_data["name"]
        assert rv.json["data"]["photo"] == put_data["photo"]
        assert rv.json["data"]["title"] == put_data["title"]
        assert rv.json["data"]["major_related"] == put_data["major_related"]
        assert rv.json["data"]["intro"] == put_data["intro"]
        assert rv.json["data"]["fields"] == put_data["fields"]
        assert rv.json["data"]["links"] == put_data["links"]

class TestDeleteSpeaker:
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

    def test_delete_speaker(self, speaker_info):
        # preparation
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            manager.create_speaker(speaker_info, autocommit=True)

        # test
        rv = self.test_client.delete("/cms/api/speaker/1")

        #assert
        assert rv.json["info"]["code"] == 0
