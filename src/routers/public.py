from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from ..data_models import Patient, Doctor, UserInDb
from ..database import db
from datetime import datetime
from passlib.context import CryptContext
from pymongo.errors import DuplicateKeyError
from typing_extensions import Annotated
from icecream import ic
from datetime import date

router = APIRouter(
    prefix="/public",
    tags=["public"]
)

pwd_context =CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/patients")
async def register_user(patient: Patient):
    try:
        patients = db["patients"]
        # hash pwd
        patient.password = get_password_hash(patient.password)
        patient.date_of_birth = datetime.combine(patient.date_of_birth, datetime.min.time())
        patients.insert_one(patient.model_dump())
        return JSONResponse(content={"message": "users created successfully"},  status_code=201)
    except DuplicateKeyError:
        raise HTTPException(status_code=401, detail={"error": "the  email is already in use"})

@router.post('/doctor')
async def register_doctor(doctor: Doctor):
    try:
        doctors = db['doctors']
        # hast pwd
        doctor.password = get_password_hash(doctor.password)
        doctors.insert_one(doctor.model_dump())
        return JSONResponse(content={"message": "doctor added successfully"}, status_code=201)
    except DuplicateKeyError:
        raise HTTPException(status_code=401, detail={"error": "the email or the license number are already in use"})


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = db["patients"].find_one({"email": form_data.username})
    if not user_dict:
        raise HTTPException(status_code=401,  detail="incorrect username or password")
    user_dict["_id"] = str(user_dict["_id"])
    user_dict["date_of_birth"] = user_dict["date_of_birth"].isoformat()
    # check password
    if not verify_password(form_data.password, user_dict["password"]):
        raise HTTPException(status_code=401, detail="incorrect username or password")
    ic(user_dict)
    return JSONResponse(content={"access_token": form_data.password, "token_type": "bearer"})

def verify_password(password, hash):
    return pwd_context.verify(password, hash)

def get_password_hash(password):
    return pwd_context.hash(password)