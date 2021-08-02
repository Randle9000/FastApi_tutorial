import logging
from typing import List

from fastapi import HTTPException
from starlette import status

from app.db.repositories.base import BaseRepository
from app.models.cleaning import CleaningCreate, CleaningUpdate, CleaningInDB, CleaningPublic
from app.models.user import UserInDB

CREATE_CLEANING_QUERY = """
    INSERT INTO cleanings (name, description, price, cleaning_type, owner)
    VALUES(:name, :description, :price, :cleaning_type, :owner)
    RETURNING id, name, description, price, cleaning_type, owner, created_at, updated_at; 
"""

GET_CLEANING_BY_ID = """
SELECT id, name, description, price, cleaning_type, owner, created_at, updated_at
FROM cleanings
WHERE id = :id;
"""

LIST_ALL_USER_CLEANINGS_QUERY = """
    SELECT id, name, description, price, cleaning_type, owner, created_at, updated_at
    FROM cleanings
    WHERE owner = :owner;
"""

GET_ALL_CLEANINGS = """
SELECT id, name, description, price, cleaning_type
FROM cleanings;
"""

UPDATE_CLEANING_BY_ID = """
    UPDATE cleanings
    SET name         = :name,
        description  = :description,
        price        = :price,
        cleaning_type = :cleaning_type
    WHERE id = :id AND owner = :owner
    RETURNING id, name, description, price, cleaning_type, owner, created_at, updated_at;
"""

DELETE_CLEANING_BY_ID_QUERY = """
    DELETE FROM cleanings  
    WHERE id = :id AND owner = :owner  
    RETURNING id;  
"""


class CleaningsRepository(BaseRepository):
    """
    All databases actions associated with the Cleaning resource
    """

    async def create_cleaning(self, *, new_cleaning: CleaningCreate, requesting_user: UserInDB) -> CleaningInDB:
        query_values = new_cleaning.dict()
        cleaning = await self.db.fetch_one(
            query=CREATE_CLEANING_QUERY, values={**query_values, "owner": requesting_user.id}
        )
        return CleaningInDB(**cleaning)

    async def get_cleaning_by_id(self, *, id: int, requesting_user: UserInDB) -> CleaningInDB:
        cleaning = await self.db.fetch_one(query=GET_CLEANING_BY_ID, values={"id": id})

        if not cleaning:
            return None

        return CleaningInDB(**cleaning)

    async def list_all_user_cleanings(self, *, requesting_user: UserInDB) -> List[CleaningInDB]:
        cleaning_records = await self.db.fetch_all(
            query=LIST_ALL_USER_CLEANINGS_QUERY, values={"owner": requesting_user.id}
        )

        return [CleaningInDB(**l) for l in cleaning_records]

    async def get_all_cleanings(self) -> List[CleaningInDB]:
        cleanings_records = await self.db.fetch_all(query=GET_ALL_CLEANINGS)
        return [CleaningInDB(**cleaning) for cleaning in cleanings_records]

    async def update_cleaning(
            self, *, id: int, cleaning_update: CleaningUpdate, requesting_user: UserInDB
    ) -> CleaningInDB:
        cleaning = await self.get_cleaning_by_id(id=id, requesting_user=requesting_user)

        if not cleaning:
            return None

        if cleaning.owner != requesting_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Users are only able to update cleanings that they created.",
            )

        cleaning_update_params = cleaning.copy(update=cleaning_update.dict(exclude_unset=True)) #By specifying exclude_unset=True, Pydantic will leave out any attributes that were not explicitly set when the model was created.
        if cleaning_update_params.cleaning_type is None:
             raise HTTPException(
                 status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid cleaning type. Cannot be None."
             )

        updated_cleaning = await self.db.fetch_one(
            query=UPDATE_CLEANING_BY_ID,
            values={
                **cleaning_update_params.dict(exclude={"created_at", "updated_at"}),
                "owner": requesting_user.id,
            },
        )
        return CleaningInDB(**updated_cleaning)

    async def delete_cleaning_by_id(self, id: int, requesting_user :UserInDB):
        cleaning = await self.get_cleaning_by_id(id=id, requesting_user=requesting_user)

        if not cleaning:
            return None

        if cleaning.owner != requesting_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Users are only able to delete cleanings that they created.",
            )

        deleted_id = await self.db.execute(
            query=DELETE_CLEANING_BY_ID_QUERY, values={"id": id, "owner": requesting_user.id})

        return deleted_id
