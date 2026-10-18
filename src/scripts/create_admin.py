"""Create an admin user. Run from project root:

    PYTHONPATH=src python -m scripts.create_admin \
        --email admin@example.com \
        --password 'StrongPass1' \
        --first-name Admin \
        --last-name User
"""

import argparse
import asyncio
import sys

from apps.users.schemas import UserRegister
from apps.users.services import UserService
from core.db.session import session_maker
from core.db.uow import UnitOfWork
from core.exceptions import UserAlreadyExistsError


async def main() -> int:
    parser = argparse.ArgumentParser(description='Create an admin user')
    parser.add_argument('--email', required=True)
    parser.add_argument('--password', required=True)
    parser.add_argument('--first-name', required=True)
    parser.add_argument('--last-name', required=True)
    args = parser.parse_args()

    service = UserService(UnitOfWork(session_maker=session_maker))
    try:
        user = await service.create_admin(
            UserRegister(
                email=args.email,
                password=args.password,
                first_name=args.first_name,
                last_name=args.last_name,
            )
        )
    except UserAlreadyExistsError:
        print('User with this email already exists', file=sys.stderr)
        return 1

    print(f'Admin created: id={user.id} email={user.email}')
    return 0


if __name__ == '__main__':
    raise SystemExit(asyncio.run(main()))
