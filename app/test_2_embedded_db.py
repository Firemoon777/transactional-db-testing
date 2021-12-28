import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.orm import Server, Base
from app.service import power_off

HABR_TEST_DB_URL="HABR_TEST_DB_URL"


@pytest.fixture(scope="function")
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
    session = Session(engine)
    yield session


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
    assert power_off(session, server) is True
    assert server.power_on is False

