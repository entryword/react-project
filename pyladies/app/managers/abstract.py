class BaseTopicManager():
    @staticmethod
    def create_topic(file_path):
        raise NotImplementedError()

    @staticmethod
    def update_topic(sn, file_path):
        raise NotImplementedError()

    @staticmethod
    def delete_topic(sn):
        raise NotImplementedError()

    @staticmethod
    def list_topics(key=None):
        raise NotImplementedError()


class BaseEventManager():
    @staticmethod
    def create_event(info):
        raise NotImplementedError()

    @staticmethod
    def update_event(sn, new_info):
        raise NotImplementedError()

    @staticmethod
    def delete_event(sn):
        raise NotImplementedError()

    @staticmethod
    def list_events(topic_sn):
        raise NotImplementedError()


class BasePlaceManager():
    @staticmethod
    def create_place(info):
        raise NotImplementedError()

    @staticmethod
    def update_place(sn, new_info):
        raise NotImplementedError()

    @staticmethod
    def list_places():
        raise NotImplementedError()


class BaseSpeakerManager():
    @staticmethod
    def create_speaker(file_path):
        raise NotImplementedError()

    @staticmethod
    def update_speaker(sn, file_path):
        raise NotImplementedError()

    @staticmethod
    def delete_speaker(sn):
        raise NotImplementedError()

    @staticmethod
    def list_speakers():
        raise NotImplementedError()


class BaseApplyManager():
    @staticmethod
    def create_event_apply_info(event_apply_info):
        raise NotImplementedError()

    @staticmethod
    def get_event_apply_info_by_event_basic_sn(event_basic_sn):
        raise NotImplementedError()

    @staticmethod
    def get_event_apply_info(event_apply_sn):
        raise NotImplementedError()

    @staticmethod
    def update_event_apply_info(event_apply_sn, update_info):
        raise NotImplementedError()

    @staticmethod
    def delete_event_apply_info(event_apply_sn):
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
    def update_role(role_sn, info):
        raise NotImplementedError()

    @staticmethod
    def delete_role(role_sn):
        raise NotImplementedError()

    @staticmethod
    def get_role(role_sn):
        raise NotImplementedError()

    @staticmethod
    def get_roles():
        raise NotImplementedError()


class BaseCheckInListManager():
    @staticmethod
    def upload(info):
        raise NotImplementedError()

    @staticmethod
    def get_check_in_list(event_basic_sn):
        raise NotImplementedError()

    @staticmethod
    def update_check_in_list(event_basic_sn, user_sn, info):
        raise NotImplementedError()

    @staticmethod
    def delete_check_in_list(check_in_list_sn):
        raise NotImplementedError()
