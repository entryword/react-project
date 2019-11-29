from werkzeug.security import generate_password_hash

from app import create_app
from app.sqldb import DBWrapper
from app.sqldb.models import User


class TestLoginRequired:
    def setup(self):
        self.app = create_app('test2')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.db.create_all()
        self.test_client = self.app.test_client()

    def teardown(self):
        self.app.db.session.remove()
        self.app.db.drop_all()
        self.app.db.engine.dispose()
        self.app_context.pop()

    def login(self, login_info):
        rv = self.test_client.post("/cms/api/login", json=login_info)
        assert rv.json["info"]["code"] == 0

    def test_access_secret_when_user_not_login(self):
        rv = self.test_client.get("/cms/api/secret")

        assert rv.status_code == 200
        assert rv.json["info"]["code"] == 1702

    def test_access_secret_when_user_login(self):
        # preparation
        login_info = {
            "username": "pyladies",
            "password": "test123456",
            "mail": "ut@pyladies.com",
        }
        user_info = {
            "name": login_info["username"],
            "password_hash": generate_password_hash(login_info["password"], method="pbkdf2:sha1"),
            "mail": login_info["mail"],
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            obj = User(**user_info)
            db_sess.add(obj)
            db_sess.commit()

        # test
        self.login(login_info)
        rv = self.test_client.get("/cms/api/secret")

        # assertion
        assert rv.status_code == 200
        assert rv.data == b"Only authenticated users are allowed!"
