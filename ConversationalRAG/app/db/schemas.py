from pydantic import BaseModel, EmailStr
import datetime

class InterviewCreate(BaseModel):
    """
    Schema for creating a new interview booking.
    Used for request validation and data transfer.
    """
    name: str
    email: EmailStr
    date: datetime.date
    time: datetime.time
