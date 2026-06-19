import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_login_access_token():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        login_data = {
            "username": "U54",
            "password": "1"
        }
        response = await ac.post("/backend/auth/token", data=login_data)
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_get_statuses():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        login_data = {
            "username": "U54",
            "password": "1"
        }
        
        response = await ac.post("/backend/auth/token", data=login_data)
        assert response.status_code == 200
        
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        response = await ac.get("/backend/synch/statuses", headers=headers)
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_list_employees():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        login_data = {
            "username": "U54",
            "password": "1"
        }
        
        response = await ac.post("/backend/auth/token", data=login_data)
        assert response.status_code == 200
        
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        response = await ac.get("/backend/user/employees", headers=headers)
        assert response.status_code == 200
        assert len(response.json()) > 0