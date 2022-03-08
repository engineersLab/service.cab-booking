"""
Models to support cab booking
"""

from .db import db
from sqlalchemy import Column, Integer, String, ForeignKey
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


class DeveloperType(db.Model):
    __tablename__ = "developer_type"

    type_id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(40), nullable=False)


class Developer(db.Model):
    __tablename__ = "developer"

    developer_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(40), nullable=False)
    email = Column(String(40), unique=True, nullable=False)
    password = Column(String(80), nullable=False)
    type_id = Column(Integer, ForeignKey("developer_type.type_id"), nullable=False)
    date_created = Column(
        mysql.DATETIME,
        server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        nullable=False,
    )


class CabType(db.Model):
    __tablename__ = "cab_type"

    type_id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(40), nullable=False)


class Cab(db.Model):
    __tablename__ = "cab"

    cab_id = Column(Integer, primary_key=True, autoincrement=True)
    reg_no = Column(String(40), nullable=False)
    is_vacant = Column(Integer, server_default="1", nullable=False)
    available_seats = Column(Integer, server_default="4", nullable=False)
    reserved_for = Column(String(10))
    type_id = Column(Integer, ForeignKey("cab_type.type_id"), nullable=False)
    date_created = Column(
        mysql.DATETIME,
        server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        nullable=False,
    )


class Booking(db.Model):
    __tablename__ = "booking"

    booking_id = Column(Integer, primary_key=True, autoincrement=True)
    cab_id = Column(Integer, ForeignKey("cab.cab_id"), nullable=False)
    developer_id = Column(Integer, ForeignKey("developer.developer_id"), nullable=False)
    date_created = Column(
        mysql.DATETIME,
        server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        nullable=False,
    )


class Admin(db.Model):
    __tablename__ = "admin"

    admin_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(40), nullable=False)
    email = Column(String(40), unique=True, nullable=False)
    password = Column(String(80), nullable=False)
