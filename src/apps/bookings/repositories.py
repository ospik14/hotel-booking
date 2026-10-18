from decimal import Decimal
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update, and_, func
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from .schemas import BookingCreate, BookingFilters, AdminBookingFilters
from .models import Booking, BookingStatus
from core.exceptions import BookingOverlapError, RoomNotExistsError


class BookingRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        booking: BookingCreate,
        user_id: int,
        price_per_night: Decimal,
        total_price: Decimal,
    ):
        try:
            stmt = (
                insert(Booking)
                .values(
                    room_id=booking.room_id,
                    check_in_date=booking.check_in_date,
                    check_out_date=booking.check_out_date,
                    guests=booking.guests,
                    user_id=user_id,
                    status=BookingStatus.CONFIRMED,
                    price_per_night=price_per_night,
                    total_price=total_price,
                )
                .returning(Booking.id)
            )
            result = await self.session.execute(stmt)
            booking_id = result.scalar_one()
        except IntegrityError as e:
            error_msg = str(e.orig)
            if 'violates foreign key constraint' in error_msg:
                raise RoomNotExistsError() from e
            if 'no_overlapping_booking' in error_msg:
                raise BookingOverlapError() from e
            raise

        return await self.get_by_id(booking_id)

    async def get_by_id(self, id: int) -> Optional[Booking]:
        stmt = (
            select(Booking)
            .options(joinedload(Booking.room))
            .where(Booking.id == id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_for_user(self, id: int, user_id: int) -> Optional[Booking]:
        stmt = (
            select(Booking)
            .options(joinedload(Booking.room))
            .where(
                and_(
                    Booking.id == id,
                    Booking.user_id == user_id,
                )
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_list(self, user_id: int, filters: BookingFilters):
        conditions = [Booking.user_id == user_id]
        self._apply_filters(conditions, filters)

        stmt = (
            select(Booking)
            .options(joinedload(Booking.room))
            .where(and_(*conditions))
            .order_by(Booking.created_at.desc())
            .limit(filters.limit)
            .offset(filters.offset)
        )
        result = await self.session.execute(stmt)
        return result.scalars().unique().all()

    async def get_admin_list(self, filters: AdminBookingFilters):
        conditions = []
        if filters.user_id is not None:
            conditions.append(Booking.user_id == filters.user_id)
        self._apply_filters(conditions, filters)

        stmt = select(Booking).options(joinedload(Booking.room))
        if conditions:
            stmt = stmt.where(and_(*conditions))
        stmt = (
            stmt.order_by(Booking.created_at.desc())
            .limit(filters.limit)
            .offset(filters.offset)
        )
        result = await self.session.execute(stmt)
        return result.scalars().unique().all()

    def _apply_filters(self, conditions: list, filters: BookingFilters) -> None:
        if filters.status is not None:
            conditions.append(Booking.status == filters.status)
        if filters.room_id is not None:
            conditions.append(Booking.room_id == filters.room_id)
        if filters.check_in_from is not None:
            conditions.append(Booking.check_in_date >= filters.check_in_from)
        if filters.check_in_to is not None:
            conditions.append(Booking.check_in_date <= filters.check_in_to)

    async def set_status(self, id: int, status: BookingStatus) -> Optional[Booking]:
        stmt = (
            update(Booking)
            .where(Booking.id == id)
            .values(status=status, updated_at=func.now())
            .returning(Booking.id)
        )
        result = await self.session.execute(stmt)
        booking_id = result.scalar_one_or_none()
        if booking_id is None:
            return None
        return await self.get_by_id(booking_id)
