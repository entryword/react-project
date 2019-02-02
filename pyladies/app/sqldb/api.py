from sqlalchemy.sql import text, extract
from sqlalchemy import or_

from app.exceptions import (
    TOPIC_NOT_EXIST, EVENTBASIC_NOT_EXIST,
    EVENTINFO_NOT_EXIST, SPEAKER_NOT_EXIST,
    PLACE_NOT_EXIST
)
from .abstract import SQLDatabaseAPI
from .models import (
    Topic, Speaker, Link, Place, EventBasic,
    SlideResource, EventInfo
)


class MySQLDatabaseAPI(SQLDatabaseAPI):
    ########## create

    def create_topic(self, info, autocommit=False):
        obj = Topic(**info)
        self.session.add(obj)

        if autocommit:
            self.session.commit()

    def create_event_basic(self, info, autocommit=False):
        obj = EventBasic(**info)
        self.session.add(obj)

        if autocommit:
            self.session.commit()

    def create_event_info(self, info, autocommit=False):
        speaker_sns = info.pop("speaker_sns", [])
        assistant_sns = info.pop("assistant_sns", [])
        slide_resources = info.pop("slide_resources", [])

        obj = EventInfo(**info)

        speakers = self.session.query(Speaker).filter(Speaker.sn.in_(speaker_sns)).all()
        obj.speakers = speakers

        assistants = self.session.query(Speaker).filter(Speaker.sn.in_(assistant_sns)).all()
        obj.assistants = assistants

        slide_resources_ = []
        for i in slide_resources:
            slide_resources_.append(SlideResource(**i))
        obj.slide_resources = slide_resources_

        self.session.add(obj)

        if autocommit:
            self.session.commit()

    def create_place(self, info, autocommit=False):
        obj = Place(**info)
        self.session.add(obj)

        if autocommit:
            self.session.commit()

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

    ########## get

    # TODO: pagination and filter
    def get_topics(self):
        return self.session.query(Topic).all()

    def get_topics_by_keyword(self, keyword):
        key = "%" + keyword + "%"
        return self.session.query(Topic).filter(Topic.name.like(key)).all()

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

        if "slide_resources" in info:
            for i in event_info.slide_resources:
                self.delete_slide_resource(i.sn, autocommit=autocommit)
            slide_resources = info.pop("slide_resources")
            slide_resources_ = []
            for i in slide_resources:
                slide_resources_.append(SlideResource(**i))
            event_info.slide_resources = slide_resources_

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

    def delete_place(self, sn, autocommit=False):
        # place = self.session.query(Place).filter_by(sn=sn).one_or_none()
        # if place:
        #     self.session.delete(place)

        #     if autocommit:
        #         self.session.commit()
        stmt = text("DELETE FROM place WHERE sn=:sn").bindparams(sn=sn)
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
