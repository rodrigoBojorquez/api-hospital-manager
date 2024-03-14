from ..data.database import db
from ..data.data_models import ObjectId, Degree, Experience, Appointment
from bson import ObjectId as _ObjectId
from fastapi import HTTPException
from datetime import datetime
from icecream import ic


async def validate_doctor(id: _ObjectId) -> dict:
    collection = db["users"]
    doctor = collection.find_one({"_id": _ObjectId(id), "rol": "doctor"})
    if not doctor:
        raise HTTPException(status_code=404, detail="doctor not found")
    doctor["_id"] = str(doctor["_id"])
    return doctor

async def validate_patient(id: _ObjectId) -> dict:
    collection = db["users"]
    patient = collection.find_one({"_id": _ObjectId(id), "rol": "patient"})
    if not patient:
        raise HTTPException(status_code=404, detail="patient not found")
    patient["_id"] = str(patient["_id"])
    return patient

async def validate_experience(
    exps: list[dict], 
    experience: Degree
):
    experiences = [{key: value for key, value in exp.items() if key != "_id"} for exp in exps]
    existing_exp = next((exp for exp in experiences if exp == experience.model_dump()), None)
    if existing_exp:
        raise HTTPException(status_code=400, detail="this work experience is already registered") 
    return

async def validate_education(
    edus: list[dict],
    degree: Experience
):
    education = [{key:value for key, value in edu.items() if key != "_id"} for edu in edus]
    existing_edu = next((edu for edu in education if edu == degree.model_dump()), None)
    if existing_edu:
        raise HTTPException(status_code=400, detail="this degree is already registered")
    return

async def validate_appointment(
    appointment: Appointment
) -> dict:
    week_days = {
        0: "lunes",
        1: "martes",
        2: "miercoles",
        3: "jueves",
        4: "viernes",
        5: "sabado",
        6: "domingo"
    }

    patient = await validate_patient(appointment.patient_id)
    doctor = await validate_doctor(appointment.doctor_id)
    work_days = doctor["work_days"]
    day = appointment.date.weekday()

    ic(week_days[day])
    ic(work_days)

    if week_days[day] not in work_days:
        raise HTTPException(status_code=400, detail="the doctor doesn't work that day")
    if appointment.date.minute != 0 or appointment.date.second != 0:
        raise HTTPException(status_code=400, detail="invalid appointment hour")
    
    appointment_list = patient["appointments"] + doctor["appointments"]
    response = db["appointments"].find({"_id": {"$in": appointment_list}})

    for appoint in response:
        if appoint["date"].hour == appointment.date.hour:
            raise HTTPException(status_code=400, detail="busy appointment schedule")

    appointment.patient_id = _ObjectId(appointment.patient_id)
    appointment.doctor_id = _ObjectId(appointment.doctor_id)
    
    return appointment.model_dump()

async def appointment_exist(id: ObjectId) -> dict:
    appointment = db["appointments"].find_one({"_id": _ObjectId(id)})
    if not appointment:
        raise HTTPException(status_code=404, detail="appointment not found")
    return appointment