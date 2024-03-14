from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from ..utility.functions import validate_doctor, validate_experience
from bson import ObjectId as _ObjectId
from ..data.data_models import ObjectId, Experience
from ..data.database import db
from icecream import ic

router = APIRouter(
    prefix="/doctor/experience",
    tags=["doctor experience"]
)

@router.post("/{id}")
async def add_doctor_experience(id: ObjectId, experience: Experience):
    doctor = await validate_doctor(id)
    await validate_experience(doctor["experience"], experience)
    to_json = experience.model_dump()
    to_json["_id"] = _ObjectId()
    db["users"].update_one(
        {"_id": _ObjectId(id)},
        { "$push": {"experience": to_json}}
    )
    return JSONResponse(content={"message": "work experience aggregate successfully"}, status_code=201)

@router.get("/{id}")
async def get_doctor_experience(id: ObjectId) -> list[Experience]:
    doctor = await validate_doctor(id)
    experience = [exp.update({"_id": str(exp["_id"])}) or exp for exp in doctor["experience"]]
    return  JSONResponse(content={
        "message":"successfull request",
        "reponse":experience
    },status_code=201)

@router.get("/{id}/{experience_id}")
async def get_one_experience(id: ObjectId, education_id: ObjectId) -> Experience:
    doctor = await validate_doctor(id)
    experiences = doctor["experience"]
    doctor_exp = next((exp for exp in experiences if exp["_id"] == _ObjectId(education_id)), None)
    if not doctor_exp:
        raise HTTPException(status_code=404, detail="work experience not found")
    doctor_exp["_id"] = str(doctor_exp["_id"])
    return JSONResponse(content={
        "message": "successfull request",
        "response": doctor_exp
    })

@router.put("/{id}/{experience_id}")
async def update_doctor_experience(id: ObjectId, experience_id: ObjectId, newExperience: Experience):
    doctor = await validate_doctor(id)
    collection = db["users"]
    await validate_experience(doctor["experience"], newExperience)
    to_json = newExperience.model_dump()
    to_json["_id"] = _ObjectId(experience_id)
    collection.update_one({"experience._id": _ObjectId(experience_id)}, {"$set": {"experience.$": to_json}})
    return JSONResponse(content={
        "message": "work experience successfully updated",
    }, status_code=201)

@router.delete("/{id}/{experience_id}")
async def delete_doctor_experience(id: ObjectId, experience_id: ObjectId):
    await validate_doctor(id)
    collection = db["users"]
    collection.delete_one({"experience._id": _ObjectId(experience_id)})
    return JSONResponse(content={
        "message": "work experience successfully deleted"
    }, status_code=201)
