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
                    "id": slide.id,
                    "type": slide.type,
                    "title": slide.title,
                    "url": slide.url
                }
                slide_data.append(data)
            return slide_data

    @staticmethod
    def create_slide(info):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            slide_id = manager.create_slide_resource(info, autocommit=True)
            return slide_id

    @staticmethod
    def get_slide(id):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            slide = manager.get_slide_resource(id)
            return slide
