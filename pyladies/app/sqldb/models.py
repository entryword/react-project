from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import types, String
from sqlalchemy.ext.declarative import declarative_base

# from app import db


Base = declarative_base(name='Model')
db = SQLAlchemy()


class IntegerArrayType(types.TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        # from python to database
        value = [str(i) for i in value]
        return ",".join(value)

    def process_result_value(self, value, dialect):
        # from database to python object
        value = value.split(",")
        value = [int(i) for i in value]
        return value


class Topic(db.Model):
    __tablename__ = "topic"

    sn = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    desc = db.Column(db.Text, nullable=True)
    freq = db.Column(db.Integer, nullable=False)
    level = db.Column(db.Integer, nullable=False)
    host = db.Column(db.Integer, nullable=False)
    fields = db.Column(IntegerArrayType(128), nullable=False)

    def __str__(self):
        return ("<Topic sn: {obj.sn}"
                ", name: {obj.name}"
                ", desc: {obj.desc}"
                ", freq: {obj.freq}"
                ", level: {obj.level}"
                ", host: {obj.host}"
                ", fields: {obj.fields}>").format(obj=self)


class Speaker(db.Model):
    __tablename__ = "speaker"

    sn = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    photo = db.Column(db.String(128), nullable=True)
    title = db.Column(db.String(128), nullable=False)
    major_related = db.Column(db.Boolean, nullable=False)
    intro = db.Column(db.Text, nullable=True)
    fields = db.Column(IntegerArrayType(128), nullable=False)

    def __str__(self):
        return ("<Speaker sn: {obj.sn}"
                ", name: {obj.name}"
                ", title: {obj.title}"
                ", fields: {obj.fields}"
                ", links: {obj.links}>").format(obj=self)


class Link(db.Model):
    __tablename__ = "link"

    sn = db.Column(db.Integer, primary_key=True)
    speaker_sn = db.Column(db.Integer,
                           db.ForeignKey("speaker.sn", ondelete="CASCADE"),
                           nullable=False)
    type = db.Column(db.String(128), nullable=False)
    url = db.Column(db.String(128), nullable=False)

    speaker = db.relationship("Speaker",
                              backref=db.backref("links", uselist=True))


class Place(db.Model):
    __tablename__ = "place"

    sn = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    addr = db.Column(db.String(128), nullable=False)
    map = db.Column(db.String(128), nullable=False)

    def __str__(self):
        return ("<Place sn: {obj.sn}"
                ", name: {obj.name}"
                ", addr: {obj.addr}"
                ", map: {obj.map}>").format(obj=self)


def validate_time_format(time_str, expected_format, err_message):
    try:
        datetime.strptime(time_str, expected_format)
    except Exception:
        raise ValueError(err_message)


class EventBasic(db.Model):
    __tablename__ = "event_basic"

    sn = db.Column(db.Integer, primary_key=True)
    topic_sn = db.Column(db.Integer,
                         db.ForeignKey("topic.sn", ondelete="CASCADE"),
                         nullable=False)
    date = db.Column(db.String(10), nullable=False)
    start_time = db.Column(db.String(5), nullable=False)
    end_time = db.Column(db.String(5), nullable=False)
    place_sn = db.Column(db.Integer,
                         db.ForeignKey("place.sn", ondelete="SET NULL"),
                         nullable=True)

    topic = db.relationship("Topic",
                            backref=db.backref("event_basics", uselist=True))
    place = db.relationship("Place")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        validate_time_format(self.date,
                             "%Y-%m-%d",
                             "The format of 'date' must be '%Y-%m-%d'")
        validate_time_format(self.start_time,
                             "%H:%M",
                             "The format of 'start_time' must be '%H:%M'")
        validate_time_format(self.end_time,
                             "%H:%M",
                             "The format of 'end_time' must be '%H:%M'")

    def __str__(self):
        return ("<EventBasic sn: {obj.sn}"
                ", topic_sn: {obj.topic_sn}"
                ", date: {obj.date}"
                ", start_time: {obj.start_time}"
                ", end_time: {obj.end_time}"
                ", place: {obj.place}>").format(obj=self)


event_info_to_speaker = db.Table(
    "event_info_to_speaker",
    # Base.metadata,
    db.Column(
        "event_info_sn",
        db.Integer,
        db.ForeignKey("event_info.sn", ondelete="CASCADE")
    ),
    db.Column(
        "speaker_sn",
        db.Integer,
        db.ForeignKey("speaker.sn", ondelete="CASCADE")
    ),
    db.PrimaryKeyConstraint("event_info_sn", "speaker_sn")
)


event_info_to_assistant = db.Table(
    "event_info_to_assistant",
    # Base.metadata,
    db.Column(
        "event_info_sn",
        db.Integer,
        db.ForeignKey("event_info.sn", ondelete="CASCADE")
    ),
    db.Column(
        "assistant_sn",
        db.Integer,
        db.ForeignKey("speaker.sn", ondelete="CASCADE")
    ),
    db.PrimaryKeyConstraint("event_info_sn", "assistant_sn")
)


class SlideResource(db.Model):
    __tablename__ = "slide_resource"

    sn = db.Column(db.Integer, primary_key=True)
    event_info_sn = db.Column(db.Integer,
                              db.ForeignKey("event_info.sn", ondelete="CASCADE"),
                              nullable=False)
    type = db.Column(db.String(128), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    url = db.Column(db.String(128), nullable=False)

    def __str__(self):
        return ("<SlideResource sn {obj.sn}"
                ", title: {obj.title}"
                ", type: {obj.type}>").format(obj=self)


class EventInfo(db.Model):
    __tablename__ = "event_info"

    sn = db.Column(db.Integer, primary_key=True)
    event_basic_sn = db.Column(db.Integer,
                               db.ForeignKey("event_basic.sn", ondelete="CASCADE"),
                               nullable=False,
                               unique=True)
    title = db.Column(db.String(128), nullable=False)
    desc = db.Column(db.Text, nullable=True)
    fields = db.Column(IntegerArrayType(128), nullable=False)

    event_basic = db.relationship("EventBasic",
                                  backref=db.backref("event_info", uselist=False))
    slide_resources = db.relationship("SlideResource", uselist=True)
    speakers = db.relationship("Speaker",
                                secondary=event_info_to_speaker,
                                uselist=True)
    assistants = db.relationship("Speaker",
                                secondary=event_info_to_assistant,
                                uselist=True)

    def __str__(self):
        return ("<EventInfo event_basic_sn: {obj.event_basic_sn}"
                ", title: {obj.title}"
                ", desc: {obj.desc}"
                ", fields: {obj.fields}"
                ", slide_resources: {obj.slide_resources}"
                ", speakers: {obj.speakers}"
                ", assistants: {obj.assistants}>").format(obj=self)