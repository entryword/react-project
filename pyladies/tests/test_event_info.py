# coding=UTF-8

import pytest

from sqlalchemy.exc import IntegrityError

from app import create_app
from app.exceptions import PyLadiesException
from app.exceptions import EVENTINFO_NOT_EXIST
from app.sqldb import DBWrapper


class TestEventInfo:
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
    def assert_event_info(event_info1, event_info2):
        assert event_info1.title == event_info2["title"]
        assert event_info1.desc == event_info2["desc"]
        assert event_info1.fields == event_info2["fields"]

    @staticmethod
    def assert_event_info_speaker(sp1, sp2):
        assert sp1.name == sp2["name"]

    @staticmethod
    def assert_event_info_assistant(as1, as2):
        assert as1.name == as2["name"]

    @staticmethod
    def assert_event_info_slide(rs1, rs2):
        assert rs1.type == rs2["type"]
        assert rs1.title == rs2["title"]
        assert rs1.url == rs2["url"]

    def test_create_event_info_without_speakers_and_slides(
            self, topic_info, event_basic_info, event_info):
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_basic = topic.event_basics[0]
            event_info["event_basic_sn"] = event_basic.sn

            # test
            manager.create_event_info(event_info, autocommit=True)

            # assertion
            event_info_sn = event_basic.event_info.sn
            event = manager.get_event_info(event_info_sn)
            self.assert_event_info(event, event_info)

    @pytest.mark.parametrize('speaker_infos', [2], indirect=True)
    @pytest.mark.parametrize('assistant_infos', [2], indirect=True)
    def test_create_event_info_without_slides(
            self, topic_info, event_basic_info, event_info, speaker_infos, assistant_infos):
        speaker_info_1 = speaker_infos[0]
        speaker_info_2 = speaker_infos[1]
        assistant_info_1 = assistant_infos[0]
        assistant_info_2 = assistant_infos[1]
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
            event_info["event_basic_sn"] = event_basic.sn
            event_info["speaker_sns"] = [speaker_1.sn, speaker_2.sn]
            event_info["assistant_sns"] = [assistant_1.sn, assistant_2.sn]

            # test
            manager.create_event_info(event_info, autocommit=True)

            # assertion
            event_info_sn = event_basic.event_info.sn
            event = manager.get_event_info(event_info_sn)
            self.assert_event_info(event, event_info)
            self.assert_event_info_speaker(event.speakers[0], speaker_info_1)
            self.assert_event_info_speaker(event.speakers[1], speaker_info_2)
            self.assert_event_info_assistant(event.assistants[0], assistant_info_1)
            self.assert_event_info_assistant(event.assistants[1], assistant_info_2)


    @pytest.mark.parametrize('slide_resources', [2], indirect=True)
    def test_create_event_info_with_speakers_and_slides(
            self, topic_info, event_basic_info, event_info,
            speaker_info, assistant_info, slide_resources):
        slide_resource_sns = []
        event_info["slide_resource_sns"] = slide_resource_sns
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_speaker(speaker_info, autocommit=True)
            speaker = manager.get_speaker_by_name(speaker_info["name"])
            manager.create_speaker(assistant_info, autocommit=True)
            assistant = manager.get_speaker_by_name(assistant_info["name"])
            for item in slide_resources:
                slide_resource_sns.append(manager.create_slide_resource(item, autocommit=True))
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_basic = topic.event_basics[0]
            event_info["event_basic_sn"] = event_basic.sn
            event_info["speaker_sns"] = [speaker.sn]
            event_info["assistant_sns"] = [assistant.sn]

            # test
            manager.create_event_info(event_info, autocommit=True)

            # assertion
            event_info_sn = event_basic.event_info.sn
            event = manager.get_event_info(event_info_sn)
            self.assert_event_info(event, event_info)
            self.assert_event_info_speaker(event.speakers[0], speaker_info)
            self.assert_event_info_assistant(event.assistants[0], assistant_info)
            self.assert_event_info_slide(event.slide_resources[0], slide_resources[0])
            self.assert_event_info_slide(event.slide_resources[1], slide_resources[1])

    def test_create_event_info_with_not_exist_event_basic(self, event_info):
        event_info["event_basic_sn"] = 100
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)

            # test & assertion
            with pytest.raises(IntegrityError) as cm:
                manager.create_event_info(event_info, autocommit=True)
            error_msg = str(cm.value)
            assert "foreign key" in error_msg.lower()

    @pytest.mark.parametrize('event_infos', [2], indirect=True)
    def test_one_event_basic_one_event_info(self, topic_info, event_basic_info, event_infos):
        event_info_1 = event_infos[0]
        event_info_2 = event_infos[1]
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_basic = topic.event_basics[0]
            event_info_1["event_basic_sn"] = event_basic.sn
            event_info_2["event_basic_sn"] = event_basic.sn

            # test
            manager.create_event_info(event_info_1, autocommit=True)

            # assertion
            with pytest.raises(IntegrityError) as cm:
                manager.create_event_info(event_info_2, autocommit=True)
            error_msg = str(cm.value)
            assert "duplicate" in error_msg.lower()

    @pytest.mark.parametrize('event_infos', [2], indirect=True)
    def test_update_event_info_without_speakers_and_slides(
            self, topic_info, event_basic_info, event_infos):
        event_info_1 = event_infos[0]
        event_info_2 = event_infos[1]
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_basic = topic.event_basics[0]
            event_info_1["event_basic_sn"] = event_basic.sn
            event_info_2["event_basic_sn"] = event_basic.sn
            manager.create_event_info(event_info_1, autocommit=True)

            # test
            manager.update_event_info(1, event_info_2, autocommit=True)

            # assertion
            event_info_sn = event_basic.event_info.sn
            event = manager.get_event_info(event_info_sn)
            self.assert_event_info(event, event_info_2)

    @pytest.mark.parametrize('event_infos', [2], indirect=True)
    def test_update_event_info_with_speakers(
            self, topic_info, event_basic_info, event_infos, speaker_info, assistant_info):
        event_info_1 = event_infos[0]
        event_info_2 = event_infos[1]
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_basic = topic.event_basics[0]
            event_info_1["event_basic_sn"] = event_basic.sn
            event_info_2["event_basic_sn"] = event_basic.sn
            manager.create_event_info(event_info_1, autocommit=True)

            # test
            manager.create_speaker(speaker_info, autocommit=True)
            speaker = manager.get_speaker_by_name(speaker_info["name"])
            manager.create_speaker(assistant_info, autocommit=True)
            assistant = manager.get_speaker_by_name(assistant_info["name"])
            event_info_2["speaker_sns"] = [speaker.sn]
            event_info_2["assistant_sns"] = [assistant.sn]
            manager.update_event_info(1, event_info_2, autocommit=True)

            # assertion
            event_info_sn = event_basic.event_info.sn
            event = manager.get_event_info(event_info_sn)
            self.assert_event_info(event, event_info_2)
            self.assert_event_info_speaker(event.speakers[0], speaker_info)
            self.assert_event_info_assistant(event.assistants[0], assistant_info)

    @pytest.mark.parametrize('event_infos', [2], indirect=True)
    @pytest.mark.parametrize('speaker_infos', [2], indirect=True)
    @pytest.mark.parametrize('assistant_infos', [2], indirect=True)
    def test_change_speakers(
            self, topic_info, event_basic_info, event_infos, speaker_infos, assistant_infos):
        event_info_1 = event_infos[0]
        event_info_2 = event_infos[1]
        speaker_info_1 = speaker_infos[0]
        speaker_info_2 = speaker_infos[1]
        assistant_info_1 = assistant_infos[0]
        assistant_info_2 = assistant_infos[1]
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_basic = topic.event_basics[0]
            event_info_1["event_basic_sn"] = event_basic.sn
            event_info_2["event_basic_sn"] = event_basic.sn
            manager.create_speaker(speaker_info_1, autocommit=True)
            speaker = manager.get_speaker_by_name(speaker_info_1["name"])
            event_info_1["speaker_sns"] = [speaker.sn]
            manager.create_speaker(assistant_info_1, autocommit=True)
            assistant = manager.get_speaker_by_name(assistant_info_1["name"])
            event_info_1["assistant_sns"] = [assistant.sn]
            manager.create_speaker(speaker_info_2, autocommit=True)
            new_speaker = manager.get_speaker_by_name(speaker_info_2["name"])
            event_info_2["speaker_sns"] = [new_speaker.sn]
            manager.create_speaker(assistant_info_2, autocommit=True)
            new_assistant = manager.get_speaker_by_name(assistant_info_2["name"])
            event_info_2["assistant_sns"] = [new_assistant.sn]
            manager.create_event_info(event_info_1, autocommit=True)

            # test
            manager.update_event_info(1, event_info_2, autocommit=True)

            # assertion 1
            event = manager.get_event_info(1)
            self.assert_event_info_speaker(event.speakers[0], speaker_info_2)
            self.assert_event_info_assistant(event.assistants[0], assistant_info_2)

            # assertion 2
            row_count = db_sess.execute("SELECT COUNT(*) FROM speaker").scalar()
            assert row_count == 4

    @pytest.mark.parametrize('event_infos', [2], indirect=True)
    @pytest.mark.parametrize('slide_resources', [2], indirect=True)
    def test_change_slides(self, topic_info, event_basic_info, event_infos, slide_resources):
        new_slide_resources = [slide_resources[1]]
        slide_resources = [slide_resources[0]]
        slide_resource_sns = []
        new_slide_resource_sns = []
        event_info_1 = event_infos[0]
        event_info_2 = event_infos[1]
        event_info_1["slide_resource_sns"] = slide_resource_sns
        event_info_2["slide_resource_sns"] = new_slide_resource_sns
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_basic = topic.event_basics[0]
            event_info_1["event_basic_sn"] = event_basic.sn
            event_info_2["event_basic_sn"] = event_basic.sn
            for item in slide_resources:
                slide_resource_sns.append(manager.create_slide_resource(item, autocommit=True))
            manager.create_event_info(event_info_1, autocommit=True)
            for item in new_slide_resources:
                new_slide_resource_sns.append(manager.create_slide_resource(item, autocommit=True))

            # test
            manager.update_event_info(1, event_info_2, autocommit=True)

            # assertion 1
            event = manager.get_event_info(1)
            self.assert_event_info_slide(event.slide_resources[0], new_slide_resources[0])

            # assertion 2
            row_count = db_sess.execute("SELECT COUNT(*) FROM slide_resource").scalar()
            assert row_count == 2

    @pytest.mark.parametrize('event_infos', [2], indirect=True)
    @pytest.mark.parametrize('slide_resources', [2], indirect=True)
    def test_update_event_info_with_slides(
            self, topic_info, event_basic_info, event_infos, slide_resources):
        slide_resource_sns = []
        event_info_1 = event_infos[0]
        event_info_2 = event_infos[1]
        event_info_2["slide_resource_sns"] = slide_resource_sns
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_basic = topic.event_basics[0]
            event_info_1["event_basic_sn"] = event_basic.sn
            event_info_2["event_basic_sn"] = event_basic.sn
            manager.create_event_info(event_info_1, autocommit=True)
            for item in slide_resources:
                slide_resource_sns.append(manager.create_slide_resource(item, autocommit=True))

            # test
            manager.update_event_info(1, event_info_2, autocommit=True)

            # assertion
            event_info_sn = event_basic.event_info.sn
            event = manager.get_event_info(event_info_sn)
            self.assert_event_info(event, event_info_2)
            self.assert_event_info_slide(event.slide_resources[0], slide_resources[0])
            self.assert_event_info_slide(event.slide_resources[1], slide_resources[1])

    @pytest.mark.parametrize('slide_resources', [2], indirect=True)
    def test_delete_event_info(
            self, topic_info, event_basic_info, event_info,
            speaker_info, assistant_info, slide_resources):
        slide_resource_sns = []
        event_info["slide_resource_sns"] = slide_resource_sns
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_basic = topic.event_basics[0]
            event_info["event_basic_sn"] = event_basic.sn
            manager.create_speaker(speaker_info, autocommit=True)
            speaker = manager.get_speaker_by_name(speaker_info["name"])
            manager.create_speaker(assistant_info, autocommit=True)
            assistant = manager.get_speaker_by_name(assistant_info["name"])
            for item in slide_resources:
                slide_resource_sns.append(manager.create_slide_resource(item, autocommit=True))
            event_info["speaker_sns"] = [speaker.sn]
            event_info["assistant_sns"] = [assistant.sn]
            manager.create_event_info(event_info, autocommit=True)
            event_info_sn = event_basic.event_info.sn

            # test
            manager.delete_event_info(event_info_sn, autocommit=True)

            # assertion 1
            with pytest.raises(PyLadiesException) as cm:
                manager.get_event_info(event_info_sn)
            assert cm.value == EVENTINFO_NOT_EXIST

            # assertion 2
            row_count = db_sess.execute("SELECT COUNT(*) FROM speaker").scalar()
            assert row_count == 2
            row_count = db_sess.execute("SELECT COUNT(*) FROM slide_resource").scalar()
            assert row_count == 2

    def test_delete_event_basic(self, topic_info, event_basic_info, event_info):
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            event_basic_info["topic_sn"] = 1
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_info["event_basic_sn"] = 1
            manager.create_event_info(event_info, autocommit=True)

            # test
            manager.delete_event_basic(1, autocommit=True)

            # assertion
            with pytest.raises(PyLadiesException) as cm:
                manager.get_event_info(1)
            assert cm.value == EVENTINFO_NOT_EXIST

    def test_delete_topic(self, topic_info, event_basic_info, event_info):
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            event_basic_info["topic_sn"] = 1
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_info["event_basic_sn"] = 1
            manager.create_event_info(event_info, autocommit=True)

            # test
            manager.delete_topic(1, autocommit=True)

            # assertion
            with pytest.raises(PyLadiesException) as cm:
                manager.get_event_info(1)
            assert cm.value == EVENTINFO_NOT_EXIST

    @pytest.mark.parametrize('speaker_infos', [2], indirect=True)
    @pytest.mark.parametrize('assistant_infos', [2], indirect=True)
    def test_delete_speaker(
            self, topic_info, event_basic_info, event_info, speaker_infos, assistant_infos):
        speaker_info_1 = speaker_infos[0]
        speaker_info_2 = speaker_infos[1]
        assistant_info_1 = assistant_infos[0]
        assistant_info_2 = assistant_infos[1]
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_basic = topic.event_basics[0]
            event_info["event_basic_sn"] = event_basic.sn
            manager.create_speaker(speaker_info_1, autocommit=True)
            speaker_1 = manager.get_speaker_by_name(speaker_info_1["name"])
            manager.create_speaker(speaker_info_2, autocommit=True)
            speaker_2 = manager.get_speaker_by_name(speaker_info_2["name"])
            event_info["speaker_sns"] = [speaker_1.sn, speaker_2.sn]
            manager.create_speaker(assistant_info_1, autocommit=True)
            assistant_1 = manager.get_speaker_by_name(assistant_info_1["name"])
            manager.create_speaker(assistant_info_2, autocommit=True)
            assistant_2 = manager.get_speaker_by_name(assistant_info_2["name"])
            event_info["assistant_sns"] = [assistant_1.sn, assistant_2.sn]
            manager.create_event_info(event_info, autocommit=True)
            event_info_sn = event_basic.event_info.sn

            # test
            manager.delete_speaker(speaker_1.sn, autocommit=True)
            manager.delete_speaker(assistant_1.sn, autocommit=True)

            # assertion 1
            event = manager.get_event_info(event_info_sn)
            self.assert_event_info_speaker(event.speakers[0], speaker_info_2)
            self.assert_event_info_assistant(event.assistants[0], assistant_info_2)

            # assertion 2
            row_count = db_sess.execute("SELECT COUNT(*) FROM speaker").scalar()
            assert row_count == 2

    def test_get_event_info_by_sn(self, topic_info, event_basic_info, event_info):
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_basic = topic.event_basics[0]
            event_info["event_basic_sn"] = event_basic.sn
            manager.create_event_info(event_info, autocommit=True)
            event_info_sn = event_basic.event_info.sn

            # test & assertion 1
            event = manager.get_event_info(event_info_sn)
            self.assert_event_info(event, event_info)

            # test & assertion 2
            with pytest.raises(PyLadiesException) as cm:
                not_exist_event_info_sn = event_info_sn + 1
                manager.get_event_info(not_exist_event_info_sn)
            assert cm.value == EVENTINFO_NOT_EXIST

    def test_get_event_info_by_event_basic(self, topic_info, event_basic_info, event_info):
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_basic = topic.event_basics[0]
            event_info["event_basic_sn"] = event_basic.sn

            # test
            manager.create_event_info(event_info, autocommit=True)

            # assertion
            self.assert_event_info(event_basic.event_info, event_info)
