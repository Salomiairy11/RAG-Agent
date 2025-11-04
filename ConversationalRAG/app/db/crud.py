import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from .models import Interview
from .schemas import InterviewCreate


logger = logging.getLogger(__name__)

def save_booking_to_db(db: Session, booking: InterviewCreate) -> Interview:
    """
    Save a new interview booking to the database.

    Args:
        db (Session): SQLAlchemy database session.
        booking (InterviewCreate): Booking data validated by Pydantic schema.

    Returns:
        Interview: The newly created Interview record.

    Raises:
        SQLAlchemyError: If the database operation fails.
    """
    try:
        new_booking = Interview(**booking.model_dump())
        db.add(new_booking)
        db.commit()
        db.refresh(new_booking)
        logger.info("New booking saved successfully: %s", new_booking.id)
        return new_booking
    except SQLAlchemyError as e:
        db.rollback()
        logger.error("Failed to save booking: %s", str(e), exc_info=True)
        raise
