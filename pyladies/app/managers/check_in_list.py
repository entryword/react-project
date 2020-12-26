from flask import current_app

from app.common.accupass_reader import AccupassCsvProcessor
from app.exceptions import FILE_REQUIRED
from app.managers.abstract import BaseCheckInListManager
from app.sqldb import DBWrapper


class CheckInListManager(BaseCheckInListManager):

    @staticmethod
    def _extract_schema(record):
        schema = {
            'sn': record.sn,
            'event_basic_sn': record.event_basic_sn,
            'user_sn': record.user_sn,
            'name': record.name,
            'mail': record.mail,
            'phone': record.phone,
            'ticket_type': record.ticket_type,
            'ticket_amount': record.ticket_amount,
            'remark': record.remark,
            'status': record.status,
        }
        return schema

    @staticmethod
    def upload(event_basic_sn, csv_reader):
        if not csv_reader:
            raise FILE_REQUIRED
        results = AccupassCsvProcessor(
            event_basic_sn=event_basic_sn, csv_reader=csv_reader
        ).get()
        return results

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
    def update_check_in_list(cls, event_basic_sn, user_sn, info):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            record = manager.update_check_in_list(
                event_basic_sn=event_basic_sn, user_sn=user_sn, info=info, autocommit=True)
            return cls._extract_schema(record=record)

    @staticmethod
    def delete_check_in_list(check_in_list_sn):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            manager.delete_check_in_list(sn=check_in_list_sn, autocommit=True)
