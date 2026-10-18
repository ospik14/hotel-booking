from core.db.uow import UnitOfWork
from core.db import session as db_session


def get_uow() -> UnitOfWork:
    return UnitOfWork(session_maker=db_session.session_maker)
