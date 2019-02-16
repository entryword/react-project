import json
import os
import sys

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import create_app, db
from app.managers.topic import Manager as TopicManager
from app.managers.event import Manager as EventManager
from app.managers.speaker import Manager as SpeakerManager
from app.managers.place import Manager as PlaceManager
#from app.managers.apply import Manager as ApplyManager


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.option('-c', '--create', action='count', help='create topic (must be used with -f)')
@manager.option('-u', '--update', dest='update_sn', metavar='ID', type=int,
                help='update topic (must be used with -f)')
@manager.option('-d', '--delete', dest='delete_sn', metavar='ID', type=int, help='delete topic')
@manager.option('-f', '--file', dest='f', metavar='FILE')
@manager.option('-l', '--list', dest='ls', action='count', help='list topics')
@manager.option('-k', '--keyword', dest='key', help='filter topics (must be used with -l)',
                default=None)
def topic(create, update_sn, delete_sn, f, ls, key):
    tm = TopicManager()
    if create:
        if not f:
            print("Please specify the JSON file path by '-f FILE'.")
        else:
            sn = tm.create_topic(f)
            print("Create topic (sn={}) successfully.".format(sn))

    if update_sn:
        if not f:
            print("Please specify the JSON file path by '-f FILE'.")
        else:
            tm.update_topic(update_sn, f)
            print("Update topic (sn={}) successfully.".format(update_sn))

    if delete_sn:
        tm.delete_topic(delete_sn)
        print("Delete topic (sn={}) successfully.".format(delete_sn))

    if ls:
        tm.list_topics(key)


@manager.option('-c', '--create', action='count', help='create event (must be used with -f)')
@manager.option('-u', '--update', dest='update_sn', metavar='ID', type=int,
                help='update event (must be used with -f)')
@manager.option('-d', '--delete', dest='delete_sn', metavar='ID', type=int, help='delete event')
@manager.option('-f', '--file', dest='f', metavar='FILE')
@manager.option('-l', '--list', dest='topic_sn', metavar='TOPIC_ID', type=int,
                help='list topic\'s events')
def event(create, update_sn, delete_sn, f, topic_sn):
    tm = EventManager()
    if create:
        if not f:
            print("Please specify the JSON file path by '-f FILE'.")
        else:
            sn = tm.create_event(f)
            print("Create event (sn={}) successfully.".format(sn))

    if update_sn:
        if not f:
            print("Please specify the JSON file path by '-f FILE'.")
        else:
            tm.update_event(update_sn, f)
            print("Update event (sn={}) successfully.".format(update_sn))

    if delete_sn:
        tm.delete_event(delete_sn)
        print("Delete event (sn={}) successfully.".format(delete_sn))

    if topic_sn:
        tm.list_events(topic_sn)


@manager.option('-c', '--create', action='count', help='create speaker (must be used with -f)')
@manager.option('-u', '--update', dest='update_sn', metavar='ID', type=int,
                help='update speaker (must be used with -f)')
@manager.option('-d', '--delete', dest='delete_sn', metavar='ID', type=int, help='delete speaker')
@manager.option('-f', '--file', dest='f', metavar='FILE')
@manager.option('-l', '--list', dest='ls', action='count', help='list speakers')
def speaker(create, update_sn, delete_sn, f, ls):
    tm = SpeakerManager()
    if create:
        if not f:
            print("Please specify the JSON file path by '-f FILE'.")
        else:
            sn = tm.create_speaker(f)
            print("Create speaker (sn={}) successfully.".format(sn))

    if update_sn:
        if not f:
            print("Please specify the JSON file path by '-f FILE'.")
        else:
            tm.update_speaker(update_sn, f)
            print("Update speaker (sn={}) successfully.".format(update_sn))

    if delete_sn:
        tm.delete_speaker(delete_sn)
        print("Delete speaker (sn={}) successfully.".format(delete_sn))

    if ls:
        tm.list_speakers()


@manager.option('-c', '--create', action='count', help='create place (must be used with -f)')
@manager.option('-u', '--update', dest='update_sn', metavar='ID', type=int,
                help='update place (must be used with -f)')
@manager.option('-d', '--delete', dest='delete_sn', metavar='ID', type=int, help='delete place')
@manager.option('-f', '--file', dest='f', metavar='FILE')
@manager.option('-l', '--list', dest='ls', action='count', help='list places')
def place(create, update_sn, delete_sn, f, ls):
    tm = PlaceManager()
    if create:
        if not f:
            print("Please specify the JSON file path by '-f FILE'.")
        else:
            sn = tm.create_place(f)
            print("Create place (sn={}) successfully.".format(sn))

    if update_sn:
        if not f:
            print("Please specify the JSON file path by '-f FILE'.")
        else:
            tm.update_place(update_sn, f)
            print("Update place (sn={}) successfully.".format(update_sn))

    if delete_sn:
        tm.delete_place(delete_sn)
        print("Delete place (sn={}) successfully.".format(delete_sn))

    if ls:
        tm.list_places()


@manager.option('-c', '--create', action='count', help='create apply info (must be used with -f)')
@manager.option('-u', '--update', dest='update_sn', metavar='ID', type=int,
                help='update apply info (must be used with -f)')
@manager.option('-d', '--delete', dest='delete_sn', metavar='ID', type=int,
                help='delete apply info')
@manager.option('-g', '--get', dest='get_sn', metavar='ID', type=int, help='get apply info')
@manager.option('-f', '--file', dest='f', metavar='FILE')
def apply(create, update_sn, delete_sn, get_sn, f):
    tm = ApplyManager()
    #filepath should be checked
    if create:
        if not f:
            print("Please specify the JSON file path by '-f FILE'.")
        else:
            with open(f) as f:
                event_apply_info = json.loads(f.read())
                tm.create_event_apply_info(event_apply_info)
                print("Create event apply info successfully.")

    if update_sn:
        if not f:
            print("Please specify the JSON file path by '-f FILE'.")
        else:
            with open(f) as f:
                event_apply_info = json.loads(f.read())
                tm.update_event_apply_info(update_sn, event_apply_info)
                print("Update event (sn={}) apply info successfully.".format(update_sn))

    if delete_sn:
        tm.delete_event_apply_info(delete_sn)
        print("Delete event (sn={}) apply info successfully.".format(delete_sn))

    if get_sn:
        event_apply_info = tm.get_event_apply_info(get_sn)
        print(event_apply_info)


if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    manager.run()
