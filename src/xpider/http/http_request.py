from typing import Callable, Optional
from uuid import uuid4 as uuid

from httpx import AsyncClient


class Request:
    def __init__(
        self,
        url: str,
        callback: Optional[Callable | str] = None,
        headers: Optional[dict] = None,
        cookies: Optional[dict] = None,
        method: str = "get",
        timeout: int = 20,
        proxy: Optional[dict] = None,
        meta:Optional[dict] = None
    ):
        self.url = url
        self.callback = callback if isinstance(callback, str) or None else callback.__name__ # type: ignore[union-attr]
        self.headers = headers
        self.cookies = cookies
        self.method = method
        self.timeout = timeout
        self.proxy = proxy
        self.meta = meta
    
    
    def add_request_id(self):
        self.id = str(uuid())
        self.retry = 0

    @staticmethod
    def from_json(request_dict:dict):
        # id = request_dict.get("id")
        pass

    async def send(self):
        async with AsyncClient() as client:
            raw_response = getattr(client, self.method)(
                self.url,
                headers=self.headers,
                cookies=self.cookies,
                proxy=self.proxy,
            )
            response = Response(raw_response, self)
            return response



class Response:
    def _init__(self, raw_response, request:Request):
        self.url = raw_response.url
        self.text = raw_response.text
        self.content =  raw_response.content
        self.headers = raw_response.headers
        self.cookies = raw_response.cookies
        self.status_code = raw_response.status_code
        self.request = request
        self.meta = request.meta
    
    def to_json(self):
        return {
            "url": self.url,
            "headers": self.headers,
            "cookies": self.cookies,
            "status_code": self.status_code,
            "request": self.request.to_json()
        }
