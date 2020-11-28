# coding=UTF-8

import json
import unittest

from app import create_app
from app.managers.user import Manager as UserManager
from app.sqldb import DBWrapper
from app.sqldb.models import User, Role


class UserManagerTestCase(unittest.TestCase):
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

    def test_get_all_users_with_role(self):
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            r1 = Role()
            r1.name = 'r1'
            r1.permission = {'feat1': 0, 'feat2': 1}
            db_sess.add(r1)
            db_sess.commit()

            r2 = Role()
            r2.name = 'r2'
            r2.permission = {'feat3': 2, 'feat2': 1}
            db_sess.add(r2)
            db_sess.commit()

            u = User()
            u.name = 'ut_name_u1'
            u.mail = 'ut_name_u1@pyladies.mail'
            u.roles.append(r1)
            u.roles.append(r2)

            db_sess.add(u)
            db_sess.commit()

            # assertion
            res = UserManager.get_all_users()

            self.assertEqual([{
                'name': 'ut_name_u1',
                'roles':[
                    {'name': 'r1', 'sn': r1.sn},
                    {'name': 'r2', 'sn': r2.sn}
                ],
                'status': 0,
                'sn': u.id
            }], res)
