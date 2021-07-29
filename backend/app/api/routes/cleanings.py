from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Path
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND

from app.models.user import UserInDB
from app.models.cleaning import CleaningCreate, CleaningPublic, CleaningUpdate
from app.db.repositories.cleanings import CleaningsRepository
from app.api.dependencies.database import get_repository
from app.api.dependencies.auth import get_current_active_user

router = APIRouter()


"""
The @router.get("/") tells FastAPI that the function right below is in charge of handling requests that go to:

    the path /
    using a get operation

"""
# @router.get("/")
# async def get_all_cleanings() -> List[dict]: # -> List[dicts] shows what type is return as in java :P
#     cleanings = [
#         {"id": 1, "name": "My house", "cleaning_type": "full_clean", "price_per_hour": 29.99},
#         {"id": 2, "name": "Someone else's house", "cleaning_type": "spot clea", "price_per_hour": 19.99}
#
#     ]
#     return cleanings


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


# @router.get("/", response_model=List[CleaningPublic], name="cleanings:get-all-cleanings")
# async def get_all_cleanings() -> List[CleaningPublic]:
#     return [{ "id": 1, "name": "fake cleaning", "price": 0}]

@router.get("/", response_model=List[CleaningPublic], name="cleanings:get-all-cleanings")
async def get_all_cleanings(
        cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository)),
) -> List[CleaningPublic]:
    return await cleanings_repo.get_all_cleanings()


@router.post("/", response_model=CleaningPublic, name="cleanings:create-cleaning", status_code=HTTP_201_CREATED)
async def create_new_cleaning(
    new_cleaning: CleaningCreate = Body(..., embed=True),
    current_user: UserInDB = Depends(get_current_active_user),
    cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository)),
) -> CleaningPublic:
    created_cleaning = await cleanings_repo.create_cleaning(new_cleaning=new_cleaning, requesting_user=current_user)
    return created_cleaning


@router.get("/{id}", response_model=CleaningPublic, name="cleanings:get-cleaning-by-id", status_code=HTTP_200_OK)
async def get_cleanings_by_id(
        id: int = Path(..., ge=1),
        current_user: UserInDB = Depends(get_current_active_user),
        cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository)),
) -> CleaningPublic:
    cleaning = await cleanings_repo.get_cleaning_by_id(id=id, requesting_user=current_user)

    if not cleaning:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No cleaning found with that id.")

    return cleaning


@router.get("/", response_model=List[CleaningPublic], name="cleanings:list-all-user-cleanings")
async def list_all_user_cleanings(
        current_user: UserInDB = Depends(get_current_active_user),
        cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository))
) -> List[CleaningPublic]:
    return await cleanings_repo.list_all_user_cleanings(requesting_user=current_user)


@router.put("/{id}/", response_model=CleaningPublic, name="cleanings:update-cleaning-by-id")
async def update_cleanings_by_id(
        id: int = Path(..., ge=1, title="The id of the cleaning to update"), # ge means the cleaning id must be integer greater or equal to 1
        cleaning_update: CleaningUpdate = Body(..., embed=True),
        cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository)),
) -> CleaningPublic:
    updated_cleaning = await cleanings_repo.update_cleaning(id=id, cleaning_update=cleaning_update)

    if not updated_cleaning:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No cleaning found with that id")

    return updated_cleaning


@router.delete("/{id}/", response_model=int, name="cleanings:delete-cleaning-by-id")
async def delete_cleaning_by_id(
        id: int = Path(..., ge=1, title="The id of the cleanign to update"),
        cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository)),
) -> int:
    deleted_id = await cleanings_repo.delete_cleaning_by_id(id=id)
    if not deleted_id:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No cleaning found with that id")

    return deleted_id



