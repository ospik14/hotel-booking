import os
from dotenv import load_dotenv
from datetime import timedelta, datetime, timezone
from passlib.context import CryptContext
from passlib.exc import UnknownHashError
from jose import jwt, JWTError

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

argon_context = CryptContext(schemes=['argon2'], deprecated='auto')

def hash_password(password: str):
    return argon_context.hash(password)

def verify_password(hashed_password: str, password: str):
    try:
        return argon_context.verify(password, hashed_password)
    except UnknownHashError:
        return False

def create_token(data: dict, expires_time: timedelta):
    encode = data.copy()
    expires = datetime.now(tz=timezone.utc) + expires_time
    encode.update({'exp': expires})
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    return token

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get('sub')
        type = payload.get('type')

        if not user_id or not type:
            raise ValueError("Invalid token payload")
        
    except JWTError:
        raise ValueError("Invalid token payload")

    return payload
        