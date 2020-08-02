import pytest
from sqlalchemy.exc import IntegrityError

from app import create_app
from app.constant import DEFAULT_PLACE_SN
from app.exceptions import PyLadiesException
from app.exceptions import SPEAKER_NOT_EXIST
from app.managers.speaker import Manager as SpeakerManager
from app.sqldb import DBWrapper


class TestSpeaker():
    def setup(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.db.create_all()
        self.create_default_place()
    
    def create_default_place(self):
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            place_info = {
                "sn": DEFAULT_PLACE_SN,
                "name": "default place",
                "addr": "default place addr",
                "map": "default place map",
            }
            manager.create_place(place_info, autocommit=True)

    def teardown(self):
        self.app.db.session.remove()
        self.app.db.drop_all()
        self.app.db.engine.dispose()
        self.app_context.pop()

    def assertEqual(self, result, expected_result):
        assert result == expected_result

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
            with pytest.raises(IntegrityError, match=r".*Duplicate.*"):
                manager.create_speaker(info_2, autocommit=True)

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
            with pytest.raises(IntegrityError, match=r".*Duplicate.*"):
                manager.update_speaker(1, new_info_dp, autocommit=True)

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
            with pytest.raises(PyLadiesException) as cm:
                manager.get_speaker_by_name(info["name"])
            self.assertEqual(cm.value, SPEAKER_NOT_EXIST)

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
            with pytest.raises(PyLadiesException) as cm:
                manager.get_speaker_by_name("speaker 2")
            self.assertEqual(cm.value, SPEAKER_NOT_EXIST)

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
            with pytest.raises(PyLadiesException) as cm:
                manager.get_speaker(2)
            self.assertEqual(cm.value, SPEAKER_NOT_EXIST)

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

    def test_search_speakers(self):
        info_1 = {
            "name": "speaker apple",
            "photo": "https://pyladies.marsw.tw/img/speaker_1_photo.png",
            "title": "Senior Engineer",
            "major_related": True,
            "intro": "",
            "fields": [3]
        }
        ans_1 = {
            "id": 1,
            "name": "speaker apple",
            "photo": "https://pyladies.marsw.tw/img/speaker_1_photo.png",
            "title": "Senior Engineer",
            "fields": [3]
        }
        info_2 = {
            "name": "speaker banana",
            "photo": "https://pyladies.marsw.tw/img/speaker_3_photo.png",
            "title": "Senior Engineer",
            "major_related": False,
            "intro": "",
            "fields": [1, 2]
        }
        ans_2 = {
            "id": 2,
            "name": "speaker banana",
            "photo": "https://pyladies.marsw.tw/img/speaker_3_photo.png",
            "title": "Senior Engineer",
            "fields": [1, 2]
        }

        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_speaker(info_1, autocommit=True)
            manager.create_speaker(info_2, autocommit=True)

            # test & assertion
            speakers = manager.search_speakers("")
            self.assertEqual(len(speakers), 2)
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

            speakers = manager.search_speakers("apple")
            self.assertEqual(len(speakers), 1)
            self.assertEqual(speakers[0].name, info_1["name"])
            self.assertEqual(speakers[0].photo, info_1["photo"])
            self.assertEqual(speakers[0].title, info_1["title"])
            self.assertEqual(speakers[0].major_related, info_1["major_related"])
            self.assertEqual(speakers[0].intro, info_1["intro"])
            self.assertEqual(speakers[0].fields, info_1["fields"])

            speakers = manager.search_speakers("banana")
            self.assertEqual(len(speakers), 1)
            self.assertEqual(speakers[0].name, info_2["name"])
            self.assertEqual(speakers[0].photo, info_2["photo"])
            self.assertEqual(speakers[0].title, info_2["title"])
            self.assertEqual(speakers[0].major_related, info_2["major_related"])
            self.assertEqual(speakers[0].intro, info_2["intro"])
            self.assertEqual(speakers[0].fields, info_2["fields"])

            speakers = manager.search_speakers("cat")
            self.assertEqual(len(speakers), 0)

    @pytest.mark.parametrize('event_infos', [3], indirect=True)
    @pytest.mark.parametrize('event_basic_infos', [3], indirect=True)
    @pytest.mark.parametrize('topic_infos', [2], indirect=True)
    def test_get_speaker_profile(self, speaker_info, event_infos, event_basic_infos, topic_infos):
        event_basic_info1 = event_basic_infos[0]
        event_basic_info2 = event_basic_infos[1]
        event_basic_info3 = event_basic_infos[2]
        event_info1 = event_infos[0]
        event_info2 = event_infos[1]
        event_info3 = event_infos[2]
        links = [{
            "type": "Github",
            "url": "http://github.com/speaker"
        }]
        speaker_info["links"] = links

        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)

            manager.create_speaker(speaker_info, autocommit=True)
            speaker = manager.get_speaker_by_name(speaker_info["name"])

            manager.create_topic(topic_infos[0], autocommit=True)
            manager.create_topic(topic_infos[1], autocommit=True)
            topic1 = manager.get_topic_by_name(topic_infos[0]["name"])
            topic2 = manager.get_topic_by_name(topic_infos[1]["name"])
            event_basic_info1["topic_sn"] = topic1.sn
            event_basic_info2["topic_sn"] = topic1.sn
            event_basic_info3["topic_sn"] = topic2.sn
            manager.create_event_basic(event_basic_info1, autocommit=True)
            manager.create_event_basic(event_basic_info2, autocommit=True)
            manager.create_event_basic(event_basic_info3, autocommit=True)
            event_info1["event_basic_sn"] = topic1.event_basics[0].sn
            event_info2["event_basic_sn"] = topic1.event_basics[1].sn
            event_info3["event_basic_sn"] = topic2.event_basics[0].sn
            event_info1["speaker_sns"] = [speaker.sn]
            event_info2["speaker_sns"] = [speaker.sn]
            event_info3["speaker_sns"] = [speaker.sn]
            manager.create_event_info(event_info1, autocommit=True)
            manager.create_event_info(event_info2, autocommit=True)
            manager.create_event_info(event_info3, autocommit=True)

            expected_talks = [
                {'topic_name': topic1.name, 'topic_id': topic1.sn,
                 'events': [{'id': 1, 'title': event_info1["title"]},
                            {'id': 2, 'title': event_info2["title"]}]},
                {'topic_name': topic2.name, 'topic_id': topic2.sn,
                 'events': [{'id': 3, 'title': event_info3["title"]}]}
            ]

            # test & assertion 1
            result = SpeakerManager().get_speaker_profile(speaker.sn)
            self.assertEqual(result["name"], speaker_info["name"])
            self.assertEqual(result["photo"], speaker_info["photo"])
            self.assertEqual(result["title"], speaker_info["title"])
            self.assertEqual(result["major_related"], speaker_info["major_related"])
            self.assertEqual(result["intro"], speaker_info["intro"])
            self.assertEqual(result["fields"], speaker_info["fields"])
            self.assertEqual(result["links"], links)
            self.assertEqual(result["talks"], expected_talks)
