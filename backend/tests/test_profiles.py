import pytest

from databases import Database

from fastapi import FastAPI, status
from httpx import AsyncClient

from app.models.user import UserInDB

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
