# coding=UTF-8

from datetime import datetime, timedelta
import unittest

from sqlalchemy.exc import IntegrityError

from app import create_app
from app.exceptions import PyLadiesException
from app.exceptions import EVENTINFO_NOT_EXIST
from app.sqldb import DBWrapper


class EventInfoTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.db.create_all()

    def tearDown(self):
        self.app.db.session.remove()
        self.app.db.drop_all()
        self.app_context.pop()

    def test_create_event_info_without_speakers_and_slides(self):
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
            "fields": [0, 1]
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_basic = topic.event_basics[0]
            event_info_info["event_basic_sn"] = event_basic.sn

            # test
            manager.create_event_info(event_info_info, autocommit=True)

            # assertion
            event_info_sn = event_basic.event_info.sn
            event_info = manager.get_event_info(event_info_sn)
            self.assertEquals(event_info.title, event_info_info["title"])
            self.assertEquals(event_info.desc, event_info_info["desc"])
            self.assertEquals(event_info.fields, event_info_info["fields"])

    def test_create_event_info_without_slides(self):
        speaker_info_1 = {
            "name": "speaker 1",
            "photo": "https://pyladies.marsw.tw/img/speaker_1_photo.png",
            "title": "Senior Engineer",
            "major_related": True,
            "intro": "",
            "fields": [3]
        }
        speaker_info_2 = {
            "name": "speaker 2",
            "photo": "https://pyladies.marsw.tw/img/speaker_2_photo.png",
            "title": "Senior Engineer",
            "major_related": True,
            "intro": "",
            "fields": [0, 3]
        }
        assistant_info_1 = {
            "name": "speaker 3",
            "photo": "https://pyladies.marsw.tw/img/speaker_3_photo.png",
            "title": "Senior Engineer",
            "major_related": True,
            "intro": "",
            "fields": [3]
        }
        assistant_info_2 = {
            "name": "speaker 4",
            "photo": "https://pyladies.marsw.tw/img/speaker_4_photo.png",
            "title": "Senior Engineer",
            "major_related": True,
            "intro": "",
            "fields": [0, 3]
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
        event_info_info = {
            "event_basic_sn": None,
            "title": "Flask class 1",
            "desc": "This is description of class 1",
            "fields": [0, 1]
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_speaker(speaker_info_1, autocommit=True)
            speaker_1 = manager.get_speaker_by_name(speaker_info_1["name"])
            manager.create_speaker(speaker_info_2, autocommit=True)
            speaker_2 = manager.get_speaker_by_name(speaker_info_2["name"])
            manager.create_speaker(assistant_info_1, autocommit=True)
            assistant_1 = manager.get_speaker_by_name(assistant_info_1["name"])
            manager.create_speaker(assistant_info_2, autocommit=True)
            assistant_2 = manager.get_speaker_by_name(assistant_info_2["name"])
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_basic = topic.event_basics[0]
            event_info_info["event_basic_sn"] = event_basic.sn
            event_info_info["speaker_sns"] = [speaker_1.sn, speaker_2.sn]
            event_info_info["assistant_sns"] = [assistant_1.sn, assistant_2.sn]

            # test
            manager.create_event_info(event_info_info, autocommit=True)

            # assertion
            event_info_sn = event_basic.event_info.sn
            event_info = manager.get_event_info(event_info_sn)
            self.assertEquals(event_info.title, event_info_info["title"])
            self.assertEquals(event_info.desc, event_info_info["desc"])
            self.assertEquals(event_info.fields, event_info_info["fields"])
            self.assertEquals(event_info.speakers[0].name, speaker_info_1["name"])
            self.assertEquals(event_info.speakers[1].name, speaker_info_2["name"])
            self.assertEquals(event_info.assistants[0].name, assistant_info_1["name"])
            self.assertEquals(event_info.assistants[1].name, assistant_info_2["name"])

    def test_create_event_info_with_speakers_and_slides(self):
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
            "title": "Senior Engineer",
            "major_related": True,
            "intro": "",
            "fields": [0, 3]
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
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_speaker(speaker_info, autocommit=True)
            speaker = manager.get_speaker_by_name(speaker_info["name"])
            manager.create_speaker(assistant_info, autocommit=True)
            assistant = manager.get_speaker_by_name(assistant_info["name"])
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_basic = topic.event_basics[0]
            event_info_info["event_basic_sn"] = event_basic.sn
            event_info_info["speaker_sns"] = [speaker.sn]
            event_info_info["assistant_sns"] = [assistant.sn]

            # test
            manager.create_event_info(event_info_info, autocommit=True)

            # assertion
            event_info_sn = event_basic.event_info.sn
            event_info = manager.get_event_info(event_info_sn)
            self.assertEquals(event_info.title, event_info_info["title"])
            self.assertEquals(event_info.desc, event_info_info["desc"])
            self.assertEquals(event_info.fields, event_info_info["fields"])
            self.assertEquals(event_info.speakers[0].name, speaker_info["name"])
            self.assertEquals(event_info.assistants[0].name, assistant_info["name"])
            self.assertEquals(event_info.slide_resources[0].type, slide_resources[0]["type"])
            self.assertEquals(event_info.slide_resources[0].title, slide_resources[0]["title"])
            self.assertEquals(event_info.slide_resources[0].url, slide_resources[0]["url"])
            self.assertEquals(event_info.slide_resources[1].type, slide_resources[1]["type"])
            self.assertEquals(event_info.slide_resources[1].title, slide_resources[1]["title"])
            self.assertEquals(event_info.slide_resources[1].url, slide_resources[1]["url"])

    def test_create_event_info_with_not_exist_event_basic(self):
        event_info_info = {
            "event_basic_sn": 100,
            "title": "Flask class 1",
            "desc": "This is description of class 1",
            "fields": [0, 1]
        }

        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)

            # test & assertion
            with self.assertRaises(IntegrityError) as cm:
                manager.create_event_info(event_info_info, autocommit=True)
            error_msg = str(cm.exception)
            self.assertIn("foreign key", error_msg.lower())

    def test_one_event_basic_one_event_info(self):
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
        event_info_info_1 = {
            "event_basic_sn": None,
            "title": "Flask class 1",
            "desc": "This is description of class 1",
            "fields": [0, 1]
        }
        event_info_info_2 = {
            "event_basic_sn": None,
            "title": "Flask class 2",
            "desc": "This is description of class 2",
            "fields": [0, 1]
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_basic = topic.event_basics[0]
            event_info_info_1["event_basic_sn"] = event_basic.sn
            event_info_info_2["event_basic_sn"] = event_basic.sn

            # test
            manager.create_event_info(event_info_info_1, autocommit=True)

            # assertion
            with self.assertRaises(IntegrityError) as cm:
                manager.create_event_info(event_info_info_2, autocommit=True)
            error_msg = str(cm.exception)
            self.assertIn("duplicate", error_msg.lower())

    def test_update_event_info_without_speakers_and_slides(self):
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
            "fields": [0, 1]
        }
        new_event_info_info = {
            "event_basic_sn": None,
            "title": "Flask class 1-1",
            "desc": "This is description of class 1-1",
            "fields": [0, 1]
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_basic = topic.event_basics[0]
            event_info_info["event_basic_sn"] = event_basic.sn
            new_event_info_info["event_basic_sn"] = event_basic.sn
            manager.create_event_info(event_info_info, autocommit=True)

            # test
            manager.update_event_info(1, new_event_info_info, autocommit=True)

            # assertion
            event_info_sn = event_basic.event_info.sn
            event_info = manager.get_event_info(event_info_sn)
            self.assertEquals(event_info.title, new_event_info_info["title"])
            self.assertEquals(event_info.desc, new_event_info_info["desc"])
            self.assertEquals(event_info.fields, new_event_info_info["fields"])

    def test_update_event_info_with_speakers(self):
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
            "fields": [0, 1]
        }
        new_event_info_info = {
            "event_basic_sn": None,
            "title": "Flask class 1-1",
            "desc": "This is description of class 1-1",
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
        assistant_info = {
            "name": "speaker 2",
            "photo": "https://pyladies.marsw.tw/img/speaker_2_photo.png",
            "title": "Senior Engineer",
            "major_related": True,
            "intro": "",
            "fields": [0, 3]
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_basic = topic.event_basics[0]
            event_info_info["event_basic_sn"] = event_basic.sn
            new_event_info_info["event_basic_sn"] = event_basic.sn
            manager.create_event_info(event_info_info, autocommit=True)

            # test
            manager.create_speaker(speaker_info, autocommit=True)
            speaker = manager.get_speaker_by_name(speaker_info["name"])
            manager.create_speaker(assistant_info, autocommit=True)
            assistant = manager.get_speaker_by_name(assistant_info["name"])
            new_event_info_info["speaker_sns"] = [speaker.sn]
            new_event_info_info["assistant_sns"] = [assistant.sn]
            manager.update_event_info(1, new_event_info_info, autocommit=True)

            # assertion
            event_info_sn = event_basic.event_info.sn
            event_info = manager.get_event_info(event_info_sn)
            self.assertEquals(event_info.title, new_event_info_info["title"])
            self.assertEquals(event_info.desc, new_event_info_info["desc"])
            self.assertEquals(event_info.fields, new_event_info_info["fields"])
            self.assertEquals(event_info.speakers[0].name, speaker_info["name"])
            self.assertEquals(event_info.assistants[0].name, assistant_info["name"])

    def test_change_speakers(self):
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
        assistant_info = {
            "name": "speaker 3",
            "photo": "https://pyladies.marsw.tw/img/speaker_3_photo.png",
            "title": "Senior Engineer",
            "major_related": True,
            "intro": "",
            "fields": [3]
        }
        new_event_info_info = {
            "event_basic_sn": None,
            "title": "Flask class 1",
            "desc": "This is description of class 1",
            "fields": [0, 1]
        }
        new_speaker_info = {
            "name": "speaker 2",
            "photo": "https://pyladies.marsw.tw/img/speaker_2_photo.png",
            "title": "Senior Engineer",
            "major_related": True,
            "intro": "",
            "fields": [0, 3]
        }
        new_assistant_info = {
            "name": "speaker 4",
            "photo": "https://pyladies.marsw.tw/img/speaker_4_photo.png",
            "title": "Senior Engineer",
            "major_related": True,
            "intro": "",
            "fields": [0, 3]
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_basic = topic.event_basics[0]
            event_info_info["event_basic_sn"] = event_basic.sn
            new_event_info_info["event_basic_sn"] = event_basic.sn
            manager.create_speaker(speaker_info, autocommit=True)
            speaker = manager.get_speaker_by_name(speaker_info["name"])
            event_info_info["speaker_sns"] = [speaker.sn]
            manager.create_speaker(assistant_info, autocommit=True)
            assistant = manager.get_speaker_by_name(assistant_info["name"])
            event_info_info["assistant_sns"] = [assistant.sn]
            manager.create_speaker(new_speaker_info, autocommit=True)
            new_speaker = manager.get_speaker_by_name(new_speaker_info["name"])
            new_event_info_info["speaker_sns"] = [new_speaker.sn]
            manager.create_speaker(new_assistant_info, autocommit=True)
            new_assistant = manager.get_speaker_by_name(new_assistant_info["name"])
            new_event_info_info["assistant_sns"] = [new_assistant.sn]
            manager.create_event_info(event_info_info, autocommit=True)

            # test
            manager.update_event_info(1, new_event_info_info, autocommit=True)

            # assertion 1
            event_info = manager.get_event_info(1)
            self.assertEquals(event_info.speakers[0].name, new_speaker_info["name"])
            self.assertEquals(event_info.assistants[0].name, new_assistant_info["name"])

            # assertion 2
            row_count = db_sess.execute("SELECT COUNT(*) FROM speaker").scalar()
            self.assertEquals(row_count, 4)

    def test_change_slides(self):
        slide_resources = [
            {
                "type": "slide",
                "title": "Flask Web Development - class 1",
                "url": "http://tw.pyladies.com/~maomao/1_flask.slides.html#/"
            }
        ]
        new_slide_resources = [
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
        new_event_info_info = {
            "event_basic_sn": None,
            "title": "Flask class 1",
            "desc": "This is description of class 1",
            "fields": [0, 1],
            "slide_resources": new_slide_resources
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_basic = topic.event_basics[0]
            event_info_info["event_basic_sn"] = event_basic.sn
            new_event_info_info["event_basic_sn"] = event_basic.sn
            manager.create_event_info(event_info_info, autocommit=True)

            # test
            manager.update_event_info(1, new_event_info_info, autocommit=True)

            # assertion 1
            event_info = manager.get_event_info(1)
            self.assertEquals(event_info.slide_resources[0].type, new_slide_resources[0]["type"])
            self.assertEquals(event_info.slide_resources[0].title, new_slide_resources[0]["title"])
            self.assertEquals(event_info.slide_resources[0].url, new_slide_resources[0]["url"])

            # assertion 2
            row_count = db_sess.execute("SELECT COUNT(*) FROM slide_resource").scalar()
            self.assertEquals(row_count, 1)

    def test_update_event_info_with_slides(self):
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
        new_event_info_info = {
            "event_basic_sn": None,
            "title": "Flask class 1-1",
            "desc": "This is description of class 1-1",
            "fields": [0, 1],
            "slide_resources": slide_resources
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_basic = topic.event_basics[0]
            event_info_info["event_basic_sn"] = event_basic.sn
            new_event_info_info["event_basic_sn"] = event_basic.sn
            manager.create_event_info(event_info_info, autocommit=True)

            # test
            manager.update_event_info(1, new_event_info_info, autocommit=True)

            # assertion
            event_info_sn = event_basic.event_info.sn
            event_info = manager.get_event_info(event_info_sn)
            self.assertEquals(event_info.title, new_event_info_info["title"])
            self.assertEquals(event_info.desc, new_event_info_info["desc"])
            self.assertEquals(event_info.fields, new_event_info_info["fields"])
            self.assertEquals(event_info.slide_resources[0].type, slide_resources[0]["type"])
            self.assertEquals(event_info.slide_resources[0].title, slide_resources[0]["title"])
            self.assertEquals(event_info.slide_resources[0].url, slide_resources[0]["url"])
            self.assertEquals(event_info.slide_resources[1].type, slide_resources[1]["type"])
            self.assertEquals(event_info.slide_resources[1].title, slide_resources[1]["title"])
            self.assertEquals(event_info.slide_resources[1].url, slide_resources[1]["url"])

    def test_delete_event_info(self):
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
            "title": "Senior Engineer",
            "major_related": True,
            "intro": "",
            "fields": [0, 3]
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_basic = topic.event_basics[0]
            event_info_info["event_basic_sn"] = event_basic.sn
            manager.create_speaker(speaker_info, autocommit=True)
            speaker = manager.get_speaker_by_name(speaker_info["name"])
            manager.create_speaker(assistant_info, autocommit=True)
            assistant = manager.get_speaker_by_name(assistant_info["name"])
            event_info_info["speaker_sns"] = [speaker.sn]
            event_info_info["assistant_sns"] = [assistant.sn]
            manager.create_event_info(event_info_info, autocommit=True)
            event_info_sn = event_basic.event_info.sn

            # test
            manager.delete_event_info(event_info_sn, autocommit=True)

            # assertion 1
            with self.assertRaises(PyLadiesException) as cm:
                manager.get_event_info(event_info_sn)
            self.assertEquals(cm.exception, EVENTINFO_NOT_EXIST)

            # assertion 2
            row_count = db_sess.execute("SELECT COUNT(*) FROM speaker").scalar()
            self.assertEquals(row_count, 2)
            row_count = db_sess.execute("SELECT COUNT(*) FROM slide_resource").scalar()
            self.assertEquals(row_count, 0)

    def test_delete_event_basic(self):
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
            "fields": [0, 1]
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            event_basic_info["topic_sn"] = 1
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_info_info["event_basic_sn"] = 1
            manager.create_event_info(event_info_info, autocommit=True)

            # test
            manager.delete_event_basic(1, autocommit=True)

            # assertion
            with self.assertRaises(PyLadiesException) as cm:
                manager.get_event_info(1)
            self.assertEquals(cm.exception, EVENTINFO_NOT_EXIST)

    def test_delete_topic(self):
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
            "fields": [0, 1]
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            event_basic_info["topic_sn"] = 1
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_info_info["event_basic_sn"] = 1
            manager.create_event_info(event_info_info, autocommit=True)

            # test
            manager.delete_topic(1, autocommit=True)

            # assertion
            with self.assertRaises(PyLadiesException) as cm:
                manager.get_event_info(1)
            self.assertEquals(cm.exception, EVENTINFO_NOT_EXIST)

    def test_delete_speaker(self):
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
            "fields": [0, 1]
        }
        speaker_info_1 = {
            "name": "speaker 1",
            "photo": "https://pyladies.marsw.tw/img/speaker_1_photo.png",
            "title": "Senior Engineer",
            "major_related": True,
            "intro": "",
            "fields": [3]
        }
        speaker_info_2 = {
            "name": "speaker 2",
            "photo": "https://pyladies.marsw.tw/img/speaker_2_photo.png",
            "title": "Senior Engineer",
            "major_related": True,
            "intro": "",
            "fields": [0, 3]
        }
        assistant_info_1 = {
            "name": "speaker 3",
            "photo": "https://pyladies.marsw.tw/img/speaker_3_photo.png",
            "title": "Senior Engineer",
            "major_related": True,
            "intro": "",
            "fields": [3]
        }
        assistant_info_2 = {
            "name": "speaker 4",
            "photo": "https://pyladies.marsw.tw/img/speaker_4_photo.png",
            "title": "Senior Engineer",
            "major_related": True,
            "intro": "",
            "fields": [0, 3]
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_basic = topic.event_basics[0]
            event_info_info["event_basic_sn"] = event_basic.sn
            manager.create_speaker(speaker_info_1, autocommit=True)
            speaker_1 = manager.get_speaker_by_name(speaker_info_1["name"])
            manager.create_speaker(speaker_info_2, autocommit=True)
            speaker_2 = manager.get_speaker_by_name(speaker_info_2["name"])
            event_info_info["speaker_sns"] = [speaker_1.sn, speaker_2.sn]
            manager.create_speaker(assistant_info_1, autocommit=True)
            assistant_1 = manager.get_speaker_by_name(assistant_info_1["name"])
            manager.create_speaker(assistant_info_2, autocommit=True)
            assistant_2 = manager.get_speaker_by_name(assistant_info_2["name"])
            event_info_info["assistant_sns"] = [assistant_1.sn, assistant_2.sn]
            manager.create_event_info(event_info_info, autocommit=True)
            event_info_sn = event_basic.event_info.sn

            # test
            manager.delete_speaker(speaker_1.sn, autocommit=True)
            manager.delete_speaker(assistant_1.sn, autocommit=True)

            # assertion 1
            event_info = manager.get_event_info(event_info_sn)
            self.assertEquals(event_info.speakers[0].name, speaker_info_2["name"])
            self.assertEquals(event_info.assistants[0].name, assistant_info_2["name"])

            # assertion 2
            row_count = db_sess.execute("SELECT COUNT(*) FROM speaker").scalar()
            self.assertEquals(row_count, 2)

    def test_get_event_info_by_sn(self):
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
            "fields": [0, 1]
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_basic = topic.event_basics[0]
            event_info_info["event_basic_sn"] = event_basic.sn
            manager.create_event_info(event_info_info, autocommit=True)
            event_info_sn = event_basic.event_info.sn

            # test & assertion 1
            event_info = manager.get_event_info(event_info_sn)
            self.assertEquals(event_info.title, event_info_info["title"])
            self.assertEquals(event_info.desc, event_info_info["desc"])
            self.assertEquals(event_info.fields, event_info_info["fields"])

            # test & assertion 2
            with self.assertRaises(PyLadiesException) as cm:
                not_exist_event_info_sn = event_info_sn + 1
                manager.get_event_info(not_exist_event_info_sn)
            self.assertEquals(cm.exception, EVENTINFO_NOT_EXIST)

    def test_get_event_info_by_event_basic(self):
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
            "fields": [0, 1]
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_basic = topic.event_basics[0]
            event_info_info["event_basic_sn"] = event_basic.sn

            # test
            manager.create_event_info(event_info_info, autocommit=True)

            # assertion
            self.assertEquals(event_basic.event_info.title, event_info_info["title"])
            self.assertEquals(event_basic.event_info.desc, event_info_info["desc"])
            self.assertEquals(event_basic.event_info.fields, event_info_info["fields"])

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
