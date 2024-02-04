# DEPENDENCIES
from typing_extensions import Annotated
from fastapi import Depends, HTTPException
from ..config import oauth2_scheme
from ..data_models import UserInDb

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = decode_token(token)
    if not user:
        raise HTTPException(
            status_code=401, 
            detail="invalid authentication credentials", 
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user


def decode_token(token):
    user = UserInDb(email="rbojorquez1620@gmail.com", password=token+"fakedecode")
    return user