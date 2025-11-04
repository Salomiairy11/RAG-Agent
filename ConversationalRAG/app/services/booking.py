import datetime
from ..db.schemas import InterviewCreate
from ..db.models import SessionLocal
from ..db.crud import save_booking_to_db

def handle_booking(name: str, email: str, date: str, time: str):
    """Create and save booking entry in DB."""
    try:
        booking_data = InterviewCreate(
            name=name,
            email=email,
            date=datetime.date.fromisoformat(date),
            time=datetime.time.fromisoformat(time)
        )

        db = SessionLocal()
        booking = save_booking_to_db(db, booking_data)
        db.close()

        return f"Interview booked successfully for {booking.name} on {booking.date} at {booking.time}."
    except Exception as e:
        return f"Invalid booking input: {e}"
