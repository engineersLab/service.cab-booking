"""
Booking related operations
"""

from flask import current_app
from service.models import Developer, Booking, Cab
from service.utils.util import serialize_developer, get_cab

app = current_app


class BookingOps:
    """
    class to manage booking related operations
    """

    def __init__(self):
        pass

    @classmethod
    def create_booking(cls, developer_id):
        """
        Method to create booking cab for a developer

        param: developer_id

        returns: object {
            "booking_id" - id for the booking,
            "cab_id - id of the cab that is booked for the the developer
        }
        """

        developer = Developer.query.get(developer_id)

        if not developer:
            raise ValueError(f"Developer with id {developer_id} does not exist.")

        if_already_booked = (
            Booking.query.filter_by(developer_id=developer_id).first() is not None
        )

        if if_already_booked:
            raise ValueError(
                f"Cab is already booked for developer with id {developer_id}"
            )

        try:
            cab = get_cab(developer)
            booking = Booking(cab_id=cab.cab_id, developer_id=developer_id)

            app.db.session.add(cab)
            app.db.session.add(booking)
            app.db.session.commit()
        except Exception as e:
            app.db.session.rollback()
            raise e

        return {"booking_id": booking.booking_id, "cab_id": booking.cab_id}

    @classmethod
    def get_booking_details(cls, booking_id):
        """
        Method to get booking details

        param: booking_id
        """

        try:
            booking = Booking.query.get(booking_id)

            if booking is None:
                raise ValueError(f"Invalid booking id: {booking_id}")
            developer = Developer.query.get(booking.developer_id)
            cab = Cab.query.get(booking.cab_id)
        except Exception as e:
            raise e

        return {
            "booking_id": booking.booking_id,
            "developer_details": serialize_developer(developer),
            "cab_details": {
                "cab_id": cab.cab_id,
                "registration_no": cab.reg_no,
            },
        }
