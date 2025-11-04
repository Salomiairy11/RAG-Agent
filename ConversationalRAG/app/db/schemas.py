from pydantic import BaseModel, EmailStr
import datetime

class InterviewCreate(BaseModel):
    name: str
    email: EmailStr
    date: datetime.date
    time: datetime.time
