import pytest

from app import create_app
from app.sqldb import DBWrapper


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
