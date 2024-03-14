# DEPENDENCIES
from typing_extensions import Annotated
from fastapi import Depends, HTTPException
from ..config import oauth2_scheme, ALGORITHM, SECRET_KEY
from ..data.data_models import UserInDb
from jose import JWTError, jwt
from ..data.database import db
from icecream import ic

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        ic(email)
        if email is None:
            raise  HTTPException(
                status_code=401, 
                detail="invalid authentication credentials 1",
                headers={"WWW-Authenticate": "Bearer"}
            )
    except JWTError as e:
        raise  HTTPException(
            status_code=401, 
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )
    user = db["users"].find_one({"email": email})
    if user is None:
        raise  HTTPException(
            status_code=401, 
            detail="invalid authentication credentials 3",
            headers={"WWW-Authenticate": "Bearer"}
        )
    user["_id"] = str(user["_id"])
    if user["rol"] == "patient":
        user["date_of_birth"] = user["date_of_birth"].isoformat()
    return user