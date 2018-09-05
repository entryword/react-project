from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .api import MySQLDatabaseAPI


class DBWrapper(object):
    def __init__(self, conn):
        self._conn = create_engine(conn)

    @contextmanager
    def session(self):
        DBSession = sessionmaker(bind=self._conn)
        session = DBSession()
        try:
            yield session
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()