from typing import Optional # We use the Optional type declaration to specify that any attribute not passed in
# when creating the model instance will be set to None
from enum import Enum

from app.models.core import CoreModel, IDModelMixin


"""
Why do we create the five different models: Base, Create, Update, InDB, Public:
Answer:
    Base - all shared attributes of a resource
    Create - attributes required to create a new resource - used at POST requests
    Update - attributes that can be updated - used at PUT requests
    InDB - attributes present on any resource coming out of the database
    Public - attributes present on public facing resources being returned from GET, POST, and PUT requests
And that pattern might be used in different places for almost every resource

And the models should corresponds to the tables created in DB 
(Compare to the code in migration/versions
"""



class CleaningType(str, Enum):
    dust_up = "dust_up"
    spot_clean = "spot_clean"
    full_clean = "full_clean"


class CleaningBase(CoreModel):
    """
    All common characteristics of our cleaning resource
    """
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    cleaning_type: Optional[CleaningType] = "spot_clean" # here the default value is 'spot_clean'


# intheriths from CleaningBase and CleaningBase from CoreBase and CoreBase from BaseModel of pedantic
class CleaningCreate(CleaningBase):
    """
    The inheritance expand the values of that model/class,
    we also have them from CleaningBase, and they corresponds to he
    files in migrations/versions there we have following columns:
        id:             sa.Column("id", sa.Integer, primary_key=True),
        name:           sa.Column("name", sa.Text, nullable=False, index=True),
        description:    sa.Column("description", sa.Text, nullable=True),
        cleaning_type:  sa.Column("cleaning_type", sa.Text, nullable=False, server_default="spot_clean"),
        price:          sa.Column("price", sa.Numeric(10, 2), nullable=False),

    """
    # each value passsed as name will be for coerced to be str (in that case)
    name: str
    price: float


class CleaningUpdate(CleaningBase):
    cleaning_type: Optional[CleaningType]


class CleaningInDB(IDModelMixin, CleaningBase):
    name: str
    price: float
    cleaning_type: CleaningType


class CleaningPublic(IDModelMixin, CleaningBase):
    pass
