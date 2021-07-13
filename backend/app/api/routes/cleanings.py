from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND

from app.models.cleaning import CleaningCreate, CleaningPublic
from app.db.repositories.cleanings import CleaningsRepository
from app.api.dependencies.database import get_repository

router = APIRouter()


"""
The @router.get("/") tells FastAPI that the function right below is in charge of handling requests that go to:

    the path /
    using a get operation

"""
@router.get("/")
async def get_all_cleanings() -> List[dict]: # -> List[dicts] shows what type is return as in java :P
    cleanings = [
        {"id": 1, "name": "My house", "cleaning_type": "full_clean", "price_per_hour": 29.99},
        {"id": 2, "name": "Someone else's house", "cleaning_type": "spot clea", "price_per_hour": 19.99}

    ]
    return cleanings


"""
The first of two path parameters in our create_new_cleaning function, new_cleaning, 
is annotated with the CleaningCreate type. 
By default, FastAPI expects the body of a post request directly. 
If we want it to expect JSON with a key new_cleaning and inside of it the model contents,
 we use the special Body parameter embed in the parameter default.

By simply specifying the CleaningCreate Python type declaration for new_cleaning, FastAPI will:

    Read the body of the request as JSON.
    Convert the corresponding types.
    Validate the data.
    Respond with an error if validation fails, or provide the route with the model instance needed.

The second of the two path parameters - cleanings_repo - 
is our database interface, and the route's only dependency. 
We're setting its default to Depends(get_repository(CleaningsRepository)) 
so that we have access to it in our route and can create the new cleaning 
whenever the function is executed. 
FastAPI automatically validates and converts the created_cleaning 
to an instance of our CleaningPublic model, 
and sends the appropriate JSON as a response.

"""
@router.post("/", response_model=CleaningPublic, name="cleanings:create-cleaning", status_code=HTTP_201_CREATED)
async def create_new_cleaning(
    new_cleaning: CleaningCreate = Body(..., embed=True),
    cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository)),
) -> CleaningPublic:
    created_cleaning = await cleanings_repo.create_cleaning(new_cleaning=new_cleaning)
    return created_cleaning


@router.get("/{id}", response_model=CleaningPublic, name="cleanings:get-cleaning-by-id", status_code=HTTP_200_OK)
async def get_cleanings_by_id(
        id: int, cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository)),
) -> CleaningPublic:
    cleaning = await cleanings_repo.get_cleaning_by_id(id=id)

    if not cleaning:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No cleaning found with that id.")

    return cleaning
