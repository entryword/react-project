import unittest

from sqlalchemy.exc import IntegrityError

from app import create_app
from app.exceptions import PyLadiesException
from app.exceptions import SPEAKER_NOT_EXIST
from app.sqldb import DBWrapper


class SpeakerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.db.create_all()

    def tearDown(self):
        self.app.db.session.remove()
        self.app.db.drop_all()
        self.app_context.pop()

    def test_create_speaker_without_link(self):
        info = {
            "name": "speaker 1",
            "photo": "https://pyladies.marsw.tw/img/speaker_1_photo.png",
            "title": "Senior Engineer",
            "major_related": True,
            "intro": "",
            "fields": [3]
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)

            # test
            manager.create_speaker(info, autocommit=True)

            # assertion
            speaker = manager.get_speaker_by_name(info["name"])
            self.assertEqual(speaker.name, info["name"])
            self.assertEqual(speaker.photo, info["photo"])
            self.assertEqual(speaker.title, info["title"])
            self.assertEqual(speaker.major_related, info["major_related"])
            self.assertEqual(speaker.intro, info["intro"])
            self.assertEqual(speaker.fields, info["fields"])
            self.assertEqual(speaker.links, [])

    def test_create_speaker_with_link(self):
        links = [
            {
                "type": "github",
                "url": "https://github.com/speaker_1"
            },
            {
                "type": "linkedin",
                "url": "https://tw.linkedin.com/speaker_1"
            }
        ]
        info = {
            "name": "speaker 1",
            "photo": "https://pyladies.marsw.tw/img/speaker_1_photo.png",
            "title": "Senior Engineer",
            "major_related": True,
            "intro": "",
            "fields": [3],
            "links": links
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)

            # test
            manager.create_speaker(info, autocommit=True)

            # assertion
            speaker = manager.get_speaker_by_name(info["name"])
            self.assertEqual(speaker.name, info["name"])
            self.assertEqual(speaker.photo, info["photo"])
            self.assertEqual(speaker.title, info["title"])
            self.assertEqual(speaker.major_related, info["major_related"])
            self.assertEqual(speaker.intro, info["intro"])
            self.assertEqual(speaker.fields, info["fields"])
            self.assertEqual(speaker.links[0].type, links[0]["type"])
            self.assertEqual(speaker.links[0].url, links[0]["url"])
            self.assertEqual(speaker.links[1].type, links[1]["type"])
            self.assertEqual(speaker.links[1].url, links[1]["url"])

    def test_unique_speaker_name(self):
        info_1 = {
            "name": "speaker 1",
            "photo": "https://pyladies.marsw.tw/img/speaker_1_photo.png",
            "title": "Senior Engineer",
            "major_related": True,
            "intro": "",
            "fields": [3]
        }
        info_2 = {
            "name": "speaker 1",
            "title": "Engineer",
            "major_related": True,
            "fields": [1, 2]
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)

            # test
            manager.create_speaker(info_1, autocommit=True)

            # assertion
            with self.assertRaises(IntegrityError) as cm:
                manager.create_speaker(info_2, autocommit=True)
            error_msg = str(cm.exception)
            self.assertIn("duplicate", error_msg.lower())

    def test_update_speaker_with_same_speaker_name(self):
        info = {
            "name": "speaker 1",
            "photo": "https://pyladies.marsw.tw/img/speaker_1_photo.png",
            "title": "Senior Engineer",
            "major_related": True,
            "intro": "",
            "fields": [3]
        }
        links = [
            {
                "type": "github",
                "url": "https://github.com/speaker_1"
            }
        ]
        new_info = {
            "name": "speaker 1",
            "photo": "https://pyladies.marsw.tw/img/speaker_1_photo.png",
            "title": "Senior Engineer",
            "major_related": True,
            "intro": "Hi~",
            "fields": [1, 2, 3],
            "links": links
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_speaker(info, autocommit=True)

            # test
            manager.update_speaker(1, new_info, autocommit=True)

            # assertion
            speaker = manager.get_speaker(1)
            self.assertEqual(speaker.name, new_info["name"])
            self.assertEqual(speaker.photo, new_info["photo"])
            self.assertEqual(speaker.title, new_info["title"])
            self.assertEqual(speaker.major_related, new_info["major_related"])
            self.assertEqual(speaker.intro, new_info["intro"])
            self.assertEqual(speaker.fields, new_info["fields"])
            self.assertEqual(speaker.links[0].type, links[0]["type"])
            self.assertEqual(speaker.links[0].url, links[0]["url"])

    def test_change_link(self):
        links = [
            {
                "type": "github",
                "url": "https://github.com/speaker_1"
            }
        ]
        info = {
            "name": "speaker 1",
            "photo": "https://pyladies.marsw.tw/img/speaker_1_photo.png",
            "title": "Senior Engineer",
            "major_related": True,
            "intro": "",
            "fields": [3],
            "links": links
        }
        new_links = [
            {
                "type": "github",
                "url": "https://github.com/speaker_1_1"
            }
        ]
        new_info = {
            "name": "speaker 1",
            "photo": "https://pyladies.marsw.tw/img/speaker_1_photo.png",
            "title": "Senior Engineer",
            "major_related": True,
            "intro": "",
            "fields": [3],
            "links": new_links
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_speaker(info, autocommit=True)

            # test
            manager.update_speaker(1, new_info, autocommit=True)

            # assertion
            speaker = manager.get_speaker(1)
            self.assertEqual(speaker.links[0].type, new_links[0]["type"])
            self.assertEqual(speaker.links[0].url, new_links[0]["url"])

    def test_update_speaker_with_different_speaker_name(self):
        info_1 = {
            "name": "speaker 1",
            "photo": "https://pyladies.marsw.tw/img/speaker_1_photo.png",
            "title": "Senior Engineer",
            "major_related": True,
            "intro": "",
            "fields": [3]
        }
        info_2 = {
            "name": "speaker 2",
            "photo": "https://pyladies.marsw.tw/img/speaker_2_photo.png",
            "title": "Senior Engineer",
            "major_related": True,
            "intro": "",
            "fields": [3]
        }
        new_info_dp = {
            "name": "speaker 2",
            "photo": "https://pyladies.marsw.tw/img/speaker_photo.png",
            "title": "Senior Engineer",
            "major_related": True,
            "intro": "Hi~",
            "fields": [1, 2, 3]
        }
        new_info_un = {
            "name": "speaker 3",
            "photo": "https://pyladies.marsw.tw/img/speaker_photo.png",
            "title": "Senior Engineer",
            "major_related": True,
            "intro": "Hi~",
            "fields": [1, 2, 3]
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_speaker(info_1, autocommit=True)
            manager.create_speaker(info_2, autocommit=True)

            # test & assertion 1
            manager.update_speaker(1, new_info_un, autocommit=True)
            speaker = manager.get_speaker(1)
            self.assertEqual(speaker.name, new_info_un["name"])
            self.assertEqual(speaker.photo, new_info_un["photo"])
            self.assertEqual(speaker.title, new_info_un["title"])
            self.assertEqual(speaker.major_related, new_info_un["major_related"])
            self.assertEqual(speaker.intro, new_info_un["intro"])
            self.assertEqual(speaker.fields, new_info_un["fields"])

            # test & assertion 2
            with self.assertRaises(IntegrityError) as cm:
                manager.update_speaker(1, new_info_dp, autocommit=True)
            error_msg = str(cm.exception)
            self.assertIn("duplicate", error_msg.lower())

    def test_delete_speaker(self):
        info = {
            "name": "speaker 1",
            "photo": "https://pyladies.marsw.tw/img/speaker_1_photo.png",
            "title": "Senior Engineer",
            "major_related": True,
            "intro": "",
            "fields": [3]
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_speaker(info, autocommit=True)
            speaker = manager.get_speaker_by_name(info["name"])
            
            # test
            manager.delete_speaker(speaker.sn, autocommit=True)

            # assertion 1
            with self.assertRaises(PyLadiesException) as cm:
                manager.get_speaker_by_name(info["name"])
            self.assertEqual(cm.exception, SPEAKER_NOT_EXIST)

            # assertion 2
            row_count = db_sess.execute("SELECT COUNT(*) FROM link").scalar()
            self.assertEqual(row_count, 0)

    def test_get_speaker_by_name(self):
        info = {
            "name": "speaker 1",
            "photo": "https://pyladies.marsw.tw/img/speaker_1_photo.png",
            "title": "Senior Engineer",
            "major_related": True,
            "intro": "",
            "fields": [3]
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_speaker(info, autocommit=True)

            # test & assertion 1
            speaker = manager.get_speaker_by_name(info["name"])
            self.assertEqual(speaker.name, info["name"])
            self.assertEqual(speaker.photo, info["photo"])
            self.assertEqual(speaker.title, info["title"])
            self.assertEqual(speaker.major_related, info["major_related"])
            self.assertEqual(speaker.intro, info["intro"])
            self.assertEqual(speaker.fields, info["fields"])

            # test & assertion 2
            with self.assertRaises(PyLadiesException) as cm:
                manager.get_speaker_by_name("speaker 2")
            self.assertEqual(cm.exception, SPEAKER_NOT_EXIST)

    def test_get_speaker_by_sn(self):
        info = {
            "name": "speaker 1",
            "photo": "https://pyladies.marsw.tw/img/speaker_1_photo.png",
            "title": "Senior Engineer",
            "major_related": True,
            "intro": "",
            "fields": [3]
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_speaker(info, autocommit=True)

            # test & assertion 1
            speaker = manager.get_speaker(1)
            self.assertEqual(speaker.name, info["name"])
            self.assertEqual(speaker.photo, info["photo"])
            self.assertEqual(speaker.title, info["title"])
            self.assertEqual(speaker.major_related, info["major_related"])
            self.assertEqual(speaker.intro, info["intro"])
            self.assertEqual(speaker.fields, info["fields"])

            # test & assertion 2
            with self.assertRaises(PyLadiesException) as cm:
                manager.get_speaker(2)
            self.assertEqual(cm.exception, SPEAKER_NOT_EXIST)

    def test_get_speakers(self):
        info_1 = {
            "name": "speaker 1",
            "photo": "https://pyladies.marsw.tw/img/speaker_1_photo.png",
            "title": "Senior Engineer",
            "major_related": True,
            "intro": "",
            "fields": [3]
        }
        info_2 = {
            "name": "speaker 2",
            "photo": "https://pyladies.marsw.tw/img/speaker_3_photo.png",
            "title": "Senior Engineer",
            "major_related": False,
            "intro": "",
            "fields": [1, 2]
        }
        info_3 = {
            "name": "speaker 3",
            "photo": "https://pyladies.marsw.tw/img/speaker_3_photo.png",
            "title": "Engineer",
            "major_related": True,
            "intro": "",
            "fields": [0, 3]
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_speaker(info_1, autocommit=True)
            manager.create_speaker(info_2, autocommit=True)
            manager.create_speaker(info_3, autocommit=True)

            # test & assertion 1
            speakers = manager.get_speakers()
            self.assertEqual(speakers[0].name, info_1["name"])
            self.assertEqual(speakers[0].photo, info_1["photo"])
            self.assertEqual(speakers[0].title, info_1["title"])
            self.assertEqual(speakers[0].major_related, info_1["major_related"])
            self.assertEqual(speakers[0].intro, info_1["intro"])
            self.assertEqual(speakers[0].fields, info_1["fields"])
            self.assertEqual(speakers[1].name, info_2["name"])
            self.assertEqual(speakers[1].photo, info_2["photo"])
            self.assertEqual(speakers[1].title, info_2["title"])
            self.assertEqual(speakers[1].major_related, info_2["major_related"])
            self.assertEqual(speakers[1].intro, info_2["intro"])
            self.assertEqual(speakers[1].fields, info_2["fields"])
            self.assertEqual(speakers[2].name, info_3["name"])
            self.assertEqual(speakers[2].photo, info_3["photo"])
            self.assertEqual(speakers[2].title, info_3["title"])
            self.assertEqual(speakers[2].major_related, info_3["major_related"])
            self.assertEqual(speakers[2].intro, info_3["intro"])
            self.assertEqual(speakers[2].fields, info_3["fields"])
