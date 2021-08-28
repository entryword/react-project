# coding=UTF-8

import unittest

from app import create_app
from app.exceptions import PyLadiesException, ROLE_NAME_DUPLICATE, ROLE_NOT_EXIST
from app.managers.role import Manager as RoleManager
from app.sqldb import DBWrapper
from app.sqldb.models import Role


class RoleManagerTestCase(unittest.TestCase):
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

    def _create_test_role_basic(self):
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            r1 = Role()
            r1.name = 'r1'
            r1.permission = {
                "EventList": 2,
                "Event": 2,
                "EventRegister": 2,
                "SpeakerList": 2,
                "Speaker": 2,
                "PlaceList": 1,
                "Place": 1,
                "UserList": 2,
                "Role": 2
            }
            db_sess.add(r1)
            db_sess.commit()
            return r1.id

    def test_get_roles(self):
        # preparation
        r1_id = self._create_test_role_basic()
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            r2 = Role()
            r2.name = 'r2'
            r2.permission = {'feat3': 2, 'feat2': 1}
            db_sess.add(r2)
            db_sess.commit()

            # test
            res = RoleManager.get_roles()

            # assert
            self.assertEqual([
                {
                    'id': r1_id,
                    'name': 'r1',
                    'permission': {
                        "EventList": 2,
                        "Event": 2,
                        "EventRegister": 2,
                        "SpeakerList": 2,
                        "Speaker": 2,
                        "PlaceList": 1,
                        "Place": 1,
                        "UserList": 2,
                        "Role": 2
                    }
                }, {
                    'id': r2.id,
                    'name': 'r2',
                    'permission': {'feat3': 2, 'feat2': 1}
                }
            ], res)

    def test_get_roles_empty_list(self):
        # test
        res = RoleManager.get_roles()

        # assert
        self.assertEqual([], res)

    def test_get_role(self):
        # preparation
        r1_id = self._create_test_role_basic()

        # test
        res = RoleManager.get_role(r1_id)

        # assert
        self.assertEqual({
            'id': r1_id,
            'name': 'r1',
            'permission': {
                "EventList": 2,
                "Event": 2,
                "EventRegister": 2,
                "SpeakerList": 2,
                "Speaker": 2,
                "PlaceList": 1,
                "Place": 1,
                "UserList": 2,
                "Role": 2
            }
        }, res)

    def test_get_role_id_not_found(self):
        # preparation
        not_existed_id = 123

        # test and assert
        with self.assertRaises(PyLadiesException) as cm:
            RoleManager.get_role(not_existed_id)
        self.assertEqual(cm.exception, ROLE_NOT_EXIST)

    def test_create_role(self):
        # preparation
        role_info = {
            "name": "now_role_name",
            "permission": {
                "EventList": 2,
                "Event": 2,
                "EventRegister": 2,
                "SpeakerList": 2,
                "Speaker": 2,
                "PlaceList": 1,
                "Place": 1,
                "UserList": 2,
                "Role": 2
            }
        }

        # test
        id = RoleManager.create_role(role_info)

        # assert
        self.assertIsNotNone(id)

    def test_create_role_duplicate_role_name(self):
        self._create_test_role_basic()
        duplicate_role_name_info = {
            "name": "r1",
            "permission": {
                "EventList": 1,
                "Event": 0,
                "EventRegister": 1,
                "SpeakerList": 0,
                "Speaker": 2,
                "PlaceList": 1,
                "Place": 1,
                "UserList": 2,
                "Role": 2
            }
        }
        # test and assert
        with self.assertRaises(PyLadiesException) as cm:
            RoleManager.create_role(duplicate_role_name_info)
        self.assertEqual(cm.exception, ROLE_NAME_DUPLICATE)

    def test_update_role(self):
        # preparation
        r1_id = self._create_test_role_basic()
        update_role_info = {
            "name": "now_role_name",
            "permission": {
                "EventList": 2,
                "Event": 2,
                "EventRegister": 2,
                "SpeakerList": 2,
                "Speaker": 2,
                "PlaceList": 1,
                "Place": 1,
                "UserList": 2,
                "Role": 2
            }
        }

        # test
        res = RoleManager.update_role(r1_id, update_role_info)

        # assert
        self.assertIsNone(res)

    def test_update_role_duplicate_name(self):
        # preparation
        self._create_test_role_basic()
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            r2 = Role()
            r2.name = 'r2'
            r2.permission = {
                "EventList": 2,
                "Event": 2,
                "EventRegister": 2,
                "SpeakerList": 2,
                "Speaker": 2,
                "PlaceList": 1,
                "Place": 1,
                "UserList": 2,
                "Role": 2
            }
            db_sess.add(r2)
            db_sess.commit()

            update_r2_with_r1_name_info = {
                "name": "r1",
                "permission": {
                    "EventList": 2,
                    "Event": 2,
                    "EventRegister": 2,
                    "SpeakerList": 2,
                    "Speaker": 2,
                    "PlaceList": 1,
                    "Place": 1,
                    "UserList": 2,
                    "Role": 2
                }
            }

            # test and assert
            with self.assertRaises(PyLadiesException) as cm:
                RoleManager.update_role(r2.id, update_r2_with_r1_name_info)
            self.assertEqual(cm.exception, ROLE_NAME_DUPLICATE)

    def test_update_role_id_not_found(self):
        # preparation
        not_existed_id = 123
        update_role_info = {
            "name": "role",
            "permission": {
                "EventList": 2,
                "Event": 2,
                "EventRegister": 2,
                "SpeakerList": 2,
                "Speaker": 2,
                "PlaceList": 1,
                "Place": 1,
                "UserList": 2,
                "Role": 2
            }
        }

        # test and assert
        with self.assertRaises(PyLadiesException) as cm:
            RoleManager.update_role(not_existed_id, update_role_info)
        self.assertEqual(cm.exception, ROLE_NOT_EXIST)

    def test_delete_role(self):
        # preparation
        r1_id = self._create_test_role_basic()

        # test
        res = RoleManager.delete_role(r1_id)

        # assert
        self.assertIsNone(res)

    def test_delete_role_id_not_found(self):
        # preparation
        not_existed_id = 123

        # test
        res = RoleManager.delete_role(not_existed_id)

        # assert
        self.assertIsNone(res)
