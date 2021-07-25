# coding=UTF-8

from flask import session
import pytest

from app import create_app
from app.managers.member import Manager as MemberManager
from app.sqldb import DBWrapper


class TestMemberApi:
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

    def _login(self, login_info):
        self.test_client.get(f"/v1.0/api/auth?email={login_info['mail']}&name={login_info['name']}")

    def test_get_member(self, member_info):
        self._create_member(member_info)
        self._login(member_info)

        with self.test_client as c:
            rv = c.get('/v1.0/api/member/me')

            assert rv.json['info']['code'] == 0
            assert rv.json['data']['name'] == member_info['name']
            assert rv.json['data']['mail'] == member_info['mail']
            assert rv.json['data']['first_time_login'] is False
            assert session['first_time_login'] is False

    def test_get_member_with_first_time_login(self, member_info):
        self._login(member_info)

        with self.test_client as c:
            rv = c.get('/v1.0/api/member/me')

            assert rv.json['info']['code'] == 0
            assert rv.json['data']['name'] == member_info['name']
            assert rv.json['data']['mail'] == member_info['mail']
            assert rv.json['data']['first_time_login'] is True
            assert session['first_time_login'] is False

    def test_get_member_without_login(self):
        rv = self.test_client.get('/v1.0/api/member/me')

        assert rv.json['info']['code'] == 1702

    @pytest.mark.parametrize('member_infos', [2], indirect=True)
    def test_update_member(self, member_infos):
        m_id = self._create_member(member_infos[0])
        self._login(member_infos[0])

        rv = self.test_client.put('/v1.0/api/member/me', json=member_infos[1])
        member_info = MemberManager.get_member(m_id)

        assert rv.json['info']['code'] == 0
        assert rv.json['data']['id'] == m_id

        assert member_info['mail'] == member_infos[0]['mail']
        assert member_info['name'] == member_infos[1]['name']
        assert member_info['is_student'] == member_infos[1]['is_student']
        assert member_info['title'] == member_infos[1]['title']
        assert member_info['fields'] == member_infos[1]['fields']

    def test_update_member_without_login(self, member_info):
        rv = self.test_client.put('/v1.0/api/member/me', json=member_info)

        assert rv.json['info']['code'] == 1702
