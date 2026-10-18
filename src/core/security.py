from datetime import timedelta, datetime, timezone
from passlib.context import CryptContext
from passlib.exc import UnknownHashError
from jose import jwt, JWTError
from core.config import SECRET_KEY, ALGORITHM

argon_context = CryptContext(schemes=['argon2'], deprecated='auto')


def hash_password(password: str) -> str:
    return argon_context.hash(password)


def verify_password(hashed_password: str, password: str) -> bool:
    try:
        return argon_context.verify(password, hashed_password)
    except UnknownHashError:
        return False


def create_token(data: dict, expires_time: timedelta) -> str:
    encode = data.copy()
    expires = datetime.now(tz=timezone.utc) + expires_time
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get('sub')
        token_type = payload.get('type')

        if not user_id or not token_type:
            raise ValueError('Invalid token payload')
    except JWTError as exc:
        raise ValueError('Invalid token payload') from exc

    return payload
