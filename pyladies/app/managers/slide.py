from flask import current_app

from app.sqldb import DBWrapper
from .abstract import BaseSlideManager


class Manager(BaseSlideManager):
    @staticmethod
    def list_slides():
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            slides = manager.get_slides()
            slide_data = []
            for slide in slides:
                data = {
                    "id": slide.sn,
                    "type": slide.type,
                    "title": slide.title,
                    "url": slide.url
                }
                slide_data.append(data)
            return slide_data
                