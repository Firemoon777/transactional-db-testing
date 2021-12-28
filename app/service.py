from sqlalchemy.orm import Session

from app.orm import Server


def power_off(session: Session, server: Server) -> bool:
    """
    Method tries to power off server
    :param server:
    :return: True if success, False otherwise
    """
    if server.id % 2 == 0:
        success = True
    else:
        success = False

    if success:
        server.power_on = False

    session.commit()
    return success
