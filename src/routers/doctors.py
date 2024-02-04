from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from typing_extensions import Annotated

# OAUTH SCHEME
from ..config import oauth2_scheme

router = APIRouter(
    prefix="/doctor",
    tags=["doctors"]
)

# @router.get('/')
# async def get_doctors(token: Annotated[str, Depends(oauth2_scheme)]):
#     return JSONResponse(content={"message": "test", "token": token})