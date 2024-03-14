from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from ..data.data_models import Developer
from ..data.database import db
from icecream import ic

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)


@router.post("/")
async def create_developer_profile(profile: Developer):
    collection = db["users"]
    admin = collection.find_one({"rol": "developer"})
    if admin:
        raise HTTPException(status_code=400,  detail="admin profile already created")
    user = collection.find_one({"email": profile.email})
    if user:
        raise HTTPException(status_code=400, detail="email already in use")
    collection.insert_one(profile.model_dump())
    return JSONResponse(content={"message": "dev created successfully"})