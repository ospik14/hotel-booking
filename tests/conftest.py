import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool

from main import app
from core.config import DATABASE_URL
from core.db import session as db_session
from core.db.uow import UnitOfWork
from apps.users.schemas import UserRegister
from apps.users.services import UserService


@pytest_asyncio.fixture(scope='session')
async def setup_engine():
    test_engine = create_async_engine(DATABASE_URL, poolclass=NullPool, echo=False)
    test_session_maker = async_sessionmaker(
        autoflush=False,
        expire_on_commit=False,
        class_=AsyncSession,
        bind=test_engine,
    )
    db_session.engine = test_engine
    db_session.session_maker = test_session_maker
    yield test_engine
    await test_engine.dispose()


@pytest_asyncio.fixture(autouse=True)
async def clean_db(setup_engine):
    async with setup_engine.begin() as conn:
        await conn.execute(
            text('TRUNCATE bookings, rooms, users RESTART IDENTITY CASCADE')
        )
    yield


@pytest_asyncio.fixture
async def client(setup_engine):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as ac:
        yield ac


@pytest_asyncio.fixture
async def user_token(client: AsyncClient) -> str:
    response = await client.post(
        '/users/register',
        json={
            'email': 'user@example.com',
            'password': 'password123',
            'first_name': 'Test',
            'last_name': 'User',
        },
    )
    assert response.status_code == 201

    login = await client.post(
        '/users/login',
        data={'username': 'user@example.com', 'password': 'password123'},
    )
    assert login.status_code == 200
    return login.json()['access_token']


@pytest_asyncio.fixture
async def other_user_token(client: AsyncClient) -> str:
    response = await client.post(
        '/users/register',
        json={
            'email': 'other@example.com',
            'password': 'password123',
            'first_name': 'Other',
            'last_name': 'User',
        },
    )
    assert response.status_code == 201

    login = await client.post(
        '/users/login',
        data={'username': 'other@example.com', 'password': 'password123'},
    )
    assert login.status_code == 200
    return login.json()['access_token']


@pytest_asyncio.fixture
async def admin_token(client: AsyncClient) -> str:
    service = UserService(UnitOfWork(session_maker=db_session.session_maker))
    await service.create_admin(
        UserRegister(
            email='admin@example.com',
            password='password123',
            first_name='Admin',
            last_name='User',
        )
    )
    login = await client.post(
        '/users/login',
        data={'username': 'admin@example.com', 'password': 'password123'},
    )
    assert login.status_code == 200
    return login.json()['access_token']


@pytest_asyncio.fixture
async def room(admin_token: str, client: AsyncClient) -> dict:
    response = await client.post(
        '/rooms/',
        headers={'Authorization': f'Bearer {admin_token}'},
        json={
            'name': 'Deluxe 101',
            'description': 'Nice room',
            'capacity': 2,
            'price_per_night': '100.00',
            'is_active': True,
        },
    )
    assert response.status_code == 201
    return response.json()
