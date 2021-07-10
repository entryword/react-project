import pytest

from app import create_app
from app.exceptions import PyLadiesException
from app.exceptions import MEMBER_NOT_EXIST
from app.sqldb import DBWrapper
from app.sqldb.models import Member


class TestMember:
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
        assert m1.name == m2['name']
        assert m1.mail == m2['mail']
        assert m1.is_student == m2['is_student']
        assert m1.title == m2['title']
        assert m1.fields == m2['fields']

    @staticmethod
    def assert_exception(ex1, ex2):
        assert ex1 == ex2

    def test_create_member(self, member_info):
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)

            member_id = manager.create_member(member_info, autocommit=True)

            member = manager.get_members()[0]
            self.assert_member(member, member_info)
            assert member.id == member_id

    @pytest.mark.parametrize('member_infos', [3], indirect=True)
    def test_get_members(self, member_infos):
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            for member_info in member_infos:
                manager.create_member(member_info, autocommit=True)

            members = manager.get_members()

            for i in range(3):
                self.assert_member(members[i], member_infos[i])

    def test_get_member(self, member_info):
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            member_id = manager.create_member(member_info, autocommit=True)

            member = manager.get_member(member_id)

            self.assert_member(member, member_info)

    def test_get_member_record_not_exist(self, member_info):
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            member_id = manager.create_member(member_info, autocommit=True)

            with pytest.raises(PyLadiesException) as cm:
                manager.get_member(member_id + 1)

            self.assert_exception(cm.value, MEMBER_NOT_EXIST)

    def test_get_member_by_email(self, member_info):
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            manager.create_member(member_info, autocommit=True)

            member = manager.get_member_by_email('1@pyladies.tw')

            self.assert_member(member, member_info)

    def test_get_member_by_email_record_not_exist(self, member_info):
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            manager.create_member(member_info, autocommit=True)

            member = manager.get_member_by_email('2@pyladies.tw')

            assert member is None

    @pytest.mark.parametrize('member_infos', [2], indirect=True)
    def test_update_member(self, member_infos):
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            member_info, new_member_info = member_infos
            manager.create_member(member_info, autocommit=True)

            manager.update_member(1, new_member_info, autocommit=True)

            member = manager.get_member(1)
            self.assert_member(member, new_member_info)

    @pytest.mark.parametrize('member_infos', [2], indirect=True)
    def test_update_member_record_not_exist(self, member_infos):
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            member_info, new_member_info = member_infos
            manager.create_member(member_info, autocommit=True)

            with pytest.raises(PyLadiesException) as cm:
                manager.update_member(2, new_member_info, autocommit=True)

            self.assert_exception(cm.value, MEMBER_NOT_EXIST)

    def test_delete_member(self, member_info):
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            manager.create_member(member_info, autocommit=True)

            manager.delete_member(1, autocommit=True)

            member = db_sess.query(Member).filter_by(id=1).first()
            assert member is None

    def test_delete_member_record_not_exist(self, member_info):
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            manager.create_member(member_info, autocommit=True)

            manager.delete_member(2, autocommit=True)

            member = db_sess.query(Member).filter_by(id=2).first()
            assert member is None
