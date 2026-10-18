import asyncio
from datetime import date, timedelta
from decimal import Decimal

import pytest
from httpx import ASGITransport, AsyncClient

from main import app
from tests.helpers import auth_header, future_dates


@pytest.mark.asyncio
async def test_create_booking_success(
    client: AsyncClient, user_token: str, room: dict
):
    check_in, check_out = future_dates(1, 2)
    response = await client.post(
        '/booking/',
        headers=auth_header(user_token),
        json={
            'room_id': room['id'],
            'check_in_date': check_in,
            'check_out_date': check_out,
            'guests': 2,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data['status'] == 'CONFIRMED'
    assert data['total_price'] == '200.00'
    assert data['price_per_night'] == '100.00'
    assert data['room']['id'] == room['id']


@pytest.mark.asyncio
async def test_booking_missing_room(client: AsyncClient, user_token: str):
    check_in, check_out = future_dates()
    response = await client.post(
        '/booking/',
        headers=auth_header(user_token),
        json={
            'room_id': 9999,
            'check_in_date': check_in,
            'check_out_date': check_out,
            'guests': 1,
        },
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_booking_invalid_dates(client: AsyncClient, user_token: str, room: dict):
    today = date.today()
    response = await client.post(
        '/booking/',
        headers=auth_header(user_token),
        json={
            'room_id': room['id'],
            'check_in_date': today.isoformat(),
            'check_out_date': today.isoformat(),
            'guests': 1,
        },
    )
    assert response.status_code == 422

    past = today - timedelta(days=2)
    response = await client.post(
        '/booking/',
        headers=auth_header(user_token),
        json={
            'room_id': room['id'],
            'check_in_date': past.isoformat(),
            'check_out_date': (past + timedelta(days=1)).isoformat(),
            'guests': 1,
        },
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_overlap_and_adjacent_bookings(
    client: AsyncClient, user_token: str, other_user_token: str, room: dict
):
    check_in, check_out = future_dates(5, 3)
    first = await client.post(
        '/booking/',
        headers=auth_header(user_token),
        json={
            'room_id': room['id'],
            'check_in_date': check_in,
            'check_out_date': check_out,
            'guests': 1,
        },
    )
    assert first.status_code == 201

    overlap = await client.post(
        '/booking/',
        headers=auth_header(other_user_token),
        json={
            'room_id': room['id'],
            'check_in_date': (
                date.fromisoformat(check_in) + timedelta(days=1)
            ).isoformat(),
            'check_out_date': (
                date.fromisoformat(check_out) + timedelta(days=1)
            ).isoformat(),
            'guests': 1,
        },
    )
    assert overlap.status_code == 409

    adjacent = await client.post(
        '/booking/',
        headers=auth_header(other_user_token),
        json={
            'room_id': room['id'],
            'check_in_date': check_out,
            'check_out_date': (
                date.fromisoformat(check_out) + timedelta(days=2)
            ).isoformat(),
            'guests': 1,
        },
    )
    assert adjacent.status_code == 201


@pytest.mark.asyncio
async def test_concurrent_bookings(
    user_token: str, other_user_token: str, room: dict
):
    check_in, check_out = future_dates(10, 2)

    async def book(token: str):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url='http://test') as client:
            return await client.post(
                '/booking/',
                headers=auth_header(token),
                json={
                    'room_id': room['id'],
                    'check_in_date': check_in,
                    'check_out_date': check_out,
                    'guests': 1,
                },
            )

    results = await asyncio.gather(
        book(user_token),
        book(other_user_token),
    )
    statuses = sorted(r.status_code for r in results)
    assert statuses == [201, 409]


@pytest.mark.asyncio
async def test_capacity_exceeded(
    client: AsyncClient, user_token: str, room: dict
):
    check_in, check_out = future_dates()
    response = await client.post(
        '/booking/',
        headers=auth_header(user_token),
        json={
            'room_id': room['id'],
            'check_in_date': check_in,
            'check_out_date': check_out,
            'guests': 5,
        },
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_cancel_own_booking(
    client: AsyncClient, user_token: str, room: dict
):
    check_in, check_out = future_dates()
    created = await client.post(
        '/booking/',
        headers=auth_header(user_token),
        json={
            'room_id': room['id'],
            'check_in_date': check_in,
            'check_out_date': check_out,
            'guests': 1,
        },
    )
    booking_id = created.json()['id']

    cancel = await client.delete(
        f'/booking/{booking_id}/',
        headers=auth_header(user_token),
    )
    assert cancel.status_code == 204

    details = await client.get(
        f'/booking/{booking_id}/',
        headers=auth_header(user_token),
    )
    assert details.json()['status'] == 'CANCELLED'


@pytest.mark.asyncio
async def test_cancel_other_users_booking(
    client: AsyncClient, user_token: str, other_user_token: str, room: dict
):
    check_in, check_out = future_dates()
    created = await client.post(
        '/booking/',
        headers=auth_header(user_token),
        json={
            'room_id': room['id'],
            'check_in_date': check_in,
            'check_out_date': check_out,
            'guests': 1,
        },
    )
    booking_id = created.json()['id']

    response = await client.delete(
        f'/booking/{booking_id}/',
        headers=auth_header(other_user_token),
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_cancel_missing_and_double_cancel(
    client: AsyncClient, user_token: str, room: dict
):
    missing = await client.delete(
        '/booking/9999/',
        headers=auth_header(user_token),
    )
    assert missing.status_code == 404

    check_in, check_out = future_dates()
    created = await client.post(
        '/booking/',
        headers=auth_header(user_token),
        json={
            'room_id': room['id'],
            'check_in_date': check_in,
            'check_out_date': check_out,
            'guests': 1,
        },
    )
    booking_id = created.json()['id']
    assert (
        await client.delete(
            f'/booking/{booking_id}/',
            headers=auth_header(user_token),
        )
    ).status_code == 204
    second = await client.delete(
        f'/booking/{booking_id}/',
        headers=auth_header(user_token),
    )
    assert second.status_code == 409


@pytest.mark.asyncio
async def test_cancelled_booking_frees_room(
    client: AsyncClient, user_token: str, other_user_token: str, room: dict
):
    check_in, check_out = future_dates(3, 2)
    created = await client.post(
        '/booking/',
        headers=auth_header(user_token),
        json={
            'room_id': room['id'],
            'check_in_date': check_in,
            'check_out_date': check_out,
            'guests': 1,
        },
    )
    booking_id = created.json()['id']
    await client.delete(
        f'/booking/{booking_id}/',
        headers=auth_header(user_token),
    )

    again = await client.post(
        '/booking/',
        headers=auth_header(other_user_token),
        json={
            'room_id': room['id'],
            'check_in_date': check_in,
            'check_out_date': check_out,
            'guests': 1,
        },
    )
    assert again.status_code == 201


@pytest.mark.asyncio
async def test_get_own_and_foreign_booking(
    client: AsyncClient, user_token: str, other_user_token: str, room: dict
):
    check_in, check_out = future_dates()
    created = await client.post(
        '/booking/',
        headers=auth_header(user_token),
        json={
            'room_id': room['id'],
            'check_in_date': check_in,
            'check_out_date': check_out,
            'guests': 1,
        },
    )
    booking_id = created.json()['id']

    mine = await client.get('/booking/my/', headers=auth_header(user_token))
    assert mine.status_code == 200
    assert len(mine.json()) == 1

    foreign = await client.get(
        f'/booking/{booking_id}/',
        headers=auth_header(other_user_token),
    )
    assert foreign.status_code == 404


@pytest.mark.asyncio
async def test_price_snapshot_immutable(
    client: AsyncClient, admin_token: str, user_token: str, room: dict
):
    check_in, check_out = future_dates(1, 3)
    created = await client.post(
        '/booking/',
        headers=auth_header(user_token),
        json={
            'room_id': room['id'],
            'check_in_date': check_in,
            'check_out_date': check_out,
            'guests': 1,
        },
    )
    assert created.status_code == 201
    assert Decimal(created.json()['total_price']) == Decimal('300.00')

    await client.patch(
        f'/rooms/{room["id"]}/',
        headers=auth_header(admin_token),
        json={'price_per_night': '999.00'},
    )

    details = await client.get(
        f'/booking/{created.json()["id"]}/',
        headers=auth_header(user_token),
    )
    assert details.json()['price_per_night'] == '100.00'
    assert details.json()['total_price'] == '300.00'
    assert details.json()['room']['price_per_night'] == '999.00'
