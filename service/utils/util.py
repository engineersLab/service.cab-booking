"""
Some reusable methods
"""

from flask import request, jsonify, current_app
from sqlalchemy import and_, or_
import string
import random
from functools import wraps
import jwt

from service.models import Developer, Cab
from .enum import DEV_TYPE, CAB_TYPE, RESERVED_FOR

app = current_app


def serialize_developer(data):
    """
    Method to convert database object into python dict
    """
    result_data = {
        "developer_id": data.developer_id,
        "name": data.name,
        "email": data.email,
        "type_id": data.type_id,
    }

    return result_data


def generate_cab_num():
    """
    Method to generate a cab number
    """

    chars = string.ascii_uppercase
    numbers = string.digits

    cab_num = (
        "TN"
        + ("".join(random.choice(numbers) for _ in range(2)))
        + ("".join(random.choice(chars) for _ in range(2)))
        + ("".join(random.choice(numbers) for _ in range(4)))
    )
    return cab_num


def book_new_cab(type_id):
    """
    Method to book a new cab
    """

    new_cab = Cab(reg_no=generate_cab_num(), type_id=type_id)
    app.db.session.add(new_cab)
    app.db.session.flush()

    return new_cab


def get_cab(developer):
    """
    Method to query and find the cab for the developer
    """

    developer_type = DEV_TYPE[developer.type_id]
    if developer_type == "frontend":
        cab = Cab.query.filter(
            and_(
                or_(
                    Cab.reserved_for == RESERVED_FOR["any"],
                    Cab.reserved_for == RESERVED_FOR["frontend"],
                ),
                Cab.is_vacant == 1,
            )
        ).first()

        if cab is None:
            cab = book_new_cab(developer.type_id)
            cab.type_id = CAB_TYPE["f"]
            cab.reserved_for = RESERVED_FOR["any"]
            return cab

        if cab.available_seats == 2:
            if cab.type_id == CAB_TYPE["fb"]:
                cab.reserved_for = RESERVED_FOR["backend"]
            elif cab.type_id == CAB_TYPE["b"] or cab.type_id == CAB_TYPE["f"]:
                cab.reserved_for = RESERVED_FOR["frontend"]

        if cab.available_seats > 1:
            if cab.type_id == CAB_TYPE["b"]:
                cab.type_id = CAB_TYPE["fb"]

        if cab.available_seats == 1:
            cab.is_vacant = 0
            cab.reserved_for = None

        cab.available_seats -= 1

        return cab

    elif developer_type == "backend":
        cab = Cab.query.filter(
            and_(
                or_(
                    Cab.reserved_for == RESERVED_FOR["any"],
                    Cab.reserved_for == RESERVED_FOR["backend"],
                ),
                Cab.is_vacant == 1,
            )
        ).first()

        if cab is None:
            cab = book_new_cab(developer.type_id)
            cab.type_id = CAB_TYPE["b"]
            cab.reserved_for = RESERVED_FOR["any"]
            return cab

        if cab.available_seats == 2:
            if cab.type_id == CAB_TYPE["fb"]:
                cab.reserved_for = RESERVED_FOR["frontend"]
            elif cab.type_id == CAB_TYPE["f"] or cab.type_id == CAB_TYPE["b"]:
                cab.reserved_for = RESERVED_FOR["backend"]

        if cab.available_seats > 1:
            if cab.type_id == CAB_TYPE["f"]:
                cab.type_id = CAB_TYPE["fb"]

        if cab.available_seats == 1:
            cab.is_vacant = 0
            cab.reserved_for = None

        cab.available_seats -= 1

        return cab


def jwt_required(f):
    """
    Method to validate jwt
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"][7:]
        if not token:
            return jsonify({"message": "Token is missing"}), 401
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            developer = Developer.query.get(data["user"]["developer_id"])

            if developer is None:
                raise Exception("Unauthorized access")

        except Exception as e:
            return jsonify({"message": f"Token is invalid: {e}"}), 401

        return f(*args, **kwargs)

    return decorated
