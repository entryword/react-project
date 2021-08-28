import pytest

from sqlalchemy.exc import IntegrityError

from app import create_app
from app.exceptions import PyLadiesException
from app.exceptions import TOPIC_NOT_EXIST
from app.sqldb import DBWrapper

class TestTopic:
    def setup(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.db.create_all()

    def teardown(self):
        self.app.db.session.remove()
        self.app.db.drop_all()
        self.app.db.engine.dispose()
        self.app_context.pop()

    @staticmethod
    def assert_topic(tp1, tp2):
        assert tp1.name == tp2["name"]
        assert tp1.desc == tp2["desc"]
        assert tp1.freq == tp2["freq"]
        assert tp1.level == tp2["level"]
        assert tp1.host == tp2["host"]
        assert tp1.fields == tp2["fields"]

    @staticmethod
    def assert_topic_name(tp1, tp2):
        assert tp1.name == tp2["name"]

    @staticmethod
    def assert_topics_length(topics, length):
        assert len(topics) == length

    @staticmethod
    def assert_exception(ex1, ex2):
        assert ex1 == ex2

    def test_create_topic(self, topic_info):
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)

            # test
            manager.create_topic(topic_info, autocommit=True)

            # assertion
            topic = manager.get_topic_by_name(topic_info["name"])
            self.assert_topic(topic, topic_info)

    @pytest.mark.parametrize('topic_infos', [2], indirect=True)
    def test_unique_topic_name(self, topic_infos):
        info_1 = topic_infos[0]
        info_2 = topic_infos[1]
        info_2["name"] = info_1["name"]
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

    @pytest.mark.parametrize('topic_infos', [2], indirect=True)
    def test_update_topic_with_same_topic_name(self, topic_infos):
        info_1 = topic_infos[0]
        info_2 = topic_infos[1]
        info_2["name"] = info_1["name"]
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(info_1, autocommit=True)

            # test
            manager.update_topic(1, info_2, autocommit=True)

            # assertion
            topic = manager.get_topic(1)
            self.assert_topic(topic, info_2)

    @pytest.mark.parametrize('topic_infos', [4], indirect=True)
    def test_update_topic_with_different_topic_name(self, topic_infos):
        info_1 = topic_infos[0]
        info_2 = topic_infos[1]
        new_info_un = topic_infos[2]
        new_info_dp = topic_infos[3]
        new_info_dp["name"] = info_2["name"]
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
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])

            # test
            manager.delete_topic(topic.id, autocommit=True)

            # assertion
            with pytest.raises(PyLadiesException) as cm:
                manager.get_topic_by_name(topic_info["name"])
            self.assert_exception(cm.value, TOPIC_NOT_EXIST)

    def test_get_topic_by_name(self, topic_info):
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)

            # test & assertion 1
            topic = manager.get_topic_by_name(topic_info["name"])
            self.assert_topic_name(topic, topic_info)

            # test & assertion 2
            with pytest.raises(PyLadiesException) as cm:
                manager.get_topic_by_name("topic 2")
            self.assert_exception(cm.value, TOPIC_NOT_EXIST)

    def test_get_topic_by_id(self, topic_info):
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)

            # test & assertion 1
            topic = manager.get_topic(1)
            self.assert_topic_name(topic, topic_info)

            # test & assertion 2
            with pytest.raises(PyLadiesException) as cm:
                manager.get_topic(2)
            self.assert_exception(cm.value, TOPIC_NOT_EXIST)

    @pytest.mark.parametrize('topic_infos', [2], indirect=True)
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

    @pytest.mark.parametrize('topic_infos', [3], indirect=True)
    def test_get_topics_by_keyword(self, topic_infos):
        info_1 = topic_infos[0]
        info_1["name"] = "abc 1"
        info_2 = topic_infos[1]
        info_2["name"] = "def 2"
        info_3 = topic_infos[2]
        info_3["name"] = "efg 1"
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(info_1, autocommit=True)
            manager.create_topic(info_2, autocommit=True)
            manager.create_topic(info_3, autocommit=True)

            # test & assertion 1
            topics = manager.search_topics("b")
            self.assert_topics_length(topics, 1)
            self.assert_topic_name(topics[0], info_1)

            # test & assertion 2
            topics = manager.search_topics("ef")
            self.assert_topics_length(topics, 2)
            self.assert_topic_name(topics[0], info_2)
            self.assert_topic_name(topics[1], info_3)
    @pytest.mark.parametrize('topic_infos', [2], indirect=True)
    def test_get_topics_by_level(self, topic_infos):
        info_1 = topic_infos[0]
        info_1["level"] = 0
        info_2 = topic_infos[1]
        info_2["level"] = 1
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(info_1, autocommit=True)
            manager.create_topic(info_2, autocommit=True)

            # test & assertion 1
            topics = manager.search_topics("", "0")
            self.assert_topics_length(topics, 1)
            self.assert_topic(topics[0], info_1)

            # test & assertion 2
            topics = manager.search_topics("", 1)
            self.assert_topics_length(topics, 1)
            self.assert_topic(topics[0], info_2)
    @pytest.mark.parametrize('topic_infos', [2], indirect=True)
    def test_get_topics_by_freq(self, topic_infos):
        info_1 = topic_infos[0]
        info_1["freq"] = 0
        info_2 = topic_infos[1]
        info_2["freq"] = 1
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(info_1, autocommit=True)
            manager.create_topic(info_2, autocommit=True)

            # test & assertion 1
            topics = manager.search_topics("", None, "0")
            self.assert_topics_length(topics, 1)
            self.assert_topic(topics[0], info_1)

            # test & assertion 2
            topics = manager.search_topics("", None, 1)
            self.assert_topics_length(topics, 1)
            self.assert_topic(topics[0], info_2)

    @pytest.mark.parametrize('topic_infos', [2], indirect=True)
    def test_get_topics_by_host(self, topic_infos):
        info_1 = topic_infos[0]
        info_1["host"] = 0
        info_2 = topic_infos[1]
        info_2["host"] = 1
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(info_1, autocommit=True)
            manager.create_topic(info_2, autocommit=True)

            # test & assertion 1
            topics = manager.search_topics("", None, None, "0")
            self.assert_topics_length(topics, 1)
            self.assert_topic(topics[0], info_1)

            # test & assertion 2
            topics = manager.search_topics("", None, None, 1)
            self.assert_topics_length(topics, 1)
            self.assert_topic(topics[0], info_2)
    @pytest.mark.parametrize('topic_infos', [2], indirect=True)
    def test_get_topics_by_level_host(self, topic_infos):
        info_1 = topic_infos[0]
        info_1["level"] = 1
        info_1["host"] = 0
        info_2 = topic_infos[1]
        info_2["level"] = 1
        info_2["host"] = 1
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(info_1, autocommit=True)
            manager.create_topic(info_2, autocommit=True)

            # test & assertion 1
            topics = manager.search_topics("", None, None, "0")
            self.assert_topics_length(topics, 1)
            self.assert_topic(topics[0], info_1)

            # test & assertion 2
            topics = manager.search_topics("", 1, None, 1)
            self.assert_topics_length(topics, 1)
            self.assert_topic(topics[0], info_2)

            # test & assertion 2
            topics = manager.search_topics("", 1, None, 2)
            self.assert_topics_length(topics, 0)
    @pytest.mark.parametrize('topic_infos', [2], indirect=True)
    def test_get_topics_by_keyword_level_host(self, topic_infos):
        info_1 = topic_infos[0]
        info_1["name"] = "abcd"
        info_1["level"] = 1
        info_1["host"] = 0
        info_2 = topic_infos[1]
        info_2["name"] = "def 2"
        info_2["level"] = 1
        info_2["host"] = 1
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(info_1, autocommit=True)
            manager.create_topic(info_2, autocommit=True)

            # test & assertion 1
            topics = manager.search_topics("b", None, None, "0")
            self.assert_topics_length(topics, 1)
            self.assert_topic(topics[0], info_1)

            # test & assertion 2
            topics = manager.search_topics("d", 1)
            self.assert_topics_length(topics, 2)
            self.assert_topic(topics[0], info_1)
            self.assert_topic(topics[1], info_2)

            # test & assertion 2
            topics = manager.search_topics("d", None, None, 2)
            self.assert_topics_length(topics, 0)

