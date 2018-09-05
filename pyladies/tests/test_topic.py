import unittest

from sqlalchemy.exc import IntegrityError

from app import create_app
from app.exceptions import PyLadiesException
from app.exceptions import TOPIC_NOT_EXIST
from app.sqldb import DBWrapper


class TopicTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.db.create_all()

    def tearDown(self):
        self.app.db.session.remove()
        self.app.db.drop_all()
        self.app_context.pop()

    def test_create_topic(self):
        info = {
            "name": "topic 1",
            "desc": "This is description",
            "freq": 0,
            "level": 1,
            "host": 0,
            "fields": [0, 1, 2]
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)

            # test
            manager.create_topic(info, autocommit=True)

            # assertion
            topic = manager.get_topic_by_name(info["name"])
            self.assertEquals(topic.name, info["name"])
            self.assertEquals(topic.desc, info["desc"])
            self.assertEquals(topic.freq, info["freq"])
            self.assertEquals(topic.level, info["level"])
            self.assertEquals(topic.host, info["host"])
            self.assertEquals(topic.fields, info["fields"])

    def test_unique_topic_name(self):
        info_1 = {
            "name": "topic 1",
            "desc": "This is description 1",
            "freq": 0,
            "level": 1,
            "host": 0,
            "fields": [0, 1, 2]
        }
        info_2 = {
            "name": "topic 1",
            "desc": "This is description 2",
            "freq": 0,
            "level": 1,
            "host": 0,
            "fields": [0, 1, 2]
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)

            # test
            manager.create_topic(info_1, autocommit=True)

            # assertion
            with self.assertRaises(IntegrityError) as cm:
                manager.create_topic(info_2, autocommit=True)
            error_msg = str(cm.exception)
            self.assertIn("duplicate", error_msg.lower())

    def test_update_topic_with_same_topic_name(self):
        info = {
            "name": "topic 1",
            "desc": "This is description",
            "freq": 0,
            "level": 1,
            "host": 0,
            "fields": [0, 1, 2]
        }
        new_info = {
            "name": "topic 1",
            "desc": "This is description 2",
            "freq": 0,
            "level": 2,
            "host": 0,
            "fields": [1, 2]
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(info, autocommit=True)

            # test
            manager.update_topic(1, new_info, autocommit=True)

            # assertion
            topic = manager.get_topic(1)
            self.assertEquals(topic.name, new_info["name"])
            self.assertEquals(topic.desc, new_info["desc"])
            self.assertEquals(topic.freq, new_info["freq"])
            self.assertEquals(topic.level, new_info["level"])
            self.assertEquals(topic.host, new_info["host"])
            self.assertEquals(topic.fields, new_info["fields"])

    def test_update_topic_with_different_topic_name(self):
        info_1 = {
            "name": "topic 1",
            "desc": "This is description",
            "freq": 0,
            "level": 1,
            "host": 0,
            "fields": [0, 1, 2]
        }
        info_2 = {
            "name": "topic 2",
            "desc": "This is description",
            "freq": 0,
            "level": 1,
            "host": 0,
            "fields": [0, 1, 2]
        }
        new_info_dp = {
            "name": "topic 2",
            "desc": "This is description 2",
            "freq": 0,
            "level": 2,
            "host": 0,
            "fields": [1, 2]
        }
        new_info_un = {
            "name": "topic 3",
            "desc": "This is description 2",
            "freq": 0,
            "level": 2,
            "host": 0,
            "fields": [1, 2]
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(info_1, autocommit=True)
            manager.create_topic(info_2, autocommit=True)

            # test & assertion 1
            manager.update_topic(1, new_info_un, autocommit=True)
            topic = manager.get_topic(1)
            self.assertEquals(topic.name, new_info_un["name"])
            self.assertEquals(topic.desc, new_info_un["desc"])
            self.assertEquals(topic.freq, new_info_un["freq"])
            self.assertEquals(topic.level, new_info_un["level"])
            self.assertEquals(topic.host, new_info_un["host"])
            self.assertEquals(topic.fields, new_info_un["fields"])

            # test & assertion 2
            with self.assertRaises(IntegrityError) as cm:
                manager.update_topic(1, new_info_dp, autocommit=True)
            error_msg = str(cm.exception)
            self.assertIn("duplicate", error_msg.lower())

    def test_delete_topic(self):
        info = {
            "name": "topic 1",
            "desc": "This is description",
            "freq": 0,
            "level": 1,
            "host": 0,
            "fields": [0, 1, 2]
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(info, autocommit=True)
            topic = manager.get_topic_by_name(info["name"])
            
            # test
            manager.delete_topic(topic.sn, autocommit=True)

            # assertion
            with self.assertRaises(PyLadiesException) as cm:
                manager.get_topic_by_name(info["name"])
            self.assertEquals(cm.exception, TOPIC_NOT_EXIST)

    def test_get_topic_by_name(self):
        info = {
            "name": "topic 1",
            "desc": "This is description",
            "freq": 0,
            "level": 1,
            "host": 0,
            "fields": [0, 1, 2]
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(info, autocommit=True)

            # test & assertion 1
            topic = manager.get_topic_by_name(info["name"])
            self.assertEquals(topic.name, info["name"])

            # test & assertion 2
            with self.assertRaises(PyLadiesException) as cm:
                manager.get_topic_by_name("topic 2")
            self.assertEquals(cm.exception, TOPIC_NOT_EXIST)

    def test_get_topic_by_sn(self):
        info = {
            "name": "topic 1",
            "desc": "This is description",
            "freq": 0,
            "level": 1,
            "host": 0,
            "fields": [0, 1, 2]
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(info, autocommit=True)

            # test & assertion 1
            topic = manager.get_topic(1)
            self.assertEquals(topic.name, info["name"])

            # test & assertion 2
            with self.assertRaises(PyLadiesException) as cm:
                manager.get_topic(2)
            self.assertEquals(cm.exception, TOPIC_NOT_EXIST)

    def test_get_topics(self):
        info_1 = {
            "name": "topic 1",
            "desc": "This is description",
            "freq": 0,
            "level": 1,
            "host": 0,
            "fields": [0, 1, 2]
        }
        info_2 = {
            "name": "topic 2",
            "desc": "This is description",
            "freq": 1,
            "level": 2,
            "host": 1,
            "fields": [3]
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(info_1, autocommit=True)
            manager.create_topic(info_2, autocommit=True)

            # test
            topics = manager.get_topics()

            # assertion
            self.assertEquals(len(topics), 2)
            self.assertEquals(topics[0].name, info_1["name"])
            self.assertEquals(topics[1].name, info_2["name"])

    def test_get_topics_by_keyword(self):
        info_1 = {
            "name": "abc 1",
            "desc": "This is description",
            "freq": 0,
            "level": 1,
            "host": 0,
            "fields": [0, 1, 2]
        }
        info_2 = {
            "name": "def 2",
            "desc": "This is description",
            "freq": 1,
            "level": 2,
            "host": 1,
            "fields": [3]
        }
        info_3 = {
            "name": "efg 1",
            "desc": "This is description",
            "freq": 0,
            "level": 1,
            "host": 0,
            "fields": [0, 1, 2]
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(info_1, autocommit=True)
            manager.create_topic(info_2, autocommit=True)
            manager.create_topic(info_3, autocommit=True)

            # test & assertion 1
            topics = manager.get_topics_by_keyword("b")
            self.assertEquals(len(topics), 1)
            self.assertEquals(topics[0].name, info_1["name"])

            # test & assertion 2
            topics = manager.get_topics_by_keyword("ef")
            self.assertEquals(len(topics), 2)
            self.assertEquals(topics[0].name, info_2["name"])
            self.assertEquals(topics[1].name, info_3["name"])
