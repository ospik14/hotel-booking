import pytest
from httpx import AsyncClient
from jose import jwt
from core.config import SECRET_KEY, ALGORITHM
from tests.helpers import auth_header


@pytest.mark.asyncio
async def test_register_success(client: AsyncClient):
    response = await client.post(
        '/users/register',
        json={
            'email': 'new@example.com',
            'password': 'password123',
            'first_name': 'New',
            'last_name': 'User',
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data['email'] == 'new@example.com'
    assert 'hashed_password' not in data
    assert data['role'] == 'user'


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    payload = {
        'email': 'dup@example.com',
        'password': 'password123',
        'first_name': 'Dup',
        'last_name': 'User',
    }
    assert (await client.post('/users/register', json=payload)).status_code == 201
    response = await client.post('/users/register', json=payload)
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_register_ignores_admin_privilege_attempt(client: AsyncClient):
    response = await client.post(
        '/users/register',
        json={
            'email': 'hacker@example.com',
            'password': 'password123',
            'first_name': 'Hack',
            'last_name': 'Er',
            'role': 'admin',
        },
    )
    # extra field is ignored by pydantic; user is always USER
    assert response.status_code == 201
    assert response.json()['role'] == 'user'


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    await client.post(
        '/users/register',
        json={
            'email': 'login@example.com',
            'password': 'password123',
            'first_name': 'Log',
            'last_name': 'In',
        },
    )
    response = await client.post(
        '/users/login',
        data={'username': 'login@example.com', 'password': 'wrongpass1'},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    await client.post(
        '/users/register',
        json={
            'email': 'ok@example.com',
            'password': 'password123',
            'first_name': 'Ok',
            'last_name': 'User',
        },
    )
    response = await client.post(
        '/users/login',
        data={'username': 'ok@example.com', 'password': 'password123'},
    )
    assert response.status_code == 200
    assert 'access_token' in response.json()


@pytest.mark.asyncio
async def test_invalid_jwt(client: AsyncClient):
    response = await client.get(
        '/users/me/',
        headers=auth_header('invalid.token.value'),
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_expired_or_tampered_jwt_role(client: AsyncClient, user_token: str):
    payload = jwt.decode(user_token, SECRET_KEY, algorithms=[ALGORITHM])
    payload['role'] = 'admin'
    forged = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    response = await client.post(
        '/rooms/',
        headers=auth_header(forged),
        json={
            'name': 'Should Fail',
            'capacity': 2,
            'price_per_night': '10.00',
        },
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_user_cannot_access_admin_endpoint(
    client: AsyncClient, user_token: str
):
    response = await client.post(
        '/rooms/',
        headers=auth_header(user_token),
        json={
            'name': 'Nope',
            'capacity': 2,
            'price_per_night': '10.00',
        },
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_and_update_profile(client: AsyncClient, user_token: str):
    me = await client.get('/users/me/', headers=auth_header(user_token))
    assert me.status_code == 200
    assert me.json()['email'] == 'user@example.com'

    updated = await client.patch(
        '/users/me/',
        headers=auth_header(user_token),
        json={'first_name': 'Updated'},
    )
    assert updated.status_code == 200
    assert updated.json()['first_name'] == 'Updated'
    assert updated.json()['role'] == 'user'
