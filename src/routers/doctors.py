from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing_extensions import Annotated
from ..database import db
from ..data_models import Degree, ObjectId, Experience, UpdateDoctor
from bson import ObjectId as _ObjectId
from icecream import ic

# OAUTH SCHEME
from ..config import oauth2_scheme

router = APIRouter(
    prefix="/doctor",
    tags=["doctors"]
)

'''
    DOCTOR CRUD
'''
@router.get('/')
async def get_all_doctors():
    collecion = db["users"]
    response = collecion.find({"rol": "doctor"})
    doctors = []
    for doctor in response:
        doctor["_id"] = str(doctor["_id"])
        for exp in doctor["experience"]:
            exp["_id"] = str(exp["_id"])
        doctors.append(doctor)
    return JSONResponse(content={"message": "successfull request", "response": doctors}, status_code=201)

@router.put("/{id}")
async def update_doctor(id: ObjectId, new_doctor: UpdateDoctor):
    doctor = await validate_doctor(id)
    doctor.update({
        "username": new_doctor.username if new_doctor.username else doctor["username"],
        "lastname": new_doctor.lastname if new_doctor.lastname else doctor["lastname"],
        "email": new_doctor.email if new_doctor.email else doctor["email"],
        "speciality": new_doctor.speciality if new_doctor.speciality else doctor["speciality"],
        "contact_number": new_doctor.contact_number if new_doctor.contact_number else doctor["contact_number"],
        "license_number": new_doctor.license_number if new_doctor.license_number else doctor["license_number"],
        "about": new_doctor.about if new_doctor.about else doctor.get("about", "")
    })
    collection = db["users"]
    collection.update_one({"_id": _ObjectId(id)}, {"$set": doctor})
    # ic(doctor)
    return JSONResponse(content={
        "message": "doctor successfully updated"
    }, status_code=201)

@router.delete("/{id}")
async def delete_doctor(id: ObjectId):
    await validate_doctor(id)
    collection = db["users"]
    collection.delete_one({"_id": _ObjectId(id)})
    return JSONResponse(content={
        "message": "doctor successfully deleted"
    }, status_code=201)


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


'''
   DOCTOR EXPERIENCE CRUD 
'''
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
    experience = [exp.update({"_id": str(exp["_id"])}) or exp for exp in doctor["experience"]]
    return  JSONResponse(content={
        "message":"successfull request",
        "reponse":experience
    },status_code=201)

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
    }, status_code=201)

async def validate_doctor(id: _ObjectId) -> dict:
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