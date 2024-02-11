from pydantic import BaseModel, Field, EmailStr, ConfigDict
from .validators import check_object_id
from pydantic.functional_validators import AfterValidator
from datetime import datetime, date
from typing import Annotated


# CUSTOM TYPES
PhoneNumber = Annotated[str, Field(pattern=r'^\d{10}$')]
ObjectId = Annotated[str, AfterValidator(check_object_id)]
    
# MODELS
class UserBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    username: str = Field(min_length=5, max_length=255)
    lastname: str = Field(min_length=5, max_length=255)
    email: EmailStr = Field(min_length=5, max_length=255)
    password: str = Field(min_length=5, max_length=255)
    rol: str = Field(default="patient")

class UserInDb(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    email: EmailStr = Field(min_length=5, max_length=255)
    password: str = Field(min_length=5, max_length=255)

class Developer(UserBase):
    rol: str  = "developer"

class Appointment(BaseModel):
    user_id: ObjectId
    doctor_id: ObjectId
    date: datetime
    commentary: str | None = None

class Clinic(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    name: str = Field(min_length=5, max_length=255)
    address: str = Field(min_length=5, max_length=1000)
    city: str  = Field(max_length=100)

class Degree(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    university: str
    speciality: str
    from_date: int | str
    to_date: int  | str

class Experience(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    clinic: str
    work: str
    from_date: int | str
    to_date: int | str

class Doctor(UserBase):
    speciality: str = Field(default=None, min_length=5,  max_length=100)
    appointments: list[str] = Field(default=[])
    contact_number: PhoneNumber
    license_number: str = Field(max_length=255)
    clinic: Clinic
    rol: str =  "doctor"
    education: list[Degree] = Field(default=[])
    experience: list[Experience] = Field(default=[])
    about: str = Field(default="")

class UpdateDoctor(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    username: str = Field(default=None, min_length=5, max_length=255)
    lastname: str = Field(default=None, min_length=5, max_length=255)
    email: EmailStr = Field(default=None)
    speciality: str = Field(default=None, min_length=5, max_length=255)
    contact_number: PhoneNumber = Field(default=None)
    license_number: str = Field(default=None, max_length=255)
    about: str = Field(default=None, min_length=5)


class Patient(UserBase):
    appointments: list[str] = Field(default=[])
    contact_number: PhoneNumber
    address: str | None = None
    date_of_birth: date | None = None
    emergency_contact: PhoneNumber

class Token(BaseModel):
    access_token: str
    token_type: str