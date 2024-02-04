from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from ..data_models import Patient, Doctor
from ..database import db
from ..config import pwd_context, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import datetime
from passlib.context import CryptContext
from pymongo.errors import DuplicateKeyError
from typing_extensions import Annotated
from jose import jwt, JWTError
from icecream import ic
from datetime import date, timedelta, timezone

router = APIRouter(
    prefix="/public",
    tags=["public"]
)

@router.post("/patients")
async def register_user(patient: Patient):
    try:
        patients = db["users"]
        # hash pwd
        patient.password = get_password_hash(patient.password)
        patient.date_of_birth = datetime.combine(patient.date_of_birth, datetime.min.time())
        patients.insert_one(patient.model_dump())
        return JSONResponse(content={"message": "users created successfully"},  status_code=201)
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail={"error": "the  email is already in use"})

@router.post('/doctor')
async def register_doctor(doctor: Doctor):
    try:
        doctors = db['users']
        # hast pwd
        doctor.password = get_password_hash(doctor.password)
        doctors.insert_one(doctor.model_dump())
        return JSONResponse(content={"message": "doctor added successfully"}, status_code=201)
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail={"error": "the email or the license number are already in use"})


@router.post("/token")
async def login_for_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = db["users"].find_one({"email": form_data.username})
    if not user_dict:
        raise HTTPException(
            status_code=401, 
            detail="incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    if not verify_password(form_data.password, user_dict["password"]):
        raise HTTPException(
            status_code=401, 
            detail="incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    user_dict["_id"] =  str(user_dict["_id"])
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub":  user_dict["email"]},
        expires_delta=access_token_expires 
    )
    return JSONResponse(content={"access_token": access_token, "token_type": "bearer"})

def verify_password(password, hash):
    return pwd_context.verify(password, hash)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) +  expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    # update the dict
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt