class BaseTopicManager():
    @staticmethod
    def create_topic(file_path):
        raise NotImplementedError()

    @staticmethod
    def update_topic(id, file_path):
        raise NotImplementedError()

    @staticmethod
    def delete_topic(id):
        raise NotImplementedError()

    @staticmethod
    def list_topics(key=None):
        raise NotImplementedError()


class BaseEventManager():
    @staticmethod
    def create_event(info):
        raise NotImplementedError()

    @staticmethod
    def update_event(id, new_info):
        raise NotImplementedError()

    @staticmethod
    def delete_event(id):
        raise NotImplementedError()

    @staticmethod
    def list_events(topic_id):
        raise NotImplementedError()


class BasePlaceManager():
    @staticmethod
    def create_place(info):
        raise NotImplementedError()

    @staticmethod
    def update_place(id, new_info):
        raise NotImplementedError()

    @staticmethod
    def list_places():
        raise NotImplementedError()


class BaseSpeakerManager():
    @staticmethod
    def create_speaker(file_path):
        raise NotImplementedError()

    @staticmethod
    def update_speaker(id, file_path):
        raise NotImplementedError()

    @staticmethod
    def delete_speaker(id):
        raise NotImplementedError()

    @staticmethod
    def list_speakers():
        raise NotImplementedError()


class BaseApplyManager():
    @staticmethod
    def create_event_apply_info(event_apply_info):
        raise NotImplementedError()

    @staticmethod
    def get_event_apply_info_by_event_basic_id(event_basic_id):
        raise NotImplementedError()

    @staticmethod
    def get_event_apply_info(event_apply_id):
        raise NotImplementedError()

    @staticmethod
    def update_event_apply_info(event_apply_id, update_info):
        raise NotImplementedError()

    @staticmethod
    def delete_event_apply_info(event_apply_id):
        raise NotImplementedError()


class BaseSlideManager():
    @staticmethod
    def list_slides():
        raise NotImplementedError()


class BaseUserManager():
    @staticmethod
    def login(username, password):
        raise NotImplementedError()

    @staticmethod
    def logout():
        raise NotImplementedError()

    @staticmethod
    def get_all_users():
        raise NotImplementedError()


class BaseRoleManager():
    @staticmethod
    def create_role(info):
        raise NotImplementedError()

    @staticmethod
    def update_role(role_id, info):
        raise NotImplementedError()

    @staticmethod
    def delete_role(role_id):
        raise NotImplementedError()

    @staticmethod
    def get_role(role_id):
        raise NotImplementedError()

    @staticmethod
    def get_roles():
        raise NotImplementedError()


class BaseCheckInListManager():
    @staticmethod
    def upload(event_basic_id, csv_reader):
        raise NotImplementedError()

    @staticmethod
    def get_check_in_list(event_basic_id):
        raise NotImplementedError()

    @staticmethod
    def update_check_in_list(event_basic_id, user_id, info):
        raise NotImplementedError()

    @staticmethod
    def delete_check_in_list(check_in_list_id):
        raise NotImplementedError()


class BaseMemberManager():
    @staticmethod
    def social_login(email, name):
        raise NotImplementedError()

    @staticmethod
    def logout():
        raise NotImplementedError()

    @staticmethod
    def get_members():
        raise NotImplementedError()

    @staticmethod
    def get_member(m_id):
        raise NotImplementedError()

    @staticmethod
    def update_member(m_id, info):
        raise NotImplementedError()

    @staticmethod
    def delete_member(m_id):
        raise NotImplementedError()
