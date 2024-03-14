from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from ..data.data_models import Appointment, ObjectId
from bson import ObjectId as _ObjectId
from fastapi.responses import JSONResponse
from ..data.database import db
from ..utility.functions import validate_appointment, appointment_exist
from icecream import ic

router = APIRouter(
    prefix="/appointment",
    tags=["appointments"]
)

@router.get("/")
async def get_all_appointments() -> list[Appointment]:
    collection = db["appointments"]
    response = collection.find()
    appointments = []

    for appointment in response:
        if appointment:
            appointment['_id'] = str(appointment['_id'])
            appointment["patient_id"] = str(appointment["patient_id"])
            appointment["doctor_id"] = str(appointment["doctor_id"])
            appointment["date"] = appointment["date"].isoformat()
            appointments.append(appointment)

    return JSONResponse(
        content={
            "message": "successfull request",
            "response": appointments
        },
        status_code=201
    )

@router.get("/{appointment_id}")
async def get_one_appointment(appointment_id: ObjectId) -> Appointment:
    appointment = db["appointments"].find_one({"_id": _ObjectId(appointment_id)})
    if appointment:
        appointment['_id'] = str(appointment['_id'])
        appointment["patient_id"] = str(appointment["patient_id"])
        appointment["doctor_id"] = str(appointment["doctor_id"])
        appointment["date"] = appointment["date"].isoformat()
    return JSONResponse(
        content={
            "message": "successfull request",
            "response": appointment
        },
        status_code=201
    )

@router.post("/")
async def create_appointment(
    appointment: Appointment
):
    to_json = await validate_appointment(appointment)
    users_index = [_ObjectId(appointment.patient_id), _ObjectId(appointment.doctor_id)]
    appoint_index = db["appointments"].insert_one(to_json).inserted_id
    db["users"].update_many({"_id": {"$in": users_index}}, {"$push": {"appointments": _ObjectId(appoint_index)}})
    return JSONResponse(
        content= {
            "message": "appointment added successfully"
        },
        status_code=201
    )

@router.put("/{appointment_id}")
async def edit_appointment(appointment_id: ObjectId, new_appointment: Appointment):
    existing_appointment = db["appointments"].find_one({"_id": _ObjectId(appointment_id)})
    if not existing_appointment:
        raise HTTPException(status_code=404, detail="appointment not found")
    
    validated_appointment = await validate_appointment(new_appointment)

    db["appointments"].update_one(
        {"_id": _ObjectId(appointment_id)},
        {"$set": validated_appointment}
    )

    return JSONResponse(
        content={
            "message": "appointment successfully updated"
        },
        status_code=201
    )

@router.delete("/{appointment_id}")
async def delete_appointment(appointment_id: ObjectId):
    await appointment_exist(appointment_id)
    db["appointments"].delete_one({"_id": _ObjectId(appointment_id)})
    return JSONResponse(
        content={
            "message": "appointment successfully canceled"
        },
        status_code=201
    )

@router.get("/patient/{patient_id}")
async def get_patient_appointments(patient_id: ObjectId):
    collection = db["appointments"]
    response = collection.find({"patient_id": _ObjectId(patient_id)})
    appointments = []

    for appointment in response:
        if appointment:
            appointment['_id'] = str(appointment['_id'])
            appointment["patient_id"] = str(appointment["patient_id"])
            appointment["doctor_id"] = str(appointment["doctor_id"])
            appointment["date"] = appointment["date"].isoformat()
            appointments.append(appointment)

    return JSONResponse(
        content={
            "message": "successfull request",
            "response": appointments
        },
        status_code=201
    )

@router.get("/doctor/{doctor_id}")
async def get_doctor_appointments(patient_id: ObjectId):
    collection = db["appointments"]
    response = collection.find({"doctor_id": _ObjectId(patient_id)})
    appointments = []

    for appointment in response:
        if appointment:
            appointment['_id'] = str(appointment['_id'])
            appointment["patient_id"] = str(appointment["patient_id"])
            appointment["doctor_id"] = str(appointment["doctor_id"])
            appointment["date"] = appointment["date"].isoformat()
            appointments.append(appointment)

    return JSONResponse(
        content={
            "message": "successfull request",
            "response": appointments
        },
        status_code=201
    )