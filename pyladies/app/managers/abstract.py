class BaseTopicManager(object):
    @staticmethod
    def create_topic(f):
        raise NotImplementedError()

    @staticmethod
    def update_topic(sn, f):
        raise NotImplementedError()

    @staticmethod
    def delete_topic(sn):
        raise NotImplementedError()

    @staticmethod
    def list_topics(key=None):
        raise NotImplementedError()


class BaseEventManager(object):
    @staticmethod
    def create_event(f):
        raise NotImplementedError()

    @staticmethod
    def update_event(sn, f):
        raise NotImplementedError()

    @staticmethod
    def delete_event(sn):
        raise NotImplementedError()

    @staticmethod
    def list_events(key=None):
        raise NotImplementedError()
