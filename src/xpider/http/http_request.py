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
    ):
        self.url = url
        self.callback = callback
        self.headers = headers
        self.cookies = cookies
        self.method = method
        self.timeout = timeout
        self.proxy = proxy
    
    
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
            response = Response(raw_response)
            return response



class Response:
    def _init__(self, raw_response):
        pass
