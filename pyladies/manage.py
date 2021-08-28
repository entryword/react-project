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
from app.managers.apply import Manager as ApplyManager


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import subprocess
    subprocess.check_call(["pytest", "./tests"])


if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    manager.run()
