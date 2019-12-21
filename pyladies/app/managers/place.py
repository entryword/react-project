import json

from flask import current_app

from app.exceptions import PLACE_NAME_DUPLICATE
from app.sqldb import DBWrapper
from .abstract import BasePlaceManager


# TODO: error handling & input verification
class Manager(BasePlaceManager):
    @staticmethod
    def create_place(info):
        if not isinstance(info, dict):
            with open(info) as f:
                info = json.loads(f.read())

        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)

            try:
                manager.create_place(info, autocommit=True)
            except Exception as e:
                if "duplicate" in str(e).lower():
                    raise PLACE_NAME_DUPLICATE
                raise e

            place = manager.get_place_by_name(info["name"])
            return place.sn

    @staticmethod
    def update_place(sn, new_info):
        if not isinstance(new_info, dict):
            with open(new_info) as f:
                new_info = json.loads(f.read())

        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            try:
                manager.update_place(sn, new_info, autocommit=True)
            except Exception as e:
                if "duplicate" in str(e).lower():
                    raise PLACE_NAME_DUPLICATE
                raise e

    @staticmethod
    def list_places():
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            places = manager.get_places()
            for i in places:
                print(i)

    @staticmethod
    def get_places():
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            places = manager.get_places()

            places_list = []
            for place in places:
                data = {
                    "addr": place.addr,
                    "id": place.sn,
                    "name": place.name,
                    "map":place.map
                }
                places_list.append(data)
            return places_list

    @staticmethod
    def get_place(sn):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            place = manager.get_place(sn)


            data = {
                "addr": place.addr,
                "id": place.sn,
                "name": place.name,
                "map":place.map
            }
                
            return data
