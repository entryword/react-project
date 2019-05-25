# coding=UTF-8

import unittest

from sqlalchemy.exc import IntegrityError

from app import create_app
from app.exceptions import PyLadiesException
from app.exceptions import PLACE_NOT_EXIST
from app.sqldb import DBWrapper


class PlaceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.db.create_all()

    def tearDown(self):
        self.app.db.session.remove()
        self.app.db.drop_all()
        self.app.db.engine.dispose()
        self.app_context.pop()

    def test_create_place(self):
        info = {
            "name": "place 1",
            "addr": "台北市信義區光復南路133號",
            "map": "http://abc.com/map.html"
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)

            # test
            manager.create_place(info, autocommit=True)

            # assertion
            place = manager.get_place_by_name(info["name"])
            self.assertEqual(place.name, info["name"])
            self.assertEqual(place.addr, info["addr"])
            self.assertEqual(place.map, info["map"])

    def test_unique_place_name(self):
        info_1 = {
            "name": "place 1",
            "addr": "台北市信義區光復南路133號",
            "map": "http://abc.com/map.html"
        }
        info_2 = {
            "name": "place 1",
            "addr": "台北市萬華區艋舺大道101號",
            "map": "http://abc.com/map2.html"
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)

            # test
            manager.create_place(info_1, autocommit=True)

            # assertion
            with self.assertRaises(IntegrityError) as cm:
                manager.create_place(info_2, autocommit=True)
            error_msg = str(cm.exception)
            self.assertIn("duplicate", error_msg.lower())

    def test_update_place_with_same_place_name(self):
        info = {
            "name": "place 1",
            "addr": "台北市信義區光復南路133號",
            "map": "http://abc.com/map.html"
        }
        new_info = {
            "name": "place 1",
            "addr": "台北市信義區光復南路134號",
            "map": "http://abc.com/map2.html"
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_place(info, autocommit=True)

            # test
            manager.update_place(1, new_info, autocommit=True)

            # assertion
            place = manager.get_place(1)
            self.assertEqual(place.name, new_info["name"])
            self.assertEqual(place.addr, new_info["addr"])
            self.assertEqual(place.map, new_info["map"])

    def test_update_place_with_different_place_name(self):
        info_1 = {
            "name": "place 1",
            "addr": "台北市信義區光復南路133號",
            "map": "http://abc.com/map.html"
        }
        info_2 = {
            "name": "place 2",
            "addr": "台北市萬華區艋舺大道101號",
            "map": "http://def.com/map.html"
        }
        new_info_dp = {
            "name": "place 2",
            "addr": "台北市萬華區艋舺大道101號",
            "map": "http://abc.com/map2.html"
        }
        new_info_un = {
            "name": "place 3",
            "addr": "台北市大安區和平東路二段50號",
            "map": "http://abc.com/map2.html"
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_place(info_1, autocommit=True)
            manager.create_place(info_2, autocommit=True)

            # test & assertion 1
            manager.update_place(1, new_info_un, autocommit=True)
            place = manager.get_place(1)
            self.assertEqual(place.name, new_info_un["name"])
            self.assertEqual(place.addr, new_info_un["addr"])
            self.assertEqual(place.map, new_info_un["map"])

            # test & assertion 2
            with self.assertRaises(IntegrityError) as cm:
                manager.update_place(1, new_info_dp, autocommit=True)
            error_msg = str(cm.exception)
            self.assertIn("duplicate", error_msg.lower())

    def test_delete_place(self):
        info = {
            "name": "place 1",
            "addr": "台北市信義區光復南路133號",
            "map": "http://abc.com/map.html"
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_place(info, autocommit=True)
            place = manager.get_place_by_name(info["name"])

            # test
            manager.delete_place(place.sn, autocommit=True)

            # assertion
            with self.assertRaises(PyLadiesException) as cm:
                manager.get_place_by_name(info["name"])
            self.assertEqual(cm.exception, PLACE_NOT_EXIST)

    def test_get_place_by_name(self):
        info = {
            "name": "place 1",
            "addr": "台北市信義區光復南路133號",
            "map": "http://abc.com/map.html"
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_place(info, autocommit=True)

            # test & assertion 1
            place = manager.get_place_by_name(info["name"])
            self.assertEqual(place.name, info["name"])
            self.assertEqual(place.addr, info["addr"])
            self.assertEqual(place.map, info["map"])

            # test & assertion 2
            with self.assertRaises(PyLadiesException) as cm:
                manager.get_place_by_name("place 2")
            self.assertEqual(cm.exception, PLACE_NOT_EXIST)

    def test_get_place_by_sn(self):
        info = {
            "name": "place 1",
            "addr": "台北市信義區光復南路133號",
            "map": "http://abc.com/map.html"
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_place(info, autocommit=True)

            # test & assertion 1
            place = manager.get_place(1)
            self.assertEqual(place.name, info["name"])
            self.assertEqual(place.addr, info["addr"])
            self.assertEqual(place.map, info["map"])

            # test & assertion 2
            with self.assertRaises(PyLadiesException) as cm:
                manager.get_place(2)
            self.assertEqual(cm.exception, PLACE_NOT_EXIST)

    def test_get_places(self):
        info_1 = {
            "name": "place 1",
            "addr": "台北市信義區光復南路133號",
            "map": "http://abc.com/map1.html"
        }
        info_2 = {
            "name": "place 2",
            "addr": "台北市萬華區艋舺大道101號",
            "map": "http://abc.com/map2.html"
        }
        info_3 = {
            "name": "place 3",
            "addr": "台北市大安區和平東路二段50號",
            "map": "http://abc.com/map3.html"
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_place(info_1, autocommit=True)
            manager.create_place(info_2, autocommit=True)
            manager.create_place(info_3, autocommit=True)

            # test & assertion 1
            places = manager.get_places()
            self.assertEqual(places[0].name, info_1["name"])
            self.assertEqual(places[0].addr, info_1["addr"])
            self.assertEqual(places[0].map, info_1["map"])
            self.assertEqual(places[1].name, info_2["name"])
            self.assertEqual(places[1].addr, info_2["addr"])
            self.assertEqual(places[1].map, info_2["map"])
            self.assertEqual(places[2].name, info_3["name"])
            self.assertEqual(places[2].addr, info_3["addr"])
            self.assertEqual(places[2].map, info_3["map"])
