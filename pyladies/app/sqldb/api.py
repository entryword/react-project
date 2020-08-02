from datetime import datetime, timedelta

from sqlalchemy.sql import text, extract
from sqlalchemy import or_, and_

from app.exceptions import (
    TOPIC_NOT_EXIST, EVENTBASIC_NOT_EXIST,
    EVENTINFO_NOT_EXIST, SPEAKER_NOT_EXIST,
    PLACE_NOT_EXIST, APPLY_NOT_EXIST,
    USER_NOT_EXIST, SLIDERESOURCE_NOT_EXIST
)
from .abstract import SQLDatabaseAPI
from .models import (
    Topic, Speaker, Link, Place, EventBasic,
    SlideResource, EventInfo, EventApply, User
)


class MySQLDatabaseAPI(SQLDatabaseAPI):
    ########## create

    def create_topic(self, info, autocommit=False):
        obj = Topic(**info)
        self.session.add(obj)

        if autocommit:
            self.session.commit()
            return obj.sn
        return None

    def create_event_basic(self, info, autocommit=False):
        obj = EventBasic(**info)
        self.session.add(obj)

        if autocommit:
            self.session.commit()
            return obj.sn
        return None

    def create_event_info(self, info, autocommit=False):
        speaker_sns = info.pop("speaker_sns", [])
        assistant_sns = info.pop("assistant_sns", [])
        slide_resource_sns = info.pop("slide_resource_sns", [])

        obj = EventInfo(**info)

        speakers = self.session.query(Speaker).filter(Speaker.sn.in_(speaker_sns)).all()
        obj.speakers = speakers

        assistants = self.session.query(Speaker).filter(Speaker.sn.in_(assistant_sns)).all()
        obj.assistants = assistants

        slide_resources = self.session.query(SlideResource).filter(SlideResource.sn.in_(slide_resource_sns)).all()
        obj.slide_resources = slide_resources

        self.session.add(obj)

        if autocommit:
            self.session.commit()
            return obj.sn
        return None

    def create_place(self, info, autocommit=False):
        obj = Place(**info)
        self.session.add(obj)

        if autocommit:
            self.session.commit()
            return obj.sn
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
            return obj.sn
        return None

    def create_event_apply(self, info, autocommit=False):
        obj = EventApply(**info)
        self.session.add(obj)
        if autocommit:
            self.session.commit()
            return obj.sn
        return None

    def create_slide_resource(self, info, autocommit=False):
        obj = SlideResource(**info)
        self.session.add(obj)

        if autocommit:
            self.session.commit()
            return obj.sn
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

    def get_topic(self, sn):
        topic = self.session.query(Topic).filter_by(sn=sn).one_or_none()
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

    def get_event_basics_by_topic(self, topic_sn):
        return self.session.query(EventBasic).filter_by(topic_sn=topic_sn).all()

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

    def get_event_basic(self, sn):
        event_basic = self.session.query(EventBasic).filter_by(sn=sn).one_or_none()
        if not event_basic:
            raise EVENTBASIC_NOT_EXIST
        event_basic = self.session.merge(event_basic)
        return event_basic

    def get_event_info(self, sn):
        event_info = self.session.query(EventInfo).filter_by(sn=sn).one_or_none()
        if not event_info:
            raise EVENTINFO_NOT_EXIST
        event_info = self.session.merge(event_info)
        return event_info

    def get_event_apply_by_event_basic_sn(self, event_basic_sn):
        event_apply = self.session.query(EventApply)\
            .filter_by(event_basic_sn=event_basic_sn).one_or_none()
        if not event_apply:
            raise APPLY_NOT_EXIST
        event_apply = self.session.merge(event_apply)
        return event_apply

    def get_event_apply(self, sn):
        event_apply = self.session.query(EventApply).filter_by(sn=sn).one_or_none()
        if not event_apply:
            raise APPLY_NOT_EXIST
        event_apply = self.session.merge(event_apply)
        return event_apply

    # TODO: pagination and filter
    def get_places(self):
        return self.session.query(Place).all()

    def get_place(self, sn):
        place = self.session.query(Place).filter_by(sn=sn).one_or_none()
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

    def get_speaker(self, sn):
        speaker = self.session.query(Speaker).filter_by(sn=sn).one_or_none()
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

    def get_slide_resource(self, sn):
        slide_resource = self.session.query(SlideResource).filter_by(sn=sn).one_or_none()
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

    ########## update

    # TODO: not finished yet

    def update_topic(self, sn, info, autocommit=False):
        topic = self.session.query(Topic).filter_by(sn=sn).one_or_none()
        if not topic:
            raise TOPIC_NOT_EXIST

        info.pop("sn", None)
        for key, value in info.items():
            if hasattr(topic, key):
                setattr(topic, key, value)

        self.session.add(topic)
        if autocommit:
            self.session.commit()

    def update_event_basic(self, sn, info, autocommit=False):
        event_basic = self.session.query(EventBasic).filter_by(sn=sn).one_or_none()
        if not event_basic:
            raise EVENTBASIC_NOT_EXIST

        info.pop("sn", None)
        for key, value in info.items():
            if hasattr(event_basic, key):
                setattr(event_basic, key, value)

        self.session.add(event_basic)
        if autocommit:
            self.session.commit()

    def update_event_info(self, sn, info, autocommit=False):
        event_info = self.session.query(EventInfo).filter_by(sn=sn).one_or_none()
        if not event_info:
            raise EVENTINFO_NOT_EXIST

        if "speaker_sns" in info:
            speaker_sns = info.pop("speaker_sns")
            speakers = self.session.query(Speaker).filter(Speaker.sn.in_(speaker_sns)).all()
            event_info.speakers = speakers

        if "assistant_sns" in info:
            assistant_sns = info.pop("assistant_sns")
            assistants = self.session.query(Speaker).filter(Speaker.sn.in_(assistant_sns)).all()
            event_info.assistants = assistants

        if "slide_resource_sns" in info:
            slide_resource_sns = info.pop("slide_resource_sns")
            slide_resources = self.session.query(SlideResource).filter(SlideResource.sn.in_(slide_resource_sns)).all()
            event_info.slide_resources = slide_resources

        info.pop("sn", None)
        for key, value in info.items():
            if hasattr(event_info, key):
                setattr(event_info, key, value)

        self.session.add(event_info)
        if autocommit:
            self.session.commit()

    def update_place(self, sn, info, autocommit=False):
        place = self.session.query(Place).filter_by(sn=sn).one_or_none()
        if not place:
            raise PLACE_NOT_EXIST

        info.pop("sn", None)
        for key, value in info.items():
            if hasattr(place, key):
                setattr(place, key, value)

        self.session.add(place)
        if autocommit:
            self.session.commit()

    def update_speaker(self, sn, info, autocommit=False):
        speaker = self.session.query(Speaker).filter_by(sn=sn).one_or_none()
        if not speaker:
            raise SPEAKER_NOT_EXIST

        if "links" in info:
            for i in speaker.links:
                self.delete_link(i.sn, autocommit=autocommit)
            links = info.pop("links")
            links_ = []
            for i in links:
                links_.append(Link(**i))
            speaker.links = links_

        info.pop("sn", None)
        for key, value in info.items():
            if hasattr(speaker, key):
                setattr(speaker, key, value)

        self.session.add(speaker)
        if autocommit:
            self.session.commit()

    def update_event_apply(self, sn, info, autocommit=False):
        event_apply = self.session.query(EventApply).filter_by(sn=sn).one_or_none()
        if not event_apply:
            raise EVENTINFO_NOT_EXIST
        info.pop("sn", None)
        for key, value in info.items():
            if hasattr(event_apply, key):
                setattr(event_apply, key, value)

        self.session.add(event_apply)
        if autocommit:
            self.session.commit()

    ########## delete

    def delete_topic(self, sn, autocommit=False):
        # topic = self.session.query(Topic).filter_by(sn=sn).one_or_none()
        # if topic:
        #     self.session.delete(topic)

        #     if autocommit:
        #         self.session.commit()
        stmt = text("DELETE FROM topic WHERE sn=:sn").bindparams(sn=sn)
        self.session.execute(stmt)
        if autocommit:
            self.session.commit()

    def delete_event_basic(self, sn, autocommit=False):
        # event_basic = self.session.query(EventBasic).filter_by(sn=sn).one_or_none()
        # if event_basic:
        #     self.session.delete(event_basic)

        #     if autocommit:
        #         self.session.commit()
        stmt = text("DELETE FROM event_basic WHERE sn=:sn").bindparams(sn=sn)
        self.session.execute(stmt)
        if autocommit:
            self.session.commit()

    def delete_event_info(self, sn, autocommit=False):
        # event_info = self.session.query(EventInfo).filter_by(sn=sn).one_or_none()
        # if event_info:
        #     self.session.delete(event_info)

        #     if autocommit:
        #         self.session.commit()
        stmt = text("DELETE FROM event_info WHERE sn=:sn").bindparams(sn=sn)
        self.session.execute(stmt)
        if autocommit:
            self.session.commit()

    def delete_speaker(self, sn, autocommit=False):
        # speaker = self.session.query(Speaker).filter_by(sn=sn).one_or_none()
        # if speaker:
        #     self.session.delete(speaker)

        #     if autocommit:
        #         self.session.commit()
        stmt = text("DELETE FROM speaker WHERE sn=:sn").bindparams(sn=sn)
        self.session.execute(stmt)
        if autocommit:
            self.session.commit()

    def delete_link(self, sn, autocommit=True):
        stmt = text("DELETE FROM link WHERE sn=:sn").bindparams(sn=sn)
        self.session.execute(stmt)
        if autocommit:
            self.session.commit()

    def delete_slide_resource(self, sn, autocommit=True):
        stmt = text("DELETE FROM slide_resource WHERE sn=:sn").bindparams(sn=sn)
        self.session.execute(stmt)
        if autocommit:
            self.session.commit()

    def delete_event_apply(self, sn, autocommit=False):
        stmt = text("DELETE FROM event_apply WHERE sn=:sn").bindparams(sn=sn)
        self.session.execute(stmt)
        if autocommit:
            self.session.commit()
