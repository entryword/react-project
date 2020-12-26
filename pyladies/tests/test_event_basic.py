# coding=UTF-8

import pytest

from sqlalchemy.exc import IntegrityError

from app import create_app
from app.constant import DEFAULT_PLACE_SN
from app.exceptions import PyLadiesException
from app.exceptions import EVENTBASIC_NOT_EXIST
from app.sqldb import DBWrapper


class TestEventBasic:
    def setup(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.db.create_all()
        self.create_default_place()

    def teardown(self):
        self.app.db.session.remove()
        self.app.db.drop_all()
        self.app.db.engine.dispose()
        self.app_context.pop()

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

    @staticmethod
    def assert_topic_info(event_basic, topic_info):
        assert event_basic.topic.name == topic_info["name"]

    @staticmethod
    def assert_event_basic_info(event_basic, event_basic_info):
        assert event_basic.date == event_basic_info["date"]
        assert event_basic.start_time == event_basic_info["start_time"]
        assert event_basic.end_time == event_basic_info["end_time"]

    @staticmethod
    def assert_place_info(event_basic, place_info):
        if place_info is None:
            assert event_basic.place.sn == DEFAULT_PLACE_SN
            return
        assert event_basic.place.name == place_info["name"]
        assert event_basic.place.map == place_info["map"]

    @staticmethod
    def assert_exception(ex1, ex2):
        assert ex1 == ex2

    def test_create_event_basic_without_place(self, topic_info, event_basic_info):
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn

            # test
            manager.create_event_basic(event_basic_info, autocommit=True)

            # assertion
            event_basic_sn = topic.event_basics[0].sn
            event_basic = manager.get_event_basic(event_basic_sn)
            self.assert_topic_info(event_basic, topic_info)
            self.assert_event_basic_info(event_basic, event_basic_info)
            self.assert_place_info(event_basic, None)

    def test_create_event_basic_with_place(self, topic_info, event_basic_info, place_info):
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            manager.create_place(place_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            place = manager.get_place_by_name(place_info["name"])
            event_basic_info.update({
                "topic_sn": topic.sn,
                "place_sn": place.sn
            })

            # test
            manager.create_event_basic(event_basic_info, autocommit=True)

            # assertion
            event_basic_sn = topic.event_basics[0].sn
            event_basic = manager.get_event_basic(event_basic_sn)
            self.assert_topic_info(event_basic, topic_info)
            self.assert_event_basic_info(event_basic, event_basic_info)
            self.assert_place_info(event_basic, place_info)

    def test_create_event_basic_with_not_existed_topic(self, event_basic_info):
        event_basic_info["topic_sn"] = 100
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)

            # test & assertion
            with pytest.raises(IntegrityError) as cm:
                manager.create_event_basic(event_basic_info, autocommit=True)
            error_msg = str(cm.value)
            assert "foreign key" in error_msg.lower()

    @pytest.mark.parametrize('event_basic_infos', [2], indirect=True)
    def test_update_event_basic(self, topic_info, event_basic_infos, place_info):
        event_basic_info = event_basic_infos[0]
        event_basic_info_2 = event_basic_infos[1]
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            event_basic_info_2["topic_sn"] = topic.sn
            manager.create_place(place_info, autocommit=True)
            place = manager.get_place_by_name(place_info["name"])
            event_basic_info_2["place_sn"] = place.sn
            manager.create_event_basic(event_basic_info, autocommit=True)

            # test
            manager.update_event_basic(1, event_basic_info_2, autocommit=True)

            # assertion
            event_basic_sn = topic.event_basics[0].sn
            event_basic = manager.get_event_basic(event_basic_sn)
            self.assert_event_basic_info(event_basic, event_basic_info_2)
            self.assert_place_info(event_basic, place_info)

    @pytest.mark.parametrize('event_basic_infos', [2], indirect=True)
    @pytest.mark.parametrize('place_infos', [2], indirect=True)
    def test_change_place(self, topic_info, event_basic_infos, place_infos):
        event_basic_info = event_basic_infos[0]
        event_basic_info_2 = event_basic_infos[1]
        place_info = place_infos[0]
        place_info_2 = place_infos[1]
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            event_basic_info_2["topic_sn"] = topic.sn
            manager.create_place(place_info, autocommit=True)
            place = manager.get_place_by_name(place_info["name"])
            event_basic_info["place_sn"] = place.sn
            manager.create_place(place_info_2, autocommit=True)
            new_place = manager.get_place_by_name(place_info_2["name"])
            event_basic_info_2["place_sn"] = new_place.sn
            manager.create_event_basic(event_basic_info, autocommit=True)

            # test
            manager.update_event_basic(1, event_basic_info_2, autocommit=True)

            # assertion 1
            event_basic_sn = topic.event_basics[0].sn
            event_basic = manager.get_event_basic(event_basic_sn)
            self.assert_event_basic_info(event_basic, event_basic_info_2)
            self.assert_place_info(event_basic, place_info_2)

            # assertion 2
            row_count = db_sess.execute("SELECT COUNT(*) FROM place").scalar()
            assert row_count == 2 + 1 # default place is also counted

    def test_delete_event_basic(self, topic_info, event_basic_info):
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_basic_sn = topic.event_basics[0].sn

            # test
            manager.delete_event_basic(event_basic_sn, autocommit=True)

            # assertion
            with pytest.raises(PyLadiesException) as cm:
                manager.get_event_basic(event_basic_sn)
            self.assert_exception(cm.value, EVENTBASIC_NOT_EXIST)

    def test_delete_topic(self, topic_info, event_basic_info):
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_basic_sn = topic.event_basics[0].sn

            # test
            manager.delete_topic(topic.sn, autocommit=True)

            # assertion
            with pytest.raises(PyLadiesException) as cm:
                manager.get_event_basic(event_basic_sn)
            self.assert_exception(cm.value, EVENTBASIC_NOT_EXIST)

    def test_get_event_basic_by_sn(self, topic_info, event_basic_info):
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_basic_sn = topic.event_basics[0].sn

            # test & assertion 1
            event_basic = manager.get_event_basic(event_basic_sn)
            self.assert_event_basic_info(event_basic, event_basic_info)

            # test & assertion 2
            with pytest.raises(PyLadiesException) as cm:
                not_exist_event_basic_sn = event_basic_sn + 1
                manager.get_event_basic(not_exist_event_basic_sn)
            self.assert_exception(cm.value, EVENTBASIC_NOT_EXIST)

    @pytest.mark.parametrize('event_basic_infos', [2], indirect=True)
    def test_get_event_basics_by_topic(self, topic_info, event_basic_infos):
        event_basic_info = event_basic_infos[0]
        event_basic_info_2 = event_basic_infos[1]
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            event_basic_info_2["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)
            manager.create_event_basic(event_basic_info_2, autocommit=True)

            # test & assertion
            assert len(topic.event_basics) == 2
            self.assert_event_basic_info(topic.event_basics[0], event_basic_info)
            self.assert_event_basic_info(topic.event_basics[1], event_basic_info_2)
