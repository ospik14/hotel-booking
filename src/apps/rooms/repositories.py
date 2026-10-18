from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy import insert, select, update, and_, func
from .models import Room
from apps.bookings.models import Booking, BookingStatus
from .schemas import RoomCreate, RoomUpdate, RoomFilters, AvailableRoomsFilters
from core.exceptions import RoomAlreadyExistsError, RoomNotFoundError


class RoomRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, room_request: RoomCreate):
        try:
            stmt = (
                insert(Room)
                .values(**room_request.model_dump())
                .returning(Room)
            )
            result = await self.session.execute(stmt)
        except IntegrityError as exc:
            raise RoomAlreadyExistsError() from exc

        return result.scalar_one()

    async def get(self, id: int):
        try:
            stmt = select(Room).where(Room.id == id)
            result = await self.session.execute(stmt)
            return result.scalar_one()
        except NoResultFound as exc:
            raise RoomNotFoundError() from exc

    async def get_for_update(self, id: int):
        stmt = select(Room).where(Room.id == id).with_for_update()
        result = await self.session.execute(stmt)
        room = result.scalar_one_or_none()
        if room is None:
            raise RoomNotFoundError()
        return room

    async def get_list(self, filters: RoomFilters):
        conditions = []
        if filters.capacity_gte is not None:
            conditions.append(Room.capacity >= filters.capacity_gte)
        if filters.capacity_lte is not None:
            conditions.append(Room.capacity <= filters.capacity_lte)
        if filters.guests is not None:
            conditions.append(Room.capacity >= filters.guests)
        if filters.price_gte is not None:
            conditions.append(Room.price_per_night >= filters.price_gte)
        if filters.price_lte is not None:
            conditions.append(Room.price_per_night <= filters.price_lte)
        if filters.name_contains is not None:
            conditions.append(Room.name.ilike(f'%{filters.name_contains}%'))
        if filters.is_active is not None:
            conditions.append(Room.is_active.is_(filters.is_active))

        stmt = select(Room)

        if filters.check_in and filters.check_out:
            busy_rooms = (
                select(Booking.room_id)
                .where(
                    Booking.status == BookingStatus.CONFIRMED,
                    Booking.check_in_date < filters.check_out,
                    Booking.check_out_date > filters.check_in,
                )
            )
            conditions.append(Room.id.not_in(busy_rooms))
            conditions.append(Room.is_active.is_(True))

        if conditions:
            stmt = stmt.where(and_(*conditions))

        stmt = (
            stmt.order_by(Room.id)
            .limit(filters.limit)
            .offset(filters.offset)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_available(self, filters: AvailableRoomsFilters):
        conditions = [
            Room.is_active.is_(True),
        ]
        if filters.guests is not None:
            conditions.append(Room.capacity >= filters.guests)
        if filters.price_gte is not None:
            conditions.append(Room.price_per_night >= filters.price_gte)
        if filters.price_lte is not None:
            conditions.append(Room.price_per_night <= filters.price_lte)

        busy_rooms = (
            select(Booking.room_id)
            .where(
                Booking.status == BookingStatus.CONFIRMED,
                Booking.check_in_date < filters.check_out,
                Booking.check_out_date > filters.check_in,
            )
        )
        conditions.append(Room.id.not_in(busy_rooms))

        stmt = (
            select(Room)
            .where(and_(*conditions))
            .order_by(Room.price_per_night, Room.id)
            .limit(filters.limit)
            .offset(filters.offset)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, id: int, room_upd: RoomUpdate):
        try:
            stmt = (
                update(Room)
                .where(Room.id == id)
                .values(
                    **room_upd.model_dump(exclude_unset=True),
                    updated_at=func.now(),
                )
                .returning(Room)
            )
            result = await self.session.execute(stmt)
            return result.scalar_one()
        except NoResultFound as exc:
            raise RoomNotFoundError() from exc
        except IntegrityError as exc:
            raise RoomAlreadyExistsError() from exc

    async def deactivate(self, id: int):
        stmt = (
            update(Room)
            .where(Room.id == id)
            .values(is_active=False, updated_at=func.now())
            .returning(Room)
        )
        result = await self.session.execute(stmt)
        room = result.scalar_one_or_none()
        if room is None:
            raise RoomNotFoundError()
        return room

    async def count_future_confirmed_with_guests_gt(
        self, room_id: int, capacity: int, today: date
    ) -> int:
        stmt = (
            select(func.count())
            .select_from(Booking)
            .where(
                Booking.room_id == room_id,
                Booking.status == BookingStatus.CONFIRMED,
                Booking.check_out_date > today,
                Booking.guests > capacity,
            )
        )
        result = await self.session.execute(stmt)
        return int(result.scalar_one())
