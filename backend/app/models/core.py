from pydantic import BaseModel


class CoreModel(BaseModel):
    """
    Any common logic to be shared by all models goes here
    """
    pass


class IDModelMixin(BaseModel):
    """
    class will be used for all resources coming out of the database.
    By not providing a default value for the id attribute,
    we're telling Pydantic that this field is required for all new instances. Since we used the int type declaration,
    the Pydantic docs tell us that "Strings, bytes or floats will be coerced (zmuszany) to ints if possible;
     otherwise an exception will be raised."
    """
    id: int
