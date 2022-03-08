"""
Developer related operations
"""

from flask import current_app
from flask_bcrypt import Bcrypt
from service.models import Developer, DeveloperType
from service.utils.util import serialize_developer

app = current_app
bcrypt = Bcrypt()


class DeveloperOps:
    """
    class to manage developer related operations
    """

    def __init__(self):
        pass

    @classmethod
    def signup(cls, **kwargs):
        """
        Method to create a new developer

        returns: created developer object
        """

        name = kwargs.get("name")
        email = kwargs.get("email")
        password = kwargs.get("password")
        type = kwargs.get("type")

        developer_exists = Developer.query.filter_by(email=email).first() is not None

        if developer_exists:
            raise ValueError(f"Developer with email {email} already exists.")

        developer_type = DeveloperType.query.filter_by(type=type).first()

        if developer_type is None:
            raise ValueError(f"No record found for developer type {type}")

        encrypted_password = bcrypt.generate_password_hash(password)
        try:
            developer = Developer(
                name=name,
                email=email,
                password=encrypted_password,
                type_id=developer_type.type_id,
            )

            app.db.session.add(developer)
            app.db.session.commit()

        except Exception as e:
            app.db.session.rollback()
            raise e

        return serialize_developer(developer)

    @classmethod
    def signin(cls, **kwargs):
        """
        Method for a developer to login

        returns: created developer object
        """

        email = kwargs.get("email")
        password = kwargs.get("password")

        developer = Developer.query.filter_by(email=email).first()

        if not developer:
            raise ValueError(f"Developer with email {email} does not exist.")

        try:
            if not (bcrypt.check_password_hash(developer.password, password)):
                raise Exception("Error: Password does not match")

        except Exception as e:
            app.db.session.rollback()
            raise e

        return serialize_developer(developer)
