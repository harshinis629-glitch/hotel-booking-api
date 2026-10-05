from datetime import datetime, timedelta, timezone
from jose import jwt,JWTError
from passlib.context import CryptContext
from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer

import os
from dotenv import load_dotenv

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
)


SECRET_KEY=os.getenv("JWT_SECRET")
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user_id:str)->str:
    expire=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload={"sub":user_id,"exp":expire}
    token=jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return token

def get_current_user(token:str=Depends(oauth2_scheme)):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id=payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401,detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401,detail="Invalid or expired token")