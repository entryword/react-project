from flask import current_app
from flask_login import login_user, logout_user

from app.sqldb import DBWrapper
from .abstract import BaseMemberManager

class Manager(BaseMemberManager):
    @staticmethod
    def social_login(email, name):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            new_created = False
            member = manager.get_member_by_email(email)

            if not member:
                info = {
                    'mail': email,
                    'name': name
                }
                member_id = manager.create_member(info=info, autocommit=True)
                new_created = True
                member = manager.get_member(member_id)

            login_user(member, False)
            return new_created

    @staticmethod
    def logout():
        logout_user()

    @staticmethod
    def get_members():
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            members = manager.get_members()
            return list(map(Manager._get_member_info, members))

    @staticmethod
    def get_member(m_id):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            member = manager.get_member(m_id)
            return Manager._get_member_info(member)

    @staticmethod
    def update_member(m_id, info):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            manager.update_member(m_id, info, autocommit=True)

    @staticmethod
    def delete_member(m_id):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            manager.delete_member(m_id, autocommit=True)

    @staticmethod
    def _get_member_info(member):
        return {
            'id': member.id,
            'name': member.name,
            'mail': member.mail,
            'is_student': member.is_student,
            'title': member.title,
            'fields': member.fields,
        }
