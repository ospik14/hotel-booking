from core.db.uow import UnitOfWork

class HotelService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    