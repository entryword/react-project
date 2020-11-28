# coding=UTF-8

import json
import unittest

from app import create_app
from app.exceptions import INVALID_INPUT, ROLE_NAME_DUPLICATE, ROLE_NOT_EXIST
from app.sqldb import DBWrapper


class TestRoleApis(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.db.create_all()
        self.test_client = self.app.test_client()
        self.basic_role_info = {
            "name": "role",
            "permission": {
                "EventList": 0,
                "Event": 1,
                "EventRegister": 1,
                "SpeakerList": 0,
                "Speaker": 2,
                "PlaceList": 1,
                "Place": 1,
                "UserList": 2,
                "Role": 2
            }
        }

    def tearDown(self):
        self.app.db.session.remove()
        self.app.db.drop_all()
        self.app.db.engine.dispose()
        self.app_context.pop()

    def _create_test_role_data(self, info):
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            role_sn = manager.create_role(info, autocommit=True)
            return role_sn

    def _check_data_existed(self, role_sn):
        existed = False
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            try:
                manager.get_role(role_sn)
                existed = True
            except:
                existed = False
        return existed

    def test_get_roles_empty_list(self):
        # case 1: empty list
        rv = self.test_client.get(
            "/cms/api/roles"
        )
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json["info"]["code"], 0)
        self.assertEqual(rv.json["data"], [])

    def test_get_roles(self):
        # case 2: 2 data
        role2_info = {
            "name": "role2",
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
        role_id1 = self._create_test_role_data(self.basic_role_info)
        role_id2 = self._create_test_role_data(role2_info)
        rv = self.test_client.get(
            "/cms/api/roles"
        )
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json["info"]["code"], 0)
        self.assertEqual(rv.json["data"], [
            {
                "id": role_id1,
                "name": "role",
                "permission": {
                    "EventList": 0,
                    "Event": 1,
                    "EventRegister": 1,
                    "SpeakerList": 0,
                    "Speaker": 2,
                    "PlaceList": 1,
                    "Place": 1,
                    "UserList": 2,
                    "Role": 2
                }
            }, {
                "id": role_id2,
                "name": "role2",
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
        ])

    def test_get_role(self):
        # case 1: 200
        role_id = self._create_test_role_data(self.basic_role_info)
        rv = self.test_client.get(
            "/cms/api/role/{role_id}".format(role_id=role_id)
        )
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json["info"]["code"], 0)
        self.assertEqual(rv.json["data"], {
            "id": role_id,
            "name": "role",
            "permission": {
                "EventList": 0,
                "Event": 1,
                "EventRegister": 1,
                "SpeakerList": 0,
                "Speaker": 2,
                "PlaceList": 1,
                "Place": 1,
                "UserList": 2,
                "Role": 2
            }
        })

    def test_get_role_id_not_found(self):
        # case 2: role id not found, still 200
        not_exist_role_id = 123
        rv = self.test_client.get(
            "/cms/api/role/{role_id}".format(role_id=not_exist_role_id)
        )
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json["info"]["code"], ROLE_NOT_EXIST.code)

    def test_create_role(self):
        # case 1: 200
        rv = self.test_client.post(
            "/cms/api/role",
            headers={"Content-Type": "application/json"},
            content_type="application/json",
            data=json.dumps(self.basic_role_info),
        )
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json["info"]["code"], 0)
        self.assertEqual(rv.json["data"], {
            "id": 1
        })

    def test_create_role_duplicate_role_name(self):
        # case 2: duplicate role name
        self._create_test_role_data(self.basic_role_info)
        duplicate_role_name_info = {
            "name": "role",
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
        rv = self.test_client.post(
            "/cms/api/role",
            headers={"Content-Type": "application/json"},
            content_type="application/json",
            data=json.dumps(duplicate_role_name_info),
        )
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json["info"]["code"], ROLE_NAME_DUPLICATE.code)

    def test_create_role_schema_error(self):
        # case 3: schema error, lacking keys in permission
        lack_role_info = {
            "name": "role2",
            "permission": {
                "EventList": 1,
                "Event": 0,
            }
        }
        rv = self.test_client.post(
            "/cms/api/role",
            headers={"Content-Type": "application/json"},
            content_type="application/json",
            data=json.dumps(lack_role_info),
        )
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json["info"]["code"], INVALID_INPUT.code)

    def test_update_role(self):
        # case 1: 200, normal case
        role_id = self._create_test_role_data(self.basic_role_info)
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
        rv = self.test_client.put(
            "/cms/api/role/{role_id}".format(role_id=str(role_id)),
            headers={"Content-Type": "application/json"},
            content_type="application/json",
            data=json.dumps(update_role_info),
        )
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json["info"]["code"], 0)

    def test_update_role_event_list_error(self):
        # case 1: 200, normal case
        role_id = self._create_test_role_data(self.basic_role_info)
        update_role_info = {
            "name": "now_role_name",
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
        }

        rv = self.test_client.put(
            "/cms/api/role/{role_id}".format(role_id=str(role_id)),
            headers={"Content-Type": "application/json"},
            content_type="application/json",
            data=json.dumps(update_role_info),
        )
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json["info"]["code"], 1)

    def test_update_role_duplicate_name(self):
        # case 2: 200, name duplicate with existed role
        role2_info = {
            "name": "role2",
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
        self._create_test_role_data(self.basic_role_info)
        role_id2 = self._create_test_role_data(role2_info)

        update_role2_with_role1_name = {
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
        rv = self.test_client.put(
            "/cms/api/role/{role_id}".format(role_id=str(role_id2)),
            headers={"Content-Type": "application/json"},
            content_type="application/json",
            data=json.dumps(update_role2_with_role1_name),
        )
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json["info"]["code"], ROLE_NAME_DUPLICATE.code)

    def test_update_role_id_not_found(self):
        # case 3: 200, id not existed
        not_exist_role_id = 123
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
        rv = self.test_client.put(
            "/cms/api/role/{role_id}".format(role_id=str(not_exist_role_id)),
            headers={"Content-Type": "application/json"},
            content_type="application/json",
            data=json.dumps(update_role_info),
        )
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json["info"]["code"], ROLE_NOT_EXIST.code)

    def test_update_role_schema_error(self):
        # case 4: 200, schema error, lacking keys in permission
        role_id = self._create_test_role_data(self.basic_role_info)
        lack_role_info = {
            "name": "role",
            "permission": {
                "EventList": 1,
                "Event": 0,
            }
        }
        rv = self.test_client.put(
            "/cms/api/role/{role_id}".format(role_id=str(role_id)),
            headers={"Content-Type": "application/json"},
            content_type="application/json",
            data=json.dumps(lack_role_info),
        )
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json["info"]["code"], INVALID_INPUT.code)

    def test_delete_role_id_not_found(self):
        # case 1: role id not found, still 200
        # get it first to confirm data not existed
        not_exist_role_id = 123
        self.assertFalse(self._check_data_existed(123))

        rv = self.test_client.delete(
            "/cms/api/role/{role_id}".format(role_id=not_exist_role_id)
        )
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json["info"]["code"], 0)

    def test_delete_role(self):
        # case 2: 200, normal case
        role_id = self._create_test_role_data(self.basic_role_info)
        rv = self.test_client.delete(
            "/cms/api/role/{role_id}".format(role_id=str(role_id))
        )
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json["info"]["code"], 0)
