# coding=UTF-8

import json
import unittest

from jsonschema.exceptions import ValidationError

from app import create_app
from app.exceptions import PyLadiesException, INVALID_INPUT, ROLE_NAME_DUPLICATE, ROLE_NOT_EXIST
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
            return r1.sn

    def test_get_roles(self):
        # preparation
        r1_sn = self._create_test_role_basic()
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
                    'id': r1_sn,
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
                    'id': r2.sn,
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
        r1_sn = self._create_test_role_basic()

        # test
        res = RoleManager.get_role(r1_sn)

        # assert
        self.assertEqual({
            'id': r1_sn,
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
        not_existed_sn = 123

        # test and assert
        with self.assertRaises(PyLadiesException) as cm:
            RoleManager.get_role(not_existed_sn)
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
        sn = RoleManager.create_role(role_info)

        # assert
        self.assertIsNotNone(sn)

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

    def test_create_role_schema_error_key(self):
        with self.assertRaises(ValidationError):
            RoleManager.create_role({
                "name": "role",
                "permission": {"feat1": 1, "feat2": 2}
            })

    def test_create_role_schema_error_value(self):
        with self.assertRaises(ValidationError):
            RoleManager.create_role({
                "name": "role",
                "permission": {
                    "EventList": 3,  # should not over than 2 or less than 0
                    "Event": 2,
                    "EventRegister": 2,
                    "SpeakerList": 2,
                    "Speaker": 2,
                    "PlaceList": 1,
                    "Place": 1,
                    "UserList": 2,
                    "Role": 2
                }
            })

    def test_update_role(self):
        # preparation
        r1_sn = self._create_test_role_basic()
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
        res = RoleManager.update_role(r1_sn, update_role_info)

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
                RoleManager.update_role(r2.sn, update_r2_with_r1_name_info)
            self.assertEqual(cm.exception, ROLE_NAME_DUPLICATE)

    def test_update_role_id_not_found(self):
        # preparation
        not_existed_sn = 123
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
            RoleManager.update_role(not_existed_sn, update_role_info)
        self.assertEqual(cm.exception, ROLE_NOT_EXIST)

    def test_update_role_schema_error_key(self):
        # preparation
        r1_sn = self._create_test_role_basic()

        # test and assert
        with self.assertRaises(ValidationError):
            RoleManager.update_role(r1_sn, {
                "name": "role",
                "permission": {"feat3": 1, "feat4": 2}
            })

    def test_update_role_schema_error_value(self):
        # preparation
        r1_sn = self._create_test_role_basic()

        # test and assert
        with self.assertRaises(ValidationError):
            RoleManager.update_role(r1_sn, {
                "name": "role",
                "permission": {
                    "EventList": 3,  # should not over than 2  or less than 0
                    "Event": 2,
                    "EventRegister": 2,
                    "SpeakerList": 2,
                    "Speaker": 2,
                    "PlaceList": 1,
                    "Place": 1,
                    "UserList": 2,
                    "Role": 2
                }
            })

    def test_delete_role(self):
        # preparation
        r1_sn = self._create_test_role_basic()

        # test
        res = RoleManager.delete_role(r1_sn)

        # assert
        self.assertIsNone(res)

    def test_delete_role_id_not_found(self):
        # preparation
        not_existed_sn = 123

        # test
        res = RoleManager.delete_role(not_existed_sn)

        # assert
        self.assertIsNone(res)
