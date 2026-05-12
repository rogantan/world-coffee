import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import aiohttp
import json
from typing import Annotated, Optional
from fastapi import HTTPException

from functools import wraps
from core.config import settings
import base64
import requests


def handle_response_errors(retries, initial_delay):

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    url, status, data = await func(*args, **kwargs)

                    if status < 400:
                        return data
                    
                    if status == 429:
                        delay = initial_delay * (2 ** (attempt + 1))
                        await asyncio.sleep(delay)
                        continue
                    elif status in (412, 404):
                        return data
                    elif status == 409:
                        data = data["errors"][0]
                        errors = [url["uuidHref"] for url in data["dependencies"]]
                        raise HTTPException(status_code=409, detail=errors)
                    else:
                        raise Exception(f"HTTP error {status} for URL {url}")
                except asyncio.exceptions.TimeoutError:
                    delay = initial_delay * (2 ** (attempt + 1))
                    await asyncio.sleep(delay)
                    continue
                except Exception as e:
                    raise e
            
            raise Exception("Превышено максимальное количество попыток")
        return wrapper
    return decorator

class AsyncHttpClient:
    def __init__(self,
        base_url: str, 
        token: Optional[str] = None,
        login: Optional[str] = None,
        password: Optional[str] = None,
        headers: Optional[str] = None,):
        
        basic_token = (base64.b64encode(f"{login}:{password}".encode("utf-8")).decode("utf-8") 
            if login and password else None)
        authorization = None

        if basic_token:
            authorization = f"Basic {basic_token}"
        elif token:
            authorization = f"Bearer {token}"
        
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": authorization,
            **(headers or {}),
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()
    
    @handle_response_errors(retries=10, initial_delay=0.2)
    async def _request(self, method: str, path: str, cache_key=None, **kwargs):
        url = f"{self.base_url.rstrip("/")}/{path.lstrip("/")}"
        key = cache_key or f"{method}:{url}:{json.dumps(kwargs.get("params") or {})}"

        async with self.session.request(
            method, url, headers=self.headers, **kwargs
        ) as response:
            content_type = response.headers.get("Content-Type", "")
            if content_type.startswith("image/png"):
                data = await response.read()
            else:
                try:
                    data = await response.json()
                except Exception:
                    data = await response.text()
            return url, response.status, data
    
    async def get(self, path: str, params: Optional[dict] = None, cache_key=None):
        return await self._request("GET", path, params=params, cache_key=cache_key)
    
    async def post(self, path: str, data: Optional[dict] = None):
        return await self._request("POST", path, json=data)
    
    async def put(self, path: str, data: Optional[dict] = None):
        return await self._request("PUT", path, json=data)
    
    async def delete(self, path: str, params: Optional[dict] = None):
        return await self._request("DELETE", path, params=params)
    
@asynccontextmanager
async def get_session(login: str = None,
    password: str = None,
    token: str = None,) -> AsyncGenerator[AsyncHttpClient, None]:
    async with AsyncHttpClient(
        base_url=settings.MS_API_URL,
        login=login,
        password=password,
        token=token,
    ) as client:
        yield client