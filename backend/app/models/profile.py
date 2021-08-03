from typing import Optional

from app.models.core import CoreModel, DateTimeModelMixin, IDModelMixin
from pydantic import EmailStr, HttpUrl


class ProfileBase(CoreModel):
    full_name: Optional[str]
    phone_number: Optional[str]
    bio: Optional[str]
    image: Optional[HttpUrl]


class ProfileCreate(ProfileBase):
    """
    there is only one additional field which we need ot create profile, it's users id
    """

    user_id: int


class ProfileUpdate(ProfileBase):
    """
    Allow users to update fields but not the user_id
    """

    pass


class ProfileInDB(ProfileBase, DateTimeModelMixin, IDModelMixin):
    user_id: int
    username: Optional[str]
    email: Optional[EmailStr]


class ProfilePublic(ProfileInDB):
    pass
