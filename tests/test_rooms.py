import pytest
from httpx import AsyncClient
from tests.helpers import auth_header, future_dates


@pytest.mark.asyncio
async def test_admin_creates_room(client: AsyncClient, admin_token: str):
    response = await client.post(
        '/rooms/',
        headers=auth_header(admin_token),
        json={
            'name': 'Suite',
            'capacity': 3,
            'price_per_night': '150.00',
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data['name'] == 'Suite'
    assert data['price_per_night'] == '150.00'


@pytest.mark.asyncio
async def test_user_cannot_create_room(client: AsyncClient, user_token: str):
    response = await client.post(
        '/rooms/',
        headers=auth_header(user_token),
        json={
            'name': 'Hack Room',
            'capacity': 2,
            'price_per_night': '10.00',
        },
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_room(
    client: AsyncClient, user_token: str, room: dict
):
    response = await client.get(
        f'/rooms/{room["id"]}/',
        headers=auth_header(user_token),
    )
    assert response.status_code == 200
    assert response.json()['id'] == room['id']


@pytest.mark.asyncio
async def test_get_missing_room(client: AsyncClient, user_token: str):
    response = await client.get(
        '/rooms/9999/',
        headers=auth_header(user_token),
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_filter_and_pagination(
    client: AsyncClient, admin_token: str
):
    for i in range(3):
        await client.post(
            '/rooms/',
            headers=auth_header(admin_token),
            json={
                'name': f'Room {i}',
                'capacity': i + 1,
                'price_per_night': str((i + 1) * 50),
            },
        )

    filtered = await client.get('/rooms/', params={'capacity_gte': 2, 'price_lte': 100})
    assert filtered.status_code == 200
    assert all(r['capacity'] >= 2 for r in filtered.json())
    assert all(float(r['price_per_night']) <= 100 for r in filtered.json())

    page = await client.get('/rooms/', params={'limit': 1, 'offset': 1})
    assert page.status_code == 200
    assert len(page.json()) == 1


@pytest.mark.asyncio
async def test_update_room(client: AsyncClient, admin_token: str, room: dict):
    response = await client.patch(
        f'/rooms/{room["id"]}/',
        headers=auth_header(admin_token),
        json={'price_per_night': '200.00'},
    )
    assert response.status_code == 200
    assert response.json()['price_per_night'] == '200.00'


@pytest.mark.asyncio
async def test_invalid_price_and_capacity(client: AsyncClient, admin_token: str):
    bad_price = await client.post(
        '/rooms/',
        headers=auth_header(admin_token),
        json={
            'name': 'Bad Price',
            'capacity': 2,
            'price_per_night': '-1',
        },
    )
    assert bad_price.status_code == 422

    bad_capacity = await client.post(
        '/rooms/',
        headers=auth_header(admin_token),
        json={
            'name': 'Bad Cap',
            'capacity': 0,
            'price_per_night': '10.00',
        },
    )
    assert bad_capacity.status_code == 422


@pytest.mark.asyncio
async def test_deactivate_and_cannot_book(
    client: AsyncClient, admin_token: str, user_token: str, room: dict
):
    deactivated = await client.delete(
        f'/rooms/{room["id"]}/',
        headers=auth_header(admin_token),
    )
    assert deactivated.status_code == 200
    assert deactivated.json()['is_active'] is False

    check_in, check_out = future_dates()
    booking = await client.post(
        '/booking/',
        headers=auth_header(user_token),
        json={
            'room_id': room['id'],
            'check_in_date': check_in,
            'check_out_date': check_out,
            'guests': 1,
        },
    )
    assert booking.status_code == 400


@pytest.mark.asyncio
async def test_available_rooms_endpoint(
    client: AsyncClient, admin_token: str, user_token: str, room: dict
):
    check_in, check_out = future_dates(2, 3)
    await client.post(
        '/booking/',
        headers=auth_header(user_token),
        json={
            'room_id': room['id'],
            'check_in_date': check_in,
            'check_out_date': check_out,
            'guests': 1,
        },
    )

    available = await client.get(
        '/rooms/available/',
        params={'check_in': check_in, 'check_out': check_out, 'guests': 1},
    )
    assert available.status_code == 200
    assert all(r['id'] != room['id'] for r in available.json())
