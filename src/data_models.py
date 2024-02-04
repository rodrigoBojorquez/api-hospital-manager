from pydantic import BaseModel, Field, EmailStr, constr, ConfigDict
from datetime import datetime, date
from typing import Annotated


# CUSTOM TYPES
PhoneNumber = Annotated[str, Field(constr(strip_whitespace=True), pattern=r'^\d{10}$')]
    
# MODELS
class UserBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    username: str = Field(min_length=5, max_length=255)
    lastname: str = Field(min_length=5, max_length=255)
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=5, max_length=255)
    rol: str = Field(default="patient")

class UserInDb(BaseModel):
    email: EmailStr
    password: str

class Appointment(BaseModel):
    user_id: int
    doctor_id: int
    date: datetime
    commentary: str | None = None

class Clinic(BaseModel):
    name: str = Field(min_length=5, max_length=255)
    address: str = Field(min_length=5, max_length=1000)
    city: str  = Field(max_length=100)

class Degree(BaseModel):
    university: str
    speciality: str
    from_date: int | str
    to_date: int  | str

class Experience(BaseModel):
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
    education: list[Degree] = Field(default=[])
    experience: list[Experience] = Field(default=[])

class Patient(UserBase):
    appointments: list[str] = Field(default=[])
    contact_number: PhoneNumber
    address: str | None = None
    date_of_birth: date | None = None
    emergency_contact: int | None = None