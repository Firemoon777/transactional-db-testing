import pytest
from sqlalchemy.orm import Session

from app.orm import Server
from app.service import power_off


class MockSession(Session):
    def commit(self):
        pass


def test_mock():
    mock = MockSession()
    server = Server()
    server.id = 2
    server.power_on = True

    assert power_off(mock, server) is True
    assert server.power_on is False