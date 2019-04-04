import pytest

from sqlalchemy.exc import IntegrityError

from app import create_app
from app.exceptions import PyLadiesException
from app.exceptions import TOPIC_NOT_EXIST
from app.sqldb import DBWrapper


class TestTopic:
    def setup_method(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.db.create_all()

    def teardown_method(self):
        self.app.db.session.remove()
        self.app.db.drop_all()
        self.app_context.pop()

    def assert_topic(self, foo, bar):
        assert foo.name == bar["name"]
        assert foo.desc == bar["desc"]
        assert foo.freq == bar["freq"]
        assert foo.level == bar["level"]
        assert foo.host == bar["host"]
        assert foo.fields == bar["fields"]

    def assert_topic_name(self, foo, bar):
        assert foo.name == bar["name"]

    def assert_topics_length(self, topics, length):
        assert len(topics) == length

    def assert_topic_exception(self, foo, bar):
        assert foo == bar

    def test_create_topic(self, topic_info):
        info = topic_info
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)

            # test
            manager.create_topic(info, autocommit=True)

            # assertion
            topic = manager.get_topic_by_name(info["name"])
            self.assert_topic(topic, info)

    @pytest.mark.parametrize('topic_infos', [[2]], indirect=True)
    def test_unique_topic_name(self, topic_infos):
        info_1 = topic_infos[0]
        info_2 = topic_infos[1]
        info_2.update({"name": "topic 1"})
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)

            # test
            manager.create_topic(info_1, autocommit=True)

            # assertion
            with pytest.raises(IntegrityError) as cm:
                manager.create_topic(info_2, autocommit=True)
            error_msg = str(cm.value)
            assert "duplicate" in error_msg.lower()

    @pytest.mark.parametrize('topic_infos', [[2]], indirect=True)
    def test_update_topic_with_same_topic_name(self, topic_infos):
        info_1 = topic_infos[0]
        info_2 = topic_infos[1]
        info_2.update({"name": "topic 1"})
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(info_1, autocommit=True)

            # test
            manager.update_topic(1, info_2, autocommit=True)

            # assertion
            topic = manager.get_topic(1)
            self.assert_topic(topic, info_2)

    @pytest.mark.parametrize('topic_infos', [[4]], indirect=True)
    def test_update_topic_with_different_topic_name(self, topic_infos):
        info_1 = topic_infos[0]
        info_2 = topic_infos[1]
        new_info_un = topic_infos[2]
        new_info_dp = topic_infos[3]
        new_info_dp.update({"name": "topic 2"})

        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(info_1, autocommit=True)
            manager.create_topic(info_2, autocommit=True)

            # test & assertion 1
            manager.update_topic(1, new_info_un, autocommit=True)
            topic = manager.get_topic(1)
            self.assert_topic(topic, new_info_un)

            # test & assertion 2
            with pytest.raises(IntegrityError) as cm:
                manager.update_topic(1, new_info_dp, autocommit=True)
            error_msg = str(cm.value)
            assert "duplicate" in error_msg.lower()

    def test_delete_topic(self, topic_info):
        info = topic_info
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(info, autocommit=True)
            topic = manager.get_topic_by_name(info["name"])

            # test
            manager.delete_topic(topic.sn, autocommit=True)

            # assertion
            with pytest.raises(PyLadiesException) as cm:
                manager.get_topic_by_name(info["name"])
            self.assert_topic_exception(cm.value, TOPIC_NOT_EXIST)

    def test_get_topic_by_name(self, topic_info):
        info = topic_info
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(info, autocommit=True)

            # test & assertion 1
            topic = manager.get_topic_by_name(info["name"])
            self.assert_topic_name(topic, info)

            # test & assertion 2
            with pytest.raises(PyLadiesException) as cm:
                manager.get_topic_by_name("topic 2")
            self.assert_topic_exception(cm.value, TOPIC_NOT_EXIST)

    def test_get_topic_by_sn(self, topic_info):
        info = topic_info
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(info, autocommit=True)

            # test & assertion 1
            topic = manager.get_topic(1)
            self.assert_topic_name(topic, info)

            # test & assertion 2
            with pytest.raises(PyLadiesException) as cm:
                manager.get_topic(2)
            self.assert_topic_exception(cm.value, TOPIC_NOT_EXIST)

    @pytest.mark.parametrize('topic_infos', [[2]], indirect=True)
    def test_get_topics(self, topic_infos):
        info_1 = topic_infos[0]
        info_2 = topic_infos[1]
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(info_1, autocommit=True)
            manager.create_topic(info_2, autocommit=True)

            # test
            topics = manager.get_topics()

            # assertion
            self.assert_topics_length(topics, 2)
            self.assert_topic_name(topics[0], info_1)
            self.assert_topic_name(topics[1], info_2)

    @pytest.mark.parametrize('topic_infos', [[3]], indirect=True)
    def test_get_topics_by_keyword(self, topic_infos):
        info_1 = topic_infos[0]
        info_1.update({"name": "abc 1"})
        info_2 = topic_infos[1]
        info_2.update({"name": "def 2"})
        info_3 = topic_infos[2]
        info_3.update({"name": "efg 1"})
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(info_1, autocommit=True)
            manager.create_topic(info_2, autocommit=True)
            manager.create_topic(info_3, autocommit=True)

            # test & assertion 1
            topics = manager.get_topics_by_keyword("b")
            self.assert_topics_length(topics, 1)
            self.assert_topic_name(topics[0], info_1)

            # test & assertion 2
            topics = manager.get_topics_by_keyword("ef")
            self.assert_topics_length(topics, 2)
            self.assert_topic_name(topics[0], info_2)
            self.assert_topic_name(topics[1], info_3)
