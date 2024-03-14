from ..data.data_models import ObjectId, Degree
from ..data.database import db
from fastapi import HTTPException, APIRouter
from fastapi.responses import JSONResponse
from ..utility.functions import validate_doctor, validate_education
from bson import ObjectId as _ObjectId

router = APIRouter(
    prefix="/doctor/education",
    tags=["doctor education"]
)

@router.post("/{doctor_id}")
async def add_doctor_degree(doctor_id: ObjectId, degree: Degree):
    doctor = await validate_doctor(doctor_id)
    await validate_education(doctor["education"], degree)
    to_json = degree.model_dump()
    to_json["_id"] = _ObjectId()
    db["users"].update_one(
        {"_id": _ObjectId(doctor_id)},
        {
            "$push": {
            "education": to_json
            }
        }
    )
    return JSONResponse(
        content={"message": "degree added successfully"},
        status_code=201
    )

@router.get("/{doctor_id}")
async def get_doctor_education(doctor_id: ObjectId) -> list[Degree]:
    doctor = await validate_doctor(doctor_id)
    education = [edu.update({"_id": str(edu["_id"])}) or edu for edu in doctor["education"]]
    return JSONResponse(
        content= {
            "message": "successfull request",
            "response": education
        },
        status_code=201
    )

@router.get("/{doctor_id}/{degree_id}")
async def get_one_degree(doctor_id: ObjectId, degree_id: ObjectId) -> Degree:
    doctor = await validate_doctor(doctor_id)
    education = doctor["education"]
    degree = next((edu for edu in education if edu["_id"] == _ObjectId(degree_id)), None)
    if not degree:
        raise HTTPException(status_code=404, detail="degree not found")
    degree["_id"] = str(degree["_id"])
    return JSONResponse(
        content= {
            "message": "successfull request",
            "response": degree
        },
        status_code=201
    )

@router.put("/{doctor_id}/{degree_id}")
async def update_doctor_degree(doctor_id: ObjectId, degree_id: ObjectId, new_degree: Degree):
    doctor = validate_doctor(doctor_id)
    await validate_education(doctor["education"], new_degree)
    to_json = new_degree.model_dump()
    to_json["_id"] = _ObjectId(degree_id)
    db["users"].update_one({"education._id": _ObjectId(degree_id)}, {"$set": {"education.$": to_json}})
    return JSONResponse(
        content= {
            "message": "degree successfully updated",
        },
        status_code=201
    )

@router.delete("/{doctor_id}/{degree_id}")
async def delete_doctor_degree(doctor_id: ObjectId, degree_id: ObjectId):
    await validate_doctor(doctor_id)
    db["users"].delete_one({"education._id": _ObjectId(degree_id)})
    return JSONResponse(
        content= {
            "message": "degree successfully deleted"
        },
        status_code=201
    )