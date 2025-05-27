import pytest
from httpx import AsyncClient
from fastapi import status
from main import app
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
@patch("redis.asyncio.Redis.incr")
@patch("redis.asyncio.Redis.ttl")
async def test_anon_rate_limit_ok(mock_ttl, mock_incr):
    mock_incr.return_value = 1
    mock_ttl.return_value = 60

    async with AsyncClient(app=app, base_url="http://test") as ac:
        for _ in range(2):
            res = await ac.get("/public-books")
            assert res.status_code == 200

@patch("redis.asyncio.Redis.incr")
@patch("redis.asyncio.Redis.ttl")
@pytest.mark.asyncio
async def test_anon_rate_limit_exceeded(mock_ttl, mock_incr):
    mock_incr.return_value = 3
    mock_ttl.return_value = 50

    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.get("/public-books")
        assert res.status_code == 429

@patch("redis.asyncio.Redis.incr")
@patch("redis.asyncio.Redis.ttl")
@pytest.mark.asyncio
async def test_auth_rate_limit_ok(mock_ttl, mock_incr):
    mock_incr.return_value = 1
    mock_ttl.return_value = 60

    async with AsyncClient(app=app, base_url="http://test") as ac:
        token_res = await ac.post("/token", data={"username": "admin", "password": "admin"})
        token = token_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        for _ in range(10):
            res = await ac.get("/books", headers=headers)
            assert res.status_code == 200

@patch("redis.asyncio.Redis.incr")
@patch("redis.asyncio.Redis.ttl")
@pytest.mark.asyncio
async def test_auth_rate_limit_exceeded(mock_ttl, mock_incr):
    mock_incr.return_value = 11
    mock_ttl.return_value = 45

    async with AsyncClient(app=app, base_url="http://test") as ac:
        token_res = await ac.post("/token", data={"username": "admin", "password": "admin"})
        token = token_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        res = await ac.get("/books", headers=headers)
        assert res.status_code == 429
