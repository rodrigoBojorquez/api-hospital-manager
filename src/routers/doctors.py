from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing_extensions import Annotated
from ..database import db
from ..data_models import Degree, ObjectId
from icecream import ic

# OAUTH SCHEME
from ..config import oauth2_scheme

router = APIRouter(
    prefix="/doctor",
    tags=["doctors"]
)

@router.get('/')
async def get_all_doctors():
    collecion = db["users"]
    doctors = collecion
    return JSONResponse(content={"message": "successfull request", "token": doctors}, status_code=201)

@router.post("/education/{id}")
async def add_degree(id: ObjectId, degree: Degree):
    collection = db["users"]
    doctor = collection.find_one({"_id": id,  "role": "doctor"})
    ic(doctor)
    if not doctor:
        raise HTTPException(status_code=404, detail="doctor with this id does not exist")
    return JSONResponse(
        content={"message": "degree added successfully",  "degree": degree},
        status_code=201
    )