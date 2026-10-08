from core.db.uow import UnitOfWork
from core.db.session import session_maker

def get_uow() -> UnitOfWork:
    return UnitOfWork(session_maker=session_maker)

def get_current_user():
    return