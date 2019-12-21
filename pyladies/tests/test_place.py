# coding=UTF-8

import pytest

from sqlalchemy.exc import IntegrityError

from app import create_app
from app.constant import DEFAULT_PLACE_SN
from app.exceptions import PyLadiesException
from app.exceptions import PLACE_NOT_EXIST
from app.sqldb import DBWrapper


class TestPlace:
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
    def assert_place(p1, p2):
        assert p1.name == p2["name"]
        assert p1.addr == p2["addr"]
        assert p1.map == p2["map"]

    def test_create_place(self, place_info):
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)

            # test
            manager.create_place(place_info, autocommit=True)

            # assertion
            place = manager.get_place_by_name(place_info["name"])
            self.assert_place(place, place_info)

    @pytest.mark.parametrize('place_infos', [2], indirect=True)
    def test_unique_place_name(self, place_infos):
        place_info = place_infos[0]
        place_info_2 = place_infos[1]
        place_info_2["name"] = place_info["name"]
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)

            # test
            manager.create_place(place_info, autocommit=True)

            # assertion
            with pytest.raises(IntegrityError) as cm:
                manager.create_place(place_info_2, autocommit=True)
            error_msg = str(cm.value)
            assert "duplicate" in error_msg.lower()

    @pytest.mark.parametrize('place_infos', [2], indirect=True)
    def test_update_place_with_same_place_name(self, place_infos):
        place_info = place_infos[0]
        place_info_2 = place_infos[1]
        place_info_2["name"] = place_info["name"]
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            place_sn = manager.create_place(place_info, autocommit=True)

            # test
            manager.update_place(place_sn, place_info_2, autocommit=True)

            # assertion
            place = manager.get_place(place_sn)
            self.assert_place(place, place_info_2)

    @pytest.mark.parametrize('place_infos', [3], indirect=True)
    def test_update_place_with_different_place_name(self, place_infos):
        place_info = place_infos[0]
        place_info_2 = place_infos[1]
        new_info_dp = place_info_2
        new_info_un = place_infos[2]
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            place_sn = manager.create_place(place_info, autocommit=True)
            manager.create_place(place_info_2, autocommit=True)

            # test & assertion 1
            manager.update_place(place_sn, new_info_un, autocommit=True)
            place = manager.get_place(place_sn)
            self.assert_place(place, new_info_un)

            # test & assertion 2
            with pytest.raises(IntegrityError) as cm:
                manager.update_place(place_sn, new_info_dp, autocommit=True)
            error_msg = str(cm.value)
            assert "duplicate" in error_msg.lower()

    def test_get_place_by_name(self, place_info):
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_place(place_info, autocommit=True)

            # test & assertion 1
            place = manager.get_place_by_name(place_info["name"])
            self.assert_place(place, place_info)

            # test & assertion 2
            with pytest.raises(PyLadiesException) as cm:
                manager.get_place_by_name("place 2")
            assert cm.value == PLACE_NOT_EXIST

    def test_get_place_by_sn(self, place_info):
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            place_sn = manager.create_place(place_info, autocommit=True)

            # test & assertion 1
            place = manager.get_place(place_sn)
            self.assert_place(place, place_info)

            # test & assertion 2
            with pytest.raises(PyLadiesException) as cm:
                manager.get_place(place_sn + 1)
            assert cm.value == PLACE_NOT_EXIST

    @pytest.mark.parametrize('place_infos', [3], indirect=True)
    def test_get_places(self, place_infos):
        place_info = place_infos[0]
        place_info_2 = place_infos[1]
        place_info_3 = place_infos[2]
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_place(place_info, autocommit=True)
            manager.create_place(place_info_2, autocommit=True)
            manager.create_place(place_info_3, autocommit=True)

            # test & assertion 1
            places = manager.get_places()
            places = [place for place in places if place.sn != DEFAULT_PLACE_SN]
            self.assert_place(places[0], place_info)
            self.assert_place(places[1], place_info_2)
            self.assert_place(places[2], place_info_3)
