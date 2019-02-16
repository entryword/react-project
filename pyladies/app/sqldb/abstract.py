class SQLDatabaseAPI():
    def __init__(self, session):
        self.session = session

    ########## create

    def create_topic(self, info, autocommit=False):
        raise NotImplementedError()

    def create_event_basic(self, info, autocommit=False):
        raise NotImplementedError()

    def create_event_info(self, info, autocommit=False):
        raise NotImplementedError()

    def create_place(self, info, autocommit=False):
        raise NotImplementedError()

    # def create_slide_resource(self, info, autocommit=False):
    #     raise NotImplementedError()

    def create_speaker(self, info, autocommit=False):
        raise NotImplementedError()

    def create_event_apply(self, info, autocommit=False):
        raise NotImplementedError()

    ########## get
    def get_topics(self):
        raise NotImplementedError()

    def get_topic(self, sn):
        raise NotImplementedError()

    def get_topic_by_name(self, name):
        raise NotImplementedError()

    # def get_event_basics(self):
    #     raise NotImplementedError()

    def get_event_basic(self, sn):
        raise NotImplementedError()

    def get_event_info(self, sn):
        raise NotImplementedError()

    def get_event_info_by_event_basic_sn(self, event_basic_sn):
        raise NotImplementedError()

    # def get_slide_resource(self, sn):
    #     raise NotImplementedError()

    def get_speakers(self):
        raise NotImplementedError()

    def get_speaker(self, sn):
        raise NotImplementedError()

    def get_event_apply_by_event_basic_sn(self, event_basic_sn):
        raise NotImplementedError()

    def get_event_apply(self, sn):
        raise NotImplementedError()

    ########## update

    def update_topic(self, sn, info, autocommit=False):
        raise NotImplementedError()

    def update_event_basic(self, sn, info, autocommit=False):
        raise NotImplementedError()

    def update_event_info(self, sn, info, autocommit=False):
        raise NotImplementedError()

    # def update_slide_resource(self, sn, info, autocommit=False):
    #     raise NotImplementedError()

    def update_speaker(self, sn, info, autocommit=False):
        raise NotImplementedError()

    def update_event_apply(self, sn, info, autocommit=False):
        raise NotImplementedError()

    ########## delete

    def delete_topic(self, sn, autocommit=False):
        raise NotImplementedError()

    def delete_event_basic(self, sn, autocommit=False):
        raise NotImplementedError()

    def delete_event_info(self, sn, autocommit=False):
        raise NotImplementedError()

    def delete_slide_resource(self, sn, autocommit=False):
        raise NotImplementedError()

    def delete_speaker(self, sn, autocommit=False):
        raise NotImplementedError()

    def delete_event_apply(self, sn, autocommit=False):
        raise NotImplementedError()
