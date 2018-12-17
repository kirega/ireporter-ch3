"""This file defines all the validation schema for marshmallow
that are reused in the views.py
"""
from marshmallow import ValidationError, Schema, fields, ValidationError


def validate_string(s):
    """Utility function for string validations"""

    if not s.strip():
        raise ValidationError('Empty string invalid')


def password_strength(s):
    """
    Utility function for password strength
    """
    if len(s) < 8:
        raise ValidationError('Password must be more than 8 characters long')


class IncidentSchema(Schema):
    """Incident Schema for validation"""

    incidentId = fields.Int()
    createdOn = fields.DateTime()
    createdBy = fields.Int(required=True)
    incidentType = fields.Str(required=True, validate=validate_string)
    location = fields.Str(required=True, validate=validate_string)
    comment = fields.Str(required=True,validate=validate_string)
    status = fields.Str()
    images = fields.List(fields.Str())
    videos = fields.List(fields.Str())


class UserSchema(Schema):
    """User models validation schema"""

    userid = fields.Int()
    first_name = fields.Str(required=True, validate=validate_string)
    last_name = fields.Str(required=True, validate=validate_string)
    other_names = fields.Str(validate=validate_string)
    phonenumber = fields.Str(required=True, validate=validate_string)
    username = fields.Str(required=True, validate=validate_string)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=[
                          validate_string, password_strength])
    isAdmin = fields.Bool()
    registeredOn = fields.DateTime()


class IncidentEditSchema(Schema):
    """Incident schema for edit comment/location as well as delete"""
    userid = fields.Int(required=True)
    comment = fields.Str(required=True,validate=validate_string)
    location = fields.Str(required=True,validate=validate_string)
    status = fields.Str(required=True,validate=validate_string)
