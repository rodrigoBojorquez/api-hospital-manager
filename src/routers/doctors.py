from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing_extensions import Annotated
from ..database import db
from ..data_models import Degree, ObjectId, Experience
from bson import ObjectId as _ObjectId
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
    response = collecion.find()
    doctors = []
    for doctor in response:
        doctor["_id"] = str(doctor["_id"])
        doctors.append(doctor)
    ic(doctors)
    return JSONResponse(content={"message": "successfull request", "token": doctors}, status_code=201)

@router.post("/education/{id}")
async def add_degree(id: ObjectId, degree: Degree):
    collection = db["users"]
    doctor = collection.find_one({"_id": id,  "role": "doctor"})
    if not doctor:
        raise HTTPException(status_code=404, detail="doctor with this id does not exist")
    return JSONResponse(
        content={"message": "degree added successfully",  "degree": degree},
        status_code=201
    )

@router.post("/experience/{id}")
async def add_doctor_experience(id: ObjectId, experience: Experience):
    doctor = await validate_doctor(id)
    await validate_experience(doctor, experience)
    response = db["users"].update_one(
        {"_id": _ObjectId(id)},
        { "$push": {"experience": experience.model_dump()}}
    )
    return JSONResponse(content={"message": "work experience aggregate successfully"}, status_code=201)

@router.get("/experience/{id}")
async def get_doctor_experience(id: ObjectId):
    doctor = await validate_doctor(id)
    exp = doctor["experience"]
    return  JSONResponse(content={
        "message":"successfull request",
        "data":exp
    },status_code=200)

'''
    TODO:
        - agregar validacion de maximo 10 experiencias laborales
        - agregar un ID a cada experiencia laboral
'''

@router.put("/experience/{id}")
async def update_doctor_experience(id: ObjectId, newExperience: Experience):
    return

async def validate_doctor(id: _ObjectId):
    ic(id)
    collection = db["users"]
    doctor = collection.find_one({"_id": _ObjectId(id), "rol": "doctor"})
    if not doctor:
        raise HTTPException(status_code=404, detail="doctor not found")
    return doctor

async def validate_experience(doctor, experience):
    existing_exp = next((exp for exp in doctor["experience"] if exp == experience.model_dump()), None)
    if existing_exp:
        raise HTTPException(status_code=400, detail="this work experience is already registered")
    return