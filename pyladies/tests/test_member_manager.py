# coding=UTF-8

from unittest import mock
import pytest

from app import create_app
from app.exceptions import PyLadiesException, MEMBER_NOT_EXIST, UNEXPECTED_ERROR
from app.managers.member import Manager as MemberManager
from app.sqldb import DBWrapper


class TestMemberManager:
    def setup(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.db.create_all()

    def teardown(self):
        self.app.db.session.remove()
        self.app.db.drop_all()
        self.app.db.engine.dispose()
        self.app_context.pop()

    @staticmethod
    def assert_member(m1, m2):
        assert m1['name'] == m2['name']
        assert m1['mail'] == m2['mail']
        assert m1['is_student'] == m2['is_student']
        assert m1['title'] == m2['title']
        assert m1['fields'] == m2['fields']

    def _create_members(self, member_infos):
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            m_ids = []

            for member_info in member_infos:
                m_id = manager.create_member(member_info, autocommit=True)
                m_ids.append(m_id)

            return m_ids

    def _get_first_member(self):
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)

            return manager.get_members()[0]

    @mock.patch('app.managers.member.login_user')
    def test_social_login_with_member_exists(self, mocked_login_user, member_info):
        self._create_members([member_info])
        new_created = MemberManager.social_login(member_info['mail'], member_info['name'])

        member = self._get_first_member()
        mocked_login_user.assert_called_once_with(member, False)
        assert new_created is False

    @mock.patch('app.managers.member.login_user')
    def test_social_login_without_member_exists(self, mocked_login_user, member_info):
        new_created = MemberManager.social_login(member_info['mail'], member_info['name'])

        member = self._get_first_member()
        mocked_login_user.assert_called_once_with(member, False)

        assert member.mail == member_info['mail']
        assert member.name == member_info['name']
        assert new_created is True

    @staticmethod
    @mock.patch('app.managers.member.login_user')
    def test_social_login_with_login_user_error(mocked_login_user, member_info):
        mocked_login_user.side_effect = UNEXPECTED_ERROR

        with pytest.raises(PyLadiesException) as cm:
            MemberManager.social_login(member_info['mail'], member_info['name'])
        assert cm.value == UNEXPECTED_ERROR

    @staticmethod
    @mock.patch('app.managers.member.logout_user')
    def test_logout(mocked_logout_user):
        MemberManager.logout()

        mocked_logout_user.assert_called_once()

    @pytest.mark.parametrize('member_infos', [3], indirect=True)
    def test_get_users(self, member_infos):
        self._create_members(member_infos)

        res = MemberManager.get_members()

        self.assert_member(res[0], member_infos[0])
        self.assert_member(res[1], member_infos[1])
        self.assert_member(res[2], member_infos[2])

    def test_get_member(self, member_info):
        m_ids = self._create_members([member_info])

        res = MemberManager.get_member(m_ids[0])

        self.assert_member(res, member_info)

    @staticmethod
    def test_get_member_without_member_exists():
        with pytest.raises(PyLadiesException) as cm:
            MemberManager.get_member(1)
        assert cm.value == MEMBER_NOT_EXIST

    @pytest.mark.parametrize('member_infos', [2], indirect=True)
    def test_update_member(self, member_infos):
        m_ids = self._create_members([member_infos[0]])

        MemberManager.update_member(m_ids[0], member_infos[1])

        res = MemberManager.get_member(m_ids[0])
        self.assert_member(res, member_infos[1])

    def test_delete_member(self, member_info):
        m_ids = self._create_members([member_info])

        MemberManager.delete_member(m_ids[0])

        with pytest.raises(PyLadiesException) as cm:
            MemberManager.get_member(m_ids[0])
        assert cm.value == MEMBER_NOT_EXIST
