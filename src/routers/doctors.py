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
    # ic(doctors)
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
    to_json = experience.model_dump()
    to_json["_id"] = _ObjectId()
    db["users"].update_one(
        {"_id": _ObjectId(id)},
        { "$push": {"experience": to_json}}
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

@router.put("/experience/{id}/{experience_id}")
async def update_doctor_experience(id: ObjectId, experience_id: ObjectId, newExperience: Experience):
    doctor = await validate_doctor(id)
    collection = db["users"]
    await validate_experience(doctor["experience"], newExperience, experience_id)
    to_json = newExperience.model_dump()
    to_json["_id"] = _ObjectId(experience_id)
    collection.update_one({"experience._id": _ObjectId(experience_id)}, {"$set": {"experience.$": to_json}})
    # ic(doctor["experience"])
    return JSONResponse(content={
        "message": "work experience successfully updated",
    }, status_code=201)

@router.delete("/experience/{id}/{experience_id}")
async def delete_doctor_experience(id: ObjectId, experience_id: ObjectId):
    await validate_doctor(id)
    collection = db["users"]
    collection.delete_one({"experience._id": _ObjectId(experience_id)})
    return JSONResponse(content={
        "message": "work experience successfully deleted"
    })

async def validate_doctor(id: _ObjectId):
    # ic(id)
    collection = db["users"]
    doctor = collection.find_one({"_id": _ObjectId(id), "rol": "doctor"})
    if not doctor:
        raise HTTPException(status_code=404, detail="doctor not found")
    return doctor

async def validate_experience(exps, experience, id):
    experiences = [{key: value for key, value in exp.items() if key != "_id"} for exp in exps]
    existing_exp = next((exp for exp in experiences if exp == experience.model_dump()), None)
    if existing_exp:
        raise HTTPException(status_code=400, detail="this work experience is already registered") 
    if _ObjectId(id) not in {exp["_id"] for exp in exps}:
        raise HTTPException(status_code=404, detail="experience not found with provided id")
    return