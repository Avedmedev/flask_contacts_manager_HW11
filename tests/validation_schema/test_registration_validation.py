import pytest
from marshmallow import ValidationError

from src.libs.validation_schema import RegistrationSchema


@pytest.mark.parametrize(
    "nick,valid",
    [
        ("Alex", True),
        ("Al", False),
        ("Alexxxxxxxxxxxxxxxx", False),
        ("", False),
    ]
)
def test_validate_registration_nick(nick, valid):
    schema = RegistrationSchema()
    data = {
        "nick": nick,  # fields.Str(validate=validate.Length(min=3, max=10), required=True)
        "email": "alex@i.ua",  # fields.Email(required=True)
        "password": '1234'  # fields.Str(validate=validate.Length(min=4), required=True)
    }

    try:
        user = schema.load(data)
        assert valid

        assert user is not None
        assert user["nick"] == data["nick"]
        assert user["email"] == data["email"]
        assert user["password"] == data["password"]
    except ValidationError:
        assert not valid


@pytest.mark.parametrize(
    "email,valid",
    [
        ("alex@i.ua", True),
        ("Al", False),
        ("Alex@", False),
        ("Alex@ua", False),
        ("", False),
    ]
)
def test_validate_registration_email(email, valid):
    schema = RegistrationSchema()
    data = {
        "nick": "Alex",  # fields.Str(validate=validate.Length(min=3, max=10), required=True)
        "email": email,  # fields.Email(required=True)
        "password": '1234'  # fields.Str(validate=validate.Length(min=4), required=True)
    }

    try:
        user = schema.load(data)
        assert valid

        assert user is not None
        assert user["nick"] == data["nick"]
        assert user["email"] == data["email"]
        assert user["password"] == data["password"]
    except ValidationError:
        assert not valid


@pytest.mark.parametrize(
    "password,valid",
    [
        ("12345", True),
        ("123", False),
        ("", False),
    ]
)
def test_validate_registration_password(password, valid):
    schema = RegistrationSchema()
    data = {
        "nick": "Alex",  # fields.Str(validate=validate.Length(min=3, max=10), required=True)
        "email": "alex@i.ua",  # fields.Email(required=True)
        "password": password  # fields.Str(validate=validate.Length(min=4), required=True)
    }

    try:
        user = schema.load(data)
        assert valid

        assert user is not None
        assert user["nick"] == data["nick"]
        assert user["email"] == data["email"]
        assert user["password"] == data["password"]
    except ValidationError:
        assert not valid


def test_validate_registration_missing_fields():
    schema = RegistrationSchema()
    data = {
        "nick": "Alex",  # fields.Str(validate=validate.Length(min=3, max=10), required=True)
        "email": "alex@i.ua",  # fields.Email(required=True)
    }

    try:
        schema.load(data)
        assert False

    except ValidationError:
        assert True

    data = {
        "nick": "Alex",  # fields.Str(validate=validate.Length(min=3, max=10), required=True)
        "password": "alex@i.ua",  # fields.Email(required=True)
    }

    with pytest.raises(ValidationError):
        schema.load(data)

    data = {
        "password": "Alex1",
        "email": "alex@i.ua",  # fields.Email(required=True)
    }

    with pytest.raises(ValidationError):
        schema.load(data)
