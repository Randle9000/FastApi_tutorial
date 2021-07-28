import string
from typing import Optional

from pydantic import EmailStr, constr, validator

from app.models.core import DateTimeModelMixin, IDModelMixin, CoreModel
from app.models.token import AccessToken
from app.models.profile import ProfilePublic


def validate_username(username: str) -> str:
    allowed = string.ascii_letters + string.digits + '-' + '_'
    assert all(char in allowed for char in username), "invalid character in user name."
    assert len(username) >= 3, "Username must be 3 characters or more."
    return username


class UserBase(CoreModel):
    """
    Leaving off password and salt from base model
    """
    email: Optional[EmailStr]
    username: Optional[str]
    email_verified: bool = False
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(CoreModel):
    """
    Email, username, and password are required for registering a new user
    The constr type is one of pydantic's constrained types and it stands for constrained string. Constrained strings offer the ability to set minimum and maximum lengths on any string value, along with other validations
    """
    email: EmailStr
    password: constr(min_length=7, max_length=100)
    username: constr(min_length=3, regex="^[a-zA-Z0-9_-]+$")


    #second approach
    # username: str
    #
    # @validator("username", pre=True)
    # def username_is_valid(cls, username: str) -> str:
    #     return validate_username(username)


class UserUpdate(CoreModel):
    """
    Users are allowed to update their email and/or username
    """
    email: Optional[EmailStr]
    username: Optional[constr(min_length=3, regex="^[a-zA-Z0-9_-]+$")]

    # second approach
    # username: str
    #
    # @validator("username", pre=True)
    # def username_is_valid(cls, username: str) -> str:
    #     return validate_username(username)


class UserPasswordUpdate(CoreModel):
    """
    Users are allowed to change their password
    """
    password: constr(min_length=7, max_length=100)
    salt: str


class UserInDB(IDModelMixin, DateTimeModelMixin, UserBase):
    """
    ADd in id, created_at, updated_at, and user's passwrod and salt
    """
    password: constr(min_length=7, max_length=100)
    salt: str


class UserPublic(IDModelMixin, DateTimeModelMixin, UserBase):
    access_token: Optional[AccessToken] # we should update our UserPublic model to also store an optional access token
    profile: Optional[ProfilePublic]