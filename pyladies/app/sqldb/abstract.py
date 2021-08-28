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

    def create_role(self, info, autocommit=False):
        raise NotImplementedError()

    def create_check_in_list(self, info, autocommit=False, flush=False):
        raise NotImplementedError()

    def create_user(self, info, autocommit=False, flush=False):
        raise NotImplementedError()

    ########## get
    def get_topics(self):
        raise NotImplementedError()

    def get_topic(self, id):
        raise NotImplementedError()

    def get_topic_by_name(self, name):
        raise NotImplementedError()

    # def get_event_basics(self):
    #     raise NotImplementedError()

    def get_event_basic(self, id):
        raise NotImplementedError()

    def get_event_info(self, id):
        raise NotImplementedError()

    # def get_event_info_by_event_basic_id(self, event_basic_id):
    #     raise NotImplementedError()

    def get_slide_resource(self, id):
        raise NotImplementedError()

    def get_speakers(self):
        raise NotImplementedError()

    def get_speaker(self, id):
        raise NotImplementedError()

    def get_event_apply_by_event_basic_id(self, event_basic_id):
        raise NotImplementedError()

    def get_event_apply(self, id):
        raise NotImplementedError()

    def get_user_by_name(self, name):
        raise NotImplementedError()

    def get_all_users(self):
        raise NotImplementedError()

    def get_users_by_emails(self, emails):
        raise NotImplementedError()

    def get_roles(self):
        raise NotImplementedError()

    def get_role(self, id):
        raise NotImplementedError()

    def get_check_in_list(self, event_basic_id):
        raise NotImplementedError()

    def get_check_in_list_by_event_basic_id_and_email(self, event_basic_id, email):
        raise NotImplementedError()

    ########## update

    def update_topic(self, id, info, autocommit=False):
        raise NotImplementedError()

    def update_event_basic(self, id, info, autocommit=False):
        raise NotImplementedError()

    def update_event_info(self, id, info, autocommit=False):
        raise NotImplementedError()

    # def update_slide_resource(self, id, info, autocommit=False):
    #     raise NotImplementedError()

    def update_speaker(self, id, info, autocommit=False):
        raise NotImplementedError()

    def update_event_apply(self, id, info, autocommit=False):
        raise NotImplementedError()

    def update_role(self, id, info, autocommit=False):
        raise NotImplementedError()

    ########## delete

    def delete_topic(self, id, autocommit=False):
        raise NotImplementedError()

    def delete_event_basic(self, id, autocommit=False):
        raise NotImplementedError()

    def delete_event_info(self, id, autocommit=False):
        raise NotImplementedError()

    def delete_slide_resource(self, id, autocommit=False):
        raise NotImplementedError()

    def delete_speaker(self, id, autocommit=False):
        raise NotImplementedError()

    def delete_event_apply(self, id, autocommit=False):
        raise NotImplementedError()

    def delete_role(self, id, autocommit=False):
        raise NotImplementedError()

    def delete_check_in_list(self, id, autocommit=False):
        raise NotImplementedError()
