import codecs

from flask import current_app

from app.common.accupass_reader import AccupassCsvProcessor
from app.exceptions import FILE_REQUIRED, RECORD_IS_EXIST
from app.managers.abstract import BaseCheckInListManager
from app.sqldb import DBWrapper


class CheckInListManager(BaseCheckInListManager):

    @staticmethod
    def _extract_schema(record):
        schema = {
            'id': record.id,
            'event_basic_id': record.event_basic_id,
            'user_id': record.user_id,
            'name': record.name,
            'mail': record.mail,
            'phone': record.phone,
            'ticket_type': record.ticket_type,
            'ticket_amount': record.ticket_amount,
            'remark': record.remark,
            'status': record.status,
        }
        return schema

    @classmethod
    def upload(cls, event_basic_id, files):
        stream = None
        if files[0].filename != '':
            file = files[0]
            stream = codecs.iterdecode(file.stream, 'utf-8')
        if not stream:
            raise FILE_REQUIRED
        old_results = cls.get_check_in_list(event_basic_id=event_basic_id)
        if old_results:
            raise RECORD_IS_EXIST
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            results = AccupassCsvProcessor(
                manager=manager, event_basic_id=event_basic_id, stream=stream
            ).get()
            return results

    @classmethod
    def create_check_in_list(cls, info):
        email = info['mail']
        event_basic_id = info['event_basic_id']
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            user_record = manager.get_check_in_list_by_event_basic_id_and_email(
                event_basic_id=event_basic_id, email=email
            )
            if user_record:
                raise RECORD_IS_EXIST

            old_user = manager.get_user_by_email(email=email)
            if old_user:
                user_id = old_user.id
            else:
                user_info = {
                    'name': email,
                    'mail': email
                }
                user_id = manager.create_user(info=user_info, flush=True)

            info.update({
                'user_id': user_id
            })

            id = manager.create_check_in_list(info=info, autocommit=True)
            return id

    @classmethod
    def get_check_in_list(cls, event_basic_id):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            records = manager.get_check_in_list(event_basic_id=event_basic_id)
            results = list()
            for record in records:
                data = cls._extract_schema(record=record)
                results.append(data)
            return results

    @classmethod
    def update_check_in_list(cls, check_in_list_id, info):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            manager.update_check_in_list(
                check_in_list_id=check_in_list_id, info=info, autocommit=True)

    @staticmethod
    def delete_check_in_list(check_in_list_id):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            manager.delete_check_in_list(id=check_in_list_id, autocommit=True)
