# coding=UTF-8

import unittest

from app import create_app
from app.exceptions import PyLadiesException
from app.sqldb import DBWrapper


class EventApplyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.db.create_all()

    def tearDown(self):
        self.app.db.session.remove()
        self.app.db.drop_all()
        self.app_context.pop()

    def test_create_apply_info_and_event_apply(self):
        apply_info_1 = {
            "channel": 1,
            "type": "all",
            "price_default": 400,
            "price_student": 200,
            "url": "https://...",
            "qualification": "https://..."
        }

        apply_info_2 = {
            "channel": 0,
            "type": "one",
            "price_default": 100,
            "price_student": 50,
            "url": "https://...",
            "qualification": "https://..."
        }

        event_apply = {
            "event_basic_sn": 128,
            "host": "American Innovation Center 美國創新中心",
            "start_time": "2019-11-23 08:00",
            "end_time": "2019-12-01 23:00",
            "limit_gender": "限女",
            "limit_age": "不限",
            "limit_desc": "須上傳登錄成功截圖"
        }

        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            apply_info_list = []
            manager = self.app.db_api_class(db_sess)

            apply_info_1_sn = manager.create_apply_info(apply_info_1, autocommit=True)
            apply_info_1 = manager.get_apply_info(apply_info_1_sn)
            apply_info_list.append(str(apply_info_1_sn))

            apply_info_2_sn = manager.create_apply_info(apply_info_2, autocommit=True)
            apply_info_2 = manager.get_apply_info(apply_info_2_sn)
            apply_info_list.append(str(apply_info_2_sn))

            event_apply["apply_info_sn_list"] = ','.join(apply_info_list)

            manager.create_event_apply(event_apply, autocommit=True)
            event_apply = manager.get_event_apply_by_event_basic(128)

            # test & assertion
            self.assertEquals(apply_info_1.channel, 1)
            self.assertEquals(apply_info_2.channel, 0)
            self.assertEquals(event_apply.event_basic_sn, 128)
            self.assertEquals(event_apply.apply_info_sn_list, "1,2")


    def test_update_event_apply(self):
        apply_info_1 = {
            "channel": 1,
            "type": "all",
            "price_default": 400,
            "price_student": 200,
            "url": "https://...",
            "qualification": "https://..."
        }

        apply_info_2 = {
            "channel": 0,
            "type": "one",
            "price_default": 100,
            "price_student": 50,
            "url": "https://...",
            "qualification": "https://..."
        }

        event_apply = {
            "event_basic_sn": 128,
            "host": "American Innovation Center 美國創新中心",
            "start_time": "2019-11-23 08:00",
            "end_time": "2019-12-01 23:00",
            "limit_gender": "限女",
            "limit_age": "不限",
            "limit_desc": "須上傳登錄成功截圖"
        }

        event_apply_new = {
            "event_basic_sn": 127
        }

        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            apply_info_list = []
            manager = self.app.db_api_class(db_sess)

            apply_info_1_sn = manager.create_apply_info(apply_info_1, autocommit=True)
            apply_info_list.append(str(apply_info_1_sn))

            apply_info_2_sn = manager.create_apply_info(apply_info_2, autocommit=True)
            apply_info_list.append(str(apply_info_2_sn))

            event_apply["apply_info_sn_list"] = ','.join(apply_info_list)

            manager.create_event_apply(event_apply, autocommit=True)
            event_apply_before = manager.get_event_apply(1)
            sn_before = event_apply_before.event_basic_sn
            host_before = event_apply_before.host

            manager.update_event_apply(event_apply_before.sn, event_apply_new, autocommit=True)
            event_apply_after = manager.get_event_apply(1)
            sn_after = event_apply_after.event_basic_sn
            host_after = event_apply_after.host

            # test & assertion
            self.assertEquals(sn_before, 128)
            self.assertEquals(sn_after, 127)
            self.assertEquals(host_before, host_after)

    def test_update_apply_info(self):
        apply_info_1 = {
            "channel": 1,
            "type": "all",
            "price_default": 400,
            "price_student": 200,
            "url": "https://...",
            "qualification": "https://..."
        }

        apply_info_2 = {
            "channel": 0,
            "type": "one",
            "price_default": 100,
            "price_student": 50,
            "url": "https://...",
            "qualification": "https://..."
        }

        event_apply = {
            "event_basic_sn": 128,
            "host": "American Innovation Center 美國創新中心",
            "start_time": "2019-11-23 08:00",
            "end_time": "2019-12-01 23:00",
            "limit_gender": "限女",
            "limit_age": "不限",
            "limit_desc": "須上傳登錄成功截圖"
        }

        apply_info_new = {
            "type": "one"
        }

        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            apply_info_list = []
            manager = self.app.db_api_class(db_sess)

            apply_info_1_sn = manager.create_apply_info(apply_info_1, autocommit=True)
            apply_info_list.append(str(apply_info_1_sn))

            apply_info_2_sn = manager.create_apply_info(apply_info_2, autocommit=True)
            apply_info_list.append(str(apply_info_2_sn))

            event_apply["apply_info_sn_list"] = ','.join(apply_info_list)

            manager.create_event_apply(event_apply, autocommit=True)

            apply_info_before = manager.get_apply_info(1)

            type_before = apply_info_before.type
            channel_before = apply_info_before.channel

            manager.update_apply_info(apply_info_before.sn, apply_info_new, autocommit=True)
            apply_info_after = manager.get_apply_info(1)
            type_after = apply_info_after.type
            channel_after = apply_info_after.channel

            # test & assertion
            self.assertEquals(type_before, "all")
            self.assertEquals(type_after, "one")
            self.assertEquals(channel_before, channel_after)

    def test_delete_event_apply_and_apply_info(self):
        event_apply_1 = {
            "event_basic_sn": 128,
            "host": "American Innovation Center 美國創新中心",
            "start_time": "2019-11-23 08:00",
            "end_time": "2019-12-01 23:00",
            "limit_gender": "限女",
            "limit_age": "不限",
            "limit_desc": "須上傳登錄成功截圖"
        }

        event_apply_2 = {
            "event_basic_sn": 129,
            "host": "American Innovation Center 美國創新中心",
            "start_time": "2019-11-23 08:00",
            "end_time": "2019-12-01 23:00",
            "limit_gender": "限女",
            "limit_age": "不限",
            "limit_desc": "須上傳登錄成功截圖"
        }

        apply_info_1 = {
            "channel": 1,
            "type": "all",
            "price_default": 400,
            "price_student": 200,
            "url": "https://...",
            "qualification": "https://..."
        }

        apply_info_2 = {
            "channel": 0,
            "type": "one",
            "price_default": 100,
            "price_student": 50,
            "url": "https://...",
            "qualification": "https://..."
        }

        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)

            apply_info_list = []
            apply_info_1_sn = manager.create_apply_info(apply_info_1, autocommit=True)
            apply_info_list.append(str(apply_info_1_sn))

            event_apply_1["apply_info_sn_list"] = ','.join(apply_info_list)
            manager.create_event_apply(event_apply_1, autocommit=True)

            apply_info_list = []
            apply_info_2_sn = manager.create_apply_info(apply_info_2, autocommit=True)
            apply_info_list.append(str(apply_info_2_sn))

            event_apply_2["apply_info_sn_list"] = ','.join(apply_info_list)
            manager.create_event_apply(event_apply_2, autocommit=True)

            event_apply_1 = manager.get_event_apply_by_event_basic(128)
            event_apply_2 = manager.get_event_apply_by_event_basic(129)

            # test
            manager.delete_event_apply(event_apply_1.sn, autocommit=True)
            # TODO if delete_apply_info need to update event_apply.apply_info_sn_list
            # manager.delete_apply_info(apply_info_1.sn, autocommit=True)

            # assertion
            self.assertEquals(event_apply_2.event_basic_sn, 129)
            with self.assertRaises(Exception) as context:
                manager.get_event_apply_by_event_basic(128)
            self.assertEquals("Unable to perform the action. EventInfo doesn't exist.", str(context.exception))

            # TODO if delete_apply_info need to update event_apply.apply_info_sn_list
            # self.assertEquals(apply_info_2.sn, 2)
            # with self.assertRaises(Exception) as context:
            #     manager.get_apply_info(1)
            # self.assertEquals("Unable to perform the action. EventInfo doesn't exist.", str(context.exception))