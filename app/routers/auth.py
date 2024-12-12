from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from typing import Optional
import jwt


SECRET_KEY = "I3b1zJhyuV7_tR-9vwK1xN8YltOK7V1TyqTsnCzq1Ww"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()
# Function to validate the JWT
def validate_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload 
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# route that requires the token to access
@router.get("/secure-data")
async def get_secure_data(payload: dict = Depends(validate_token)):
    return {"message": "This is secured data", "user": payload}

@router.post("/token")
def generate_token(username: str, password: str):
    if username == "admin" and password == "password":
        payload = {"sub": username}
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token": token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
