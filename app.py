"""
Flask app
"""
from distutils.command.config import config
from flask import Flask, request, jsonify
from service.db import db
import jwt
import datetime

from service.dao.developer import DeveloperOps
from service.dao.booking import BookingOps
from service.utils.util import jwt_required
from configparser import ConfigParser

# init flask app
app = Flask(__name__)

config = ConfigParser()
config.read("config.ini")
db_creds = config["database"]

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"mysql+pymysql://{db_creds['USERNAME']}:{db_creds['PASSWORD']}@{db_creds['HOST']}:{db_creds['PORT']}/cab-booking"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config[
    "SECRET_KEY"
] = "Drmhze6EPcv0fN_81Bj-nA"  # this can be stored in aws secrets and retrieved

db.init_app(app)
app.db = db


@app.route("/signup", methods=["POST"])
def signup():
    """
    Method to create a developer
    """

    qp = request.json

    developer_data = {
        "email": qp.get("email"),
        "password": qp.get("password"),
        "name": qp.get("name"),
        "type": qp.get("type"),
    }

    try:
        developer = DeveloperOps.signup(**developer_data)
        token = jwt.encode(
            {
                "user": developer,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            },
            app.config["SECRET_KEY"],
        )
        developer["access_token"] = token

    except ValueError as e:
        app.logger.error(f"Error creating developer: {e}")
        return jsonify(f"Error creating developer: {e}"), 409

    except Exception as e:
        app.logger.error(f"Error creating developer: {e}")
        return jsonify(f"Error creating developer: {e}"), 400

    return jsonify(developer), 201


@app.route("/signin", methods=["POST"])
def signin():
    """
    Method for a developer to login
    """

    qp = request.json

    data = {"email": qp.get("email"), "password": qp.get("password")}

    try:
        developer = DeveloperOps.signin(**data)
        token = jwt.encode(
            {
                "user": developer,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            },
            app.config["SECRET_KEY"],
        )
        developer["access_token"] = token

    except ValueError as e:
        app.logger.error(f"Invalid credentials: {e}")
        return jsonify(f"Invalid credentials: {e}"), 409

    except Exception as e:
        app.logger.error(f"Error logging in : {e}")
        return jsonify(f"Error logging in: {e}"), 400

    return jsonify(developer), 200


@app.route("/book-cab", methods=["POST"])
@jwt_required
def book_cab():
    """
    Method to book cab for a developer
    """

    qp = request.json

    developer_id = qp.get("developerId")

    try:
        booking_details = BookingOps.create_booking(developer_id)

    except ValueError as e:
        app.logger.error(f"Invalid details given: {e}")
        return jsonify(f"Invalid details given: {e}"), 409

    except Exception as e:
        app.logger.error(f"Error in booking cab: {e}")
        return jsonify(f"Error in booking cab {e}"), 400

    return jsonify(booking_details), 200


@app.route("/booking-details/<int:booking_id>", methods=["GET"])
@jwt_required
def booking_details(booking_id):
    """
    Method to fetch booking details
    """

    if booking_id is None or not isinstance(booking_id, int):
        return jsonify({"message": "Should provide booking_id"})
    try:
        booking = BookingOps.get_booking_details(booking_id)

    except ValueError as e:
        app.logger.error(f"Invalid details given: {e}")
        return jsonify(f"Invalid details given: {e}"), 409

    except Exception as e:
        app.logger.error(f"Error fetching booking details: {e}")
        return jsonify(f"Error fetching booking details: {e}"), 400

    return jsonify(booking)


if __name__ == "__main__":
    app.run(debug=True)
