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
            'id': record.sn,
            'event_basic_id': record.event_basic_sn,
            'user_id': record.user_sn,
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
    def upload(cls, event_basic_sn, files):
        stream = None
        if files[0].filename != '':
            file = files[0]
            stream = codecs.iterdecode(file.stream, 'utf-8')
        if not stream:
            raise FILE_REQUIRED
        old_results = cls.get_check_in_list(event_basic_sn=event_basic_sn)
        if old_results:
            raise RECORD_IS_EXIST
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            results = AccupassCsvProcessor(
                manager=manager, event_basic_sn=event_basic_sn, stream=stream
            ).get()
            return results

    @classmethod
    def create_check_in_list(cls, info):
        email = info['mail']
        event_basic_sn = info['event_basic_sn']
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            user_record = manager.get_check_in_list_by_event_basic_sn_and_email(
                event_basic_sn=event_basic_sn, email=email
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
                'user_sn': user_id
            })

            sn = manager.create_check_in_list(info=info, autocommit=True)
            return sn

    @classmethod
    def get_check_in_list(cls, event_basic_sn):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            records = manager.get_check_in_list(event_basic_sn=event_basic_sn)
            results = list()
            for record in records:
                data = cls._extract_schema(record=record)
                results.append(data)
            return results

    @classmethod
    def update_check_in_list(cls, check_in_list_sn, info):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            manager.update_check_in_list(
                check_in_list_sn=check_in_list_sn, info=info, autocommit=True)

    @staticmethod
    def delete_check_in_list(check_in_list_sn):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            manager.delete_check_in_list(sn=check_in_list_sn, autocommit=True)
