from fastapi import APIRouter, HTTPException, Body
from typing import Annotated
from fastapi.responses import JSONResponse
from ..data.database import db
from ..data.data_models import Degree, ObjectId, Experience, UpdateDoctor, Doctor
from bson import ObjectId as _ObjectId
from datetime import time
from icecream import ic
from ..utility.functions import validate_doctor, validate_experience

# OAUTH SCHEME
from ..config import oauth2_scheme

router = APIRouter(
    prefix="/doctor",
    tags=["doctors"]
)

@router.get('/')
async def get_all_doctors() -> list[Doctor]:
    collecion = db["users"]
    response = collecion.find({"rol": "doctor"})
    doctors = []
    for doctor in response:
        doctor["_id"] = str(doctor["_id"])
        del doctor["experience"]
        del doctor["education"]
        del doctor["appointments"]
        doctors.append(doctor)
    return JSONResponse(content={"message": "successfull request", "response": doctors}, status_code=201)

@router.get("/{id}")
async def get_doctor(id: ObjectId) -> Doctor:
    doctor = await validate_doctor(id)
    return JSONResponse(content={
        "message": "successfull request",
        "response": doctor
    })

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
    return JSONResponse(content={
        "message": "doctor successfully updated"
    }, status_code=201)

@router.put("/{id}/schedule")
async def update_work_schedule(id: ObjectId, start_work: Annotated[time, Body()], finish_work: Annotated[time, Body()], work_days: list[str]):
    await validate_doctor(id)
    start_work_str = start_work.strftime("%H:%M:%S")
    finish_work_str = finish_work.strftime("%H:%M:%S")

    update_data = {
        "start_work": start_work_str,
        "finish_work": finish_work_str,
        "work_days": work_days
    }

    db["users"].update_one(
        {"_id": _ObjectId(id)}, {"$set": update_data}
    )
    return JSONResponse(
        content= {
            "message": "work schedule successfully updated"
        },
        status_code=201
    )

@router.delete("/{id}")
async def delete_doctor(id: ObjectId):
    await validate_doctor(id)
    collection = db["users"]
    collection.delete_one({"_id": _ObjectId(id)})
    return JSONResponse(content={
        "message": "doctor successfully deleted"
    }, status_code=201)
