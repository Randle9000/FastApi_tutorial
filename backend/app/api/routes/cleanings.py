from typing import List
from fastapi import APIRouter

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
