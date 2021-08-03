from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator


class CoreModel(BaseModel):
    """
    Any common logic to be shared by all models goes here
    """
    pass


class DateTimeModelMixin(BaseModel):
    """
    new common model that will help us manage timestamps across our application
    """
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


    """
    feature - the validator decorator - to set a default datetime for both the created_at and updated_at fields. 
    https://pydantic-docs.helpmanual.io/usage/validators/
    """
    @validator("created_at", "updated_at", pre=True)
    def default_datetime(cls, value: datetime) -> datetime:
        return value or datetime.datetime.now()


class IDModelMixin(BaseModel):
    """
    class will be used for all resources coming out of the database.
    By not providing a default value for the id attribute,
    we're telling Pydantic that this field is required for all new instances. Since we used the int type declaration,
    the Pydantic docs tell us that "Strings, bytes or floats will be coerced (zmuszany) to ints if possible;
     otherwise an exception will be raised."
    """
    id: int
