from fastapi import APIRouter, Depends
from typing_extensions import Annotated
from ..data.data_models import UserInDb

# DEPENDENCIES
from ..dependencies.global_dep import get_current_user

router = APIRouter(
    prefix="/user",
    tags=["users"]
)

@router.get("/me")
async def read_user_info(current_user: Annotated[UserInDb, Depends(get_current_user)]):
    return current_user