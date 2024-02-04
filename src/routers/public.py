from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from ..data_models import Patient, Doctor, UserInDb
from ..database import db
from datetime import datetime
from passlib.context import CryptContext
from pymongo.errors import DuplicateKeyError

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


@router.post("/login")
async def login(user: UserInDb):
    response = db.users.find_one({'email': user.email})
    if not response:
        raise HTTPException(status_code=404,  detail='user not found')
    if not verify_password(response.password):
        raise HTTPException(status_code=401,  detail='incorrect password')
    
    print(response)

    return JSONResponse(content={"message": "user autenticated successfully"}, status_code=201)

def verify_password(password, hash):
    return pwd_context.verify(password, hash)

def get_password_hash(password):
    return pwd_context.hash(password)