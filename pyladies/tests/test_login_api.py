# coding=UTF-8

from flask import session

from app import create_app
from app.sqldb import DBWrapper


class TestLoginApi:
    def setup(self):
        self.app = create_app('test2')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.db.create_all()
        self.test_client = self.app.test_client()

    def teardown(self):
        self.app.db.session.remove()
        self.app.db.drop_all()
        self.app.db.engine.dispose()
        self.app_context.pop()

    def _create_member(self, member_info):
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            m_id = manager.create_member(member_info, autocommit=True)

            return m_id

    def test_login(self):
        rv = self.test_client.get('/v1.0/api/login')

        assert rv.status_code == 302
        assert 'https://accounts.google.com/o/oauth2/auth' in rv.location

    def test_auth(self, member_info):
        self._create_member(member_info)

        with self.test_client as c:
            rv = c.get(f"/v1.0/api/auth?email={member_info['mail']}&name={member_info['name']}")

            assert session['user_type'] == 'Member'
            assert session['first_time_login'] is False
            assert rv.status_code == 302
            assert rv.location == 'http://localhost/'

    def test_auth_new_member(self, member_info):
        with self.test_client as c:
            rv = c.get(f"/v1.0/api/auth?email={member_info['mail']}&name={member_info['name']}")

            assert session['user_type'] == 'Member'
            assert session['first_time_login'] is True
            assert rv.status_code == 302
            assert rv.location == 'http://localhost/'

    def test_logout(self, member_info):
        self._create_member(member_info)
        self.test_client.get(
            f"/v1.0/api/auth?email={member_info['mail']}&name={member_info['name']}"
        )

        rv = self.test_client.get('/v1.0/api/logout')

        assert rv.status_code == 302
        assert rv.location == 'http://localhost/'

    def test_logout_without_login(self):
        rv = self.test_client.get('/v1.0/api/logout')

        assert rv.json['info']['code'] == 1702
