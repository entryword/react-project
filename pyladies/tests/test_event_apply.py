# coding=UTF-8

import pytest

from app import create_app
from app.constant import DEFAULT_PLACE_SN
from app.exceptions import PyLadiesException
from app.exceptions import APPLY_NOT_EXIST
from app.sqldb import DBWrapper

# from tests import conftest

class TestEventApply:
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

    @pytest.mark.parametrize('apply_infos', [2], indirect=True)
    def test_create_event_apply(self, topic_info, event_basic_info, apply_infos):
        input_event_apply = {
            "event_basic_sn": None,
            "apply": apply_infos
        }

        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_basic = topic.event_basics[0]
            input_event_apply["event_basic_sn"] = event_basic.sn

            # test
            manager.create_event_apply(input_event_apply, autocommit=True)
            event_apply = manager.get_event_apply_by_event_basic_sn(event_basic.sn)

            # test & assertion
            assert event_apply.event_basic_sn == event_basic.sn
            assert event_apply.apply == input_event_apply["apply"]

    @pytest.mark.parametrize('apply_infos', [2], indirect=True)
    def test_update_event_apply(self, topic_info, event_basic_info, apply_infos):
        apply_info = apply_infos[0]
        apply_info_2 = apply_infos[1]
        input_event_apply = {
            "event_basic_sn": None,
            "apply": [apply_info]
        }
        input_event_apply_2 = {
            "apply": [apply_info_2]
        }

        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_basic = topic.event_basics[0]
            input_event_apply["event_basic_sn"] = event_basic.sn

            event_apply_sn = manager.create_event_apply(input_event_apply, autocommit=True)
            event_apply_before = manager.get_event_apply(event_apply_sn)
            event_basic_sn_before = event_apply_before.event_basic_sn
            apply_info_before = event_apply_before.apply

            # test
            manager.update_event_apply(event_apply_sn, input_event_apply_2, autocommit=True)
            event_apply_after = manager.get_event_apply(event_apply_sn)
            event_basic_sn_after = event_apply_after.event_basic_sn
            apply_info_after = event_apply_after.apply

            # test & assertion
            assert event_basic_sn_before == event_basic_sn_after
            assert apply_info_before == input_event_apply["apply"]
            assert apply_info_after == input_event_apply_2["apply"]

    def test_delete_event_apply(self, topic_info, event_basic_info, apply_info):
        input_event_apply = {
            "event_basic_sn": None,
            "apply": [apply_info]
        }

        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_basic = topic.event_basics[0]
            input_event_apply["event_basic_sn"] = event_basic.sn

            event_apply_sn = manager.create_event_apply(input_event_apply, autocommit=True)

            # test
            manager.delete_event_apply(event_apply_sn, autocommit=True)

            # test & assertion
            with pytest.raises(PyLadiesException) as cm:
                manager.get_event_apply(event_apply_sn)
            assert cm.value == APPLY_NOT_EXIST
