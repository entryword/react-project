from datetime import datetime, timedelta

from sqlalchemy.sql import text, extract
from sqlalchemy import or_, and_

from app.exceptions import (
    TOPIC_NOT_EXIST, EVENTBASIC_NOT_EXIST,
    EVENTINFO_NOT_EXIST, SPEAKER_NOT_EXIST,
    MEMBER_NOT_EXIST,
    PLACE_NOT_EXIST, APPLY_NOT_EXIST,
    USER_NOT_EXIST, SLIDERESOURCE_NOT_EXIST,
    ROLE_NOT_EXIST,
    RECORD_NOT_EXIST)
from .abstract import SQLDatabaseAPI
from .models import (
    EventApply,
    EventBasic,
    EventInfo,
    Link,
    Member,
    Place,
    Role,
    SlideResource,
    Speaker,
    Topic,
    User,
    CheckInList)


class MySQLDatabaseAPI(SQLDatabaseAPI):
    ########## create

    def create_topic(self, info, autocommit=False):
        obj = Topic(**info)
        self.session.add(obj)

        if autocommit:
            self.session.commit()
            return obj.id
        return None

    def create_event_basic(self, info, autocommit=False):
        obj = EventBasic(**info)
        self.session.add(obj)

        if autocommit:
            self.session.commit()
            return obj.id
        return None

    def create_event_info(self, info, autocommit=False):
        speaker_ids = info.pop("speaker_ids", [])
        assistant_ids = info.pop("assistant_ids", [])
        slide_resource_ids = info.pop("slide_resource_ids", [])

        obj = EventInfo(**info)

        speakers = self.session.query(Speaker).filter(Speaker.id.in_(speaker_ids)).all()
        obj.speakers = speakers

        assistants = self.session.query(Speaker).filter(Speaker.id.in_(assistant_ids)).all()
        obj.assistants = assistants

        slide_resources = self.session.query(SlideResource).filter(SlideResource.id.in_(slide_resource_ids)).all()
        obj.slide_resources = slide_resources

        self.session.add(obj)

        if autocommit:
            self.session.commit()
            return obj.id

    def create_place(self, info, autocommit=False):
        obj = Place(**info)
        self.session.add(obj)

        if autocommit:
            self.session.commit()
            return obj.id
        return None

    def create_speaker(self, info, autocommit=False):
        links = info.pop("links", [])

        obj = Speaker(**info)
        links_ = []
        for i in links:
            links_.append(Link(**i))
        obj.links = links_
        self.session.add(obj)

        if autocommit:
            self.session.commit()
            return obj.id
        return None

    def create_event_apply(self, info, autocommit=False):
        obj = EventApply(**info)
        self.session.add(obj)
        if autocommit:
            self.session.commit()
            return obj.id
        return None

    def create_slide_resource(self, info, autocommit=False):
        obj = SlideResource(**info)
        self.session.add(obj)

        if autocommit:
            self.session.commit()
            return obj.id
        return None

    def create_role(self, info, autocommit=False):
        obj = Role(**info)
        self.session.add(obj)

        if autocommit:
            self.session.commit()
            return obj.id
        return None

    def create_check_in_list(self, info, autocommit=False, flush=False):
        obj = CheckInList(**info)
        self.session.add(obj)

        if autocommit:
            self.session.commit()
            return obj.id
        if flush:
            self.session.flush()
            return obj.id

    def create_user(self, info, autocommit=False, flush=False):
        obj = User(**info)
        self.session.add(obj)

        if autocommit:
            self.session.commit()
            return obj.id
        if flush:
            self.session.flush()
            return obj.id

    def create_member(self, info, autocommit=False):
        obj = Member(**info)
        self.session.add(obj)

        if autocommit:
            self.session.commit()
            return obj.id
        return None

    ########## get

    # TODO: pagination and filter
    def get_topics(self):
        return self.session.query(Topic).all()

    def search_topics(self, keyword, level=None, freq=None, host=None):
        key = "%" + keyword + "%"
        statement = Topic.name.like(key)
        if level:
            statement = and_(statement, Topic.level == level)
        if freq:
            statement = and_(statement, Topic.freq == freq)
        if host:
            statement = and_(statement, Topic.host == host)
        return self.session.query(Topic).filter(statement).all()

    def get_topic(self, id):
        topic = self.session.query(Topic).filter_by(id=id).one_or_none()
        if not topic:
            raise TOPIC_NOT_EXIST
        topic = self.session.merge(topic)
        return topic

    def get_topic_by_name(self, name):
        topic = self.session.query(Topic).filter_by(name=name).one_or_none()
        if not topic:
            raise TOPIC_NOT_EXIST
        topic = self.session.merge(topic)
        return topic

    def get_events_from_distinct_topics(self, limit):
        topic_levels = self.session.query(Topic.level).distinct(Topic.level).all()
        if not topic_levels:
            return []

        topic_levels = [row[0] for row in topic_levels]
        home_event = []
        current_time = datetime.utcnow() + timedelta(hours=8)
        for level in topic_levels:
            query = self.session.query(EventBasic)
            query = query.filter(EventBasic.topic.has(Topic.level == level))
            query = query.filter(
                or_(
                    EventBasic.date > current_time.strftime("%Y-%m-%d"),
                    and_(
                        EventBasic.date == current_time.strftime("%Y-%m-%d"),
                        EventBasic.start_time > current_time.strftime("%H:%M")
                    )
                )
            )
            query = query.order_by(EventBasic.date.asc())
            query = query.order_by(EventBasic.start_time.asc())
            event_basic = query.first()
            if event_basic and event_basic.event_info:
                home_event.append(event_basic)

        home_event.sort(key=lambda e: "{} {}".format(e.date, e.start_time))
        return home_event[:limit]

    def get_event_basics_by_topic(self, topic_id):
        return self.session.query(EventBasic).filter_by(topic_id=topic_id).all()

    def search_event_basics(self, keyword, date):

        # filter EventBasic date by specific year and month
        q = self.session.query(EventBasic)
        if date:
            date_splits = date.split('-')
            year = date_splits[0]
            month = date_splits[1]
            q = q.filter(
                extract('year', EventBasic.date) == year,
                extract('month', EventBasic.date) == month)

        # filter EventInfo title or Topic name by keyword
        key = "%" + keyword + "%"
        return q.filter(
            or_(
                EventBasic.event_info.has(EventInfo.title.like(key)),
                EventBasic.topic.has(Topic.name.like(key))
            )).all()

    def get_event_basics(self):
        return self.session.query(EventBasic).all()

    def get_event_basic(self, id):
        event_basic = self.session.query(EventBasic).filter_by(id=id).one_or_none()
        if not event_basic:
            raise EVENTBASIC_NOT_EXIST
        event_basic = self.session.merge(event_basic)
        return event_basic

    def get_event_info(self, id):
        event_info = self.session.query(EventInfo).filter_by(id=id).one_or_none()
        if not event_info:
            raise EVENTINFO_NOT_EXIST
        event_info = self.session.merge(event_info)
        return event_info

    def get_event_apply_by_event_basic_id(self, event_basic_id):
        event_apply = self.session.query(EventApply)\
            .filter_by(event_basic_id=event_basic_id).one_or_none()
        if not event_apply:
            raise APPLY_NOT_EXIST
        event_apply = self.session.merge(event_apply)
        return event_apply

    def get_event_apply(self, id):
        event_apply = self.session.query(EventApply).filter_by(id=id).one_or_none()
        if not event_apply:
            raise APPLY_NOT_EXIST
        event_apply = self.session.merge(event_apply)
        return event_apply

    # TODO: pagination and filter
    def get_places(self):
        return self.session.query(Place).all()

    def get_place(self, id):
        place = self.session.query(Place).filter_by(id=id).one_or_none()
        if not place:
            raise PLACE_NOT_EXIST
        place = self.session.merge(place)
        return place

    def get_place_by_name(self, name):
        place = self.session.query(Place).filter_by(name=name).one_or_none()
        if not place:
            raise PLACE_NOT_EXIST
        place = self.session.merge(place)
        return place

    # TODO: pagination and filter
    def get_speakers(self):
        return self.session.query(Speaker).all()

    def get_speaker(self, id):
        speaker = self.session.query(Speaker).filter_by(id=id).one_or_none()
        if not speaker:
            raise SPEAKER_NOT_EXIST
        speaker = self.session.merge(speaker)
        return speaker

    def get_speaker_by_name(self, name):
        speaker = self.session.query(Speaker).filter_by(name=name).one_or_none()
        if not speaker:
            raise SPEAKER_NOT_EXIST
        speaker = self.session.merge(speaker)
        return speaker

    def search_speakers(self, keyword):
        key = "%" + keyword + "%"
        return self.session.query(Speaker).filter(Speaker.name.like(key)).all()

    def get_slides(self):
        return self.session.query(SlideResource).all()

    def get_slide_resource(self, id):
        slide_resource = self.session.query(SlideResource).filter_by(id=id).one_or_none()
        if not slide_resource:
            raise SLIDERESOURCE_NOT_EXIST
        slide_resource = self.session.merge(slide_resource)
        return slide_resource

    def get_user_by_name(self, name):
        user = self.session.query(User).filter_by(name=name).one_or_none()
        if not user:
            raise USER_NOT_EXIST
        user = self.session.merge(user)
        return user

    def get_all_users(self):
        user_list = self.session.query(User).all()
        return user_list

    def get_users_by_emails(self, emails):
        return self.session.query(User).filter(User.mail.in_(emails)).all()

    def get_user_by_email(self, email):
        return self.session.query(User).filter(User.mail == email).first()

    def get_role(self, id):
        role = self.session.query(Role).filter_by(id=id).one_or_none()
        if not role:
            raise ROLE_NOT_EXIST
        role = self.session.merge(role)
        return role

    def get_roles(self):
        roles = self.session.query(Role).all()
        return roles

    def get_check_in_list(self, event_basic_id):
        records = self.session.query(CheckInList).filter_by(
            event_basic_id=event_basic_id
        ).all()
        return records

    def get_check_in_list_by_event_basic_id_and_email(self, event_basic_id, email):
        record = self.session.query(CheckInList).filter_by(
            event_basic_id=event_basic_id,
            mail=email
        ).first()
        return record

    def get_members(self):
        return self.session.query(Member).all()

    def get_member(self, m_id):
        member = self.session.query(Member).filter_by(id=m_id).first()
        if not member:
            raise MEMBER_NOT_EXIST
        return member

    def get_member_by_email(self, email):
        return self.session.query(Member).filter_by(mail=email).first()

    ########## update

    # TODO: not finished yet

    def update_topic(self, id, info, autocommit=False):
        topic = self.session.query(Topic).filter_by(id=id).one_or_none()
        if not topic:
            raise TOPIC_NOT_EXIST

        info.pop("id", None)
        for key, value in info.items():
            if hasattr(topic, key):
                setattr(topic, key, value)

        self.session.add(topic)
        if autocommit:
            self.session.commit()

    def update_event_basic(self, id, info, autocommit=False):
        event_basic = self.session.query(EventBasic).filter_by(id=id).one_or_none()
        if not event_basic:
            raise EVENTBASIC_NOT_EXIST

        info.pop("id", None)
        for key, value in info.items():
            if hasattr(event_basic, key):
                setattr(event_basic, key, value)

        self.session.add(event_basic)
        if autocommit:
            self.session.commit()

    def update_event_info(self, id, info, autocommit=False):
        event_info = self.session.query(EventInfo).filter_by(id=id).one_or_none()
        if not event_info:
            raise EVENTINFO_NOT_EXIST

        if "speaker_ids" in info:
            speaker_ids = info.pop("speaker_ids")
            speakers = self.session.query(Speaker).filter(Speaker.id.in_(speaker_ids)).all()
            event_info.speakers = speakers

        if "assistant_ids" in info:
            assistant_ids = info.pop("assistant_ids")
            assistants = self.session.query(Speaker).filter(Speaker.id.in_(assistant_ids)).all()
            event_info.assistants = assistants

        if "slide_resource_ids" in info:
            slide_resource_ids = info.pop("slide_resource_ids")
            slide_resources = self.session.query(SlideResource).filter(SlideResource.id.in_(slide_resource_ids)).all()
            event_info.slide_resources = slide_resources

        info.pop("id", None)
        for key, value in info.items():
            if hasattr(event_info, key):
                setattr(event_info, key, value)

        self.session.add(event_info)
        if autocommit:
            self.session.commit()

    def update_place(self, id, info, autocommit=False):
        place = self.session.query(Place).filter_by(id=id).one_or_none()
        if not place:
            raise PLACE_NOT_EXIST

        info.pop("id", None)
        for key, value in info.items():
            if hasattr(place, key):
                setattr(place, key, value)

        self.session.add(place)
        if autocommit:
            self.session.commit()

    def update_speaker(self, id, info, autocommit=False):
        speaker = self.session.query(Speaker).filter_by(id=id).one_or_none()
        if not speaker:
            raise SPEAKER_NOT_EXIST

        if "links" in info:
            for i in speaker.links:
                self.delete_link(i.id, autocommit=autocommit)
            links = info.pop("links")
            links_ = []
            for i in links:
                links_.append(Link(**i))
            speaker.links = links_

        info.pop("id", None)
        for key, value in info.items():
            if hasattr(speaker, key):
                setattr(speaker, key, value)

        self.session.add(speaker)
        if autocommit:
            self.session.commit()

    def update_event_apply(self, id, info, autocommit=False):
        event_apply = self.session.query(EventApply).filter_by(id=id).one_or_none()
        if not event_apply:
            raise EVENTINFO_NOT_EXIST
        info.pop("id", None)
        for key, value in info.items():
            if hasattr(event_apply, key):
                setattr(event_apply, key, value)

        self.session.add(event_apply)
        if autocommit:
            self.session.commit()

    def update_role(self, id, info, autocommit=False):
        role = self.session.query(Role).filter_by(id=id).one_or_none()
        if not role:
            raise ROLE_NOT_EXIST
        info.pop("id", None)
        for key, value in info.items():
            if hasattr(role, key):
                setattr(role, key, value)

        self.session.add(role)
        if autocommit:
            self.session.commit()

    def update_check_in_list(self, check_in_list_id, info, autocommit=False):
        record = self.session.query(CheckInList).filter_by(id=check_in_list_id).first()
        if not record:
            raise RECORD_NOT_EXIST

        for k, v in info.items():
            setattr(record, k, v)

        self.session.add(record)
        if autocommit:
            self.session.commit()

    def update_member(self, m_id, info, autocommit=False):
        member = self.session.query(Member).filter_by(id=m_id).first()
        if not member:
            raise MEMBER_NOT_EXIST

        for key, value in info.items():
            setattr(member, key, value)

        self.session.add(member)
        if autocommit:
            self.session.commit()

    ########## delete

    def delete_topic(self, id, autocommit=False):
        # topic = self.session.query(Topic).filter_by(id=id).one_or_none()
        # if topic:
        #     self.session.delete(topic)

        #     if autocommit:
        #         self.session.commit()
        stmt = text("DELETE FROM topic WHERE id=:id").bindparams(id=id)
        self.session.execute(stmt)
        if autocommit:
            self.session.commit()

    def delete_event_basic(self, id, autocommit=False):
        # event_basic = self.session.query(EventBasic).filter_by(id=id).one_or_none()
        # if event_basic:
        #     self.session.delete(event_basic)

        #     if autocommit:
        #         self.session.commit()
        stmt = text("DELETE FROM event_basic WHERE id=:id").bindparams(id=id)
        self.session.execute(stmt)
        if autocommit:
            self.session.commit()

    def delete_event_info(self, id, autocommit=False):
        # event_info = self.session.query(EventInfo).filter_by(id=id).one_or_none()
        # if event_info:
        #     self.session.delete(event_info)

        #     if autocommit:
        #         self.session.commit()
        stmt = text("DELETE FROM event_info WHERE id=:id").bindparams(id=id)
        self.session.execute(stmt)
        if autocommit:
            self.session.commit()

    def delete_speaker(self, id, autocommit=False):
        # speaker = self.session.query(Speaker).filter_by(id=id).one_or_none()
        # if speaker:
        #     self.session.delete(speaker)

        #     if autocommit:
        #         self.session.commit()
        stmt = text("DELETE FROM speaker WHERE id=:id").bindparams(id=id)
        self.session.execute(stmt)
        if autocommit:
            self.session.commit()

    def delete_link(self, id, autocommit=True):
        stmt = text("DELETE FROM link WHERE id=:id").bindparams(id=id)
        self.session.execute(stmt)
        if autocommit:
            self.session.commit()

    def delete_slide_resource(self, id, autocommit=True):
        stmt = text("DELETE FROM slide_resource WHERE id=:id").bindparams(id=id)
        self.session.execute(stmt)
        if autocommit:
            self.session.commit()

    def delete_event_apply(self, id, autocommit=False):
        stmt = text("DELETE FROM event_apply WHERE id=:id").bindparams(id=id)
        self.session.execute(stmt)
        if autocommit:
            self.session.commit()

    def delete_role(self, id, autocommit=False):
        stmt = text("DELETE FROM role WHERE id=:id").bindparams(id=id)
        self.session.execute(stmt)
        if autocommit:
            self.session.commit()

    def delete_check_in_list(self, id, autocommit=False):
        stmt = text("DELETE FROM check_in_list WHERE id=:id").bindparams(id=id)
        self.session.execute(stmt)
        if autocommit:
            self.session.commit()

    def delete_member(self, m_id, autocommit=False):
        member = self.session.query(Member).filter_by(id=m_id).first()
        if not member:
            return

        self.session.delete(member)
        if autocommit:
            self.session.commit()
