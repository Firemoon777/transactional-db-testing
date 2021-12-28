import os

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, scoped_session
from sqlalchemy.orm.session import Session as SessionBase, sessionmaker

from app.orm import Server, Base
from app.service import power_off

HABR_TEST_DB_URL="HABR_TEST_DB_URL"


class TestSession(SessionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.begin_nested()

        @event.listens_for(self, "after_transaction_end")
        def restart_savepoint(session, transaction):
            if transaction.nested and not transaction._parent.nested:
                session.expire_all()
                session.begin_nested()


Session = scoped_session(sessionmaker(autoflush=False, class_=TestSession))


@pytest.fixture(scope="session")
def engine():
    if HABR_TEST_DB_URL not in os.environ:
        skip_reason_message: str = (
            f"Environment var with name {HABR_TEST_DB_URL!r} is not provided. "
            "Set this with a path to the real test database to run skipped tests."
        )
        pytest.skip(msg=skip_reason_message)

    engine = create_engine(
        os.environ[HABR_TEST_DB_URL],
        echo=False
    )
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    try:
        yield engine
    finally:
        Base.metadata.drop_all(engine, checkfirst=True)


@pytest.fixture
def session(engine):
    connection = engine.connect()
    transaction = connection.begin()

    Session.configure(bind=engine)
    session = Session()

    try:
        yield session
    finally:
        Session.remove()
        transaction.rollback()
        connection.close()


@pytest.fixture
def server(session):
    s = Server()
    s.ip = '127.0.0.1'
    s.hostname = 'home'
    s.power_on = True
    session.add(s)
    session.commit()
    return s


def test_presence(server):
    assert server.ip == '127.0.0.1'


def test_embedded_db(session, server):
    print(session.query(Server).all())
    assert power_off(session, server) == bool((server.id % 2) != 0)
    assert server.power_on == bool((server.id % 2) == 0)

