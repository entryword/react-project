from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin, AnonymousUserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import types, String, func, text
from sqlalchemy.ext.declarative import declarative_base

from app.constant import DEFAULT_PLACE_SN

Base = declarative_base(name='Model')
db = SQLAlchemy()


class IntegerArrayType(types.TypeDecorator):
    impl = String

    @property
    def python_type(self):
        return list

    def process_literal_param(self, value, dialect):
        raise RuntimeError("Not allow to use this")

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
                ", photo: {obj.photo}"
                ", title: {obj.title}"
                ", intro: {obj.intro}"
                ", fields: {obj.fields}").format(obj=self)


class Link(db.Model):
    __tablename__ = "link"

    sn = db.Column(db.Integer, primary_key=True)
    speaker_sn = db.Column(db.Integer,
                           db.ForeignKey("speaker.sn", ondelete="CASCADE"),
                           nullable=False)
    type = db.Column(db.String(128), nullable=False)
    url = db.Column(db.String(1024), nullable=False)

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
                         db.ForeignKey("place.sn", ondelete="NO ACTION"),
                         default=DEFAULT_PLACE_SN,
                         nullable=False)

    topic = db.relationship("Topic",
                            backref=db.backref("event_basics", uselist=True))
    place = db.relationship("Place")
    apply = db.relationship("EventApply", uselist=False)

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
    type = db.Column(db.String(128), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    url = db.Column(db.String(1024), nullable=False)

    def __str__(self):
        return ("<SlideResource sn {obj.sn}"
                ", title: {obj.title}"
                ", type: {obj.type}>").format(obj=self)

event_slide = db.Table(
    'event_slide',
    db.Column(
        'event_info_sn',
        db.Integer,
        db.ForeignKey('event_info.sn', ondelete="CASCADE")
    ),
    db.Column(
        'slide_sn',
        db.Integer,
        db.ForeignKey('slide_resource.sn', ondelete="CASCADE")
    ),
    db.PrimaryKeyConstraint("event_info_sn", "slide_sn")
)

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
    slide_resources = db.relationship("SlideResource",
                                      secondary=event_slide,
                                      uselist=True)
    speakers = db.relationship("Speaker",
                               secondary=event_info_to_speaker,
                               uselist=True,
                               backref=db.backref("event_infos", uselist=True))
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


class EventApply(db.Model):
    __tablename__ = "event_apply"

    sn = db.Column(db.Integer, primary_key=True)
    event_basic_sn = db.Column(db.Integer,
                               db.ForeignKey("event_basic.sn", ondelete="CASCADE"),
                               nullable=False,
                               unique=True)
    apply = db.Column(types.JSON, nullable=True)

    def __str__(self):
        return ("<EventApply sn: {obj.sn}"
                ", event_basic_sn: {obj.event_basic_sn}"
                ", apply: {obj.apply}").format(obj=self)


user_to_role = db.Table(
    "user_to_role",
    db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE")
    ),
    db.Column(
        "role_sn",
        db.Integer,
        db.ForeignKey("role.sn", ondelete="CASCADE")
    ),
    db.PrimaryKeyConstraint("user_id", "role_sn")
)


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    mail = db.Column(db.String(128), unique=True, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)
    roles = db.relationship("Role",
                            secondary=user_to_role,
                            uselist=True)

    # @property
    # def password(self):
    #     raise AttributeError('password is not a readable attribute')

    # @password.setter
    # def password(self, password):
    #     self.password_hash = generate_password_hash(password, method="pbkdf2:sha1")

    @property
    def role_ids(self):
        return [r.sn for r in self.roles]

    def __str__(self):
        return ("<User sn: {obj.id}"
                ", name: {obj.name}"
                ", mail: {obj.mail}"
                ", status: {obj.status}"
                ", role_ids: {obj.role_ids}").format(obj=self)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Role(db.Model):
    __tablename__ = "role"

    sn = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    permission = db.Column(types.JSON, nullable=False)
    users = db.relationship("User",
                            secondary=user_to_role,
                            uselist=True)

    @property
    def user_ids(self):
        return [u.id for u in self.users]

    def __str__(self):
        return ("<Role sn: {obj.sn}"
                ", name: {obj.name}"
                ", permission: {obj.permission}"
                ", user_ids: {obj.user_ids}").format(obj=self)


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


# 活動報到名冊 TODO 待User table設計好後 加入ForeignKey
class CheckInList(db.Model):
    __tablename__ = "check_in_list"

    sn = db.Column(db.Integer, primary_key=True)
    event_basic_sn = db.Column(db.Integer, nullable=False)  # 活動id
    user_sn = db.Column(db.Integer)  # 參加者id (當下有在user table的話就加入，沒有就null)
    name = db.Column(db.String(128), nullable=False)  # 參加者名稱
    mail = db.Column(db.String(128), nullable=False)  # 參加者email
    phone = db.Column(db.String(128), nullable=False)  # 參加者phone
    ticket_type = db.Column(db.Integer, nullable=False)  # 票卷種類 1:一般人 2:學生票
    ticket_amount = db.Column(db.Integer, nullable=False)  # 票價
    remark = db.Column(db.String(128))  # 備註 (admin可編輯)
    status = db.Column(db.Integer, server_default=text('0'), nullable=False)  # 狀態 0:未出席 1:出席
    update_datetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())  # 更新時間
    create_datetime = db.Column(db.DateTime, nullable=False, server_default=func.now())  # 建立時間
