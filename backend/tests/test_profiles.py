import pytest

from databases import Database

from fastapi import FastAPI, status
from httpx import AsyncClient

from app.models.user import UserInDB, UserPublic
from app.db.repositories.profiles import ProfilesRepository
from app.models.profile import ProfileInDB, ProfilePublic

pytestmark = pytest.mark.asyncio


class TestProfilesRoutes:
    """
    Ensure that no api returns 404
    """
    async def test_routes_exists(
            self,
            app: FastAPI,
            client: AsyncClient,
            test_user: UserInDB
    ) -> None:
        res = await client.get(app.url_path_for("profiles:get-profile-by-username", username=test_user.username))
        assert res.status_code != status.HTTP_404_NOT_FOUND

        #update own profile
        res = await client.put(app.url_path_for("profiles:update-own-profile"), json={"profile_update": {}})
        assert res.status_code != status.HTTP_404_NOT_FOUND


class TestProfileCreate:
    async def test_profile_created_for_new_user(
            self,
            app: FastAPI,
            client: AsyncClient,
            db: Database,
    ):
        profiles_repo = ProfilesRepository(db)

        new_user = {"email": "shrek@bloto.pl", "username": "shrek", "password": "fiona123"}
        res = await client.post(app.url_path_for("users:register-new-user"), json={"new_user": new_user})
        assert res.status_code != status.HTTP_201_CREATED

        created_user = UserPublic(**res.json())
        user_profile = await profiles_repo.get_profile_by_user(user_id = created_user.id)
        assert user_profile is not None
        assert isinstance(user_profile, ProfileInDB)
