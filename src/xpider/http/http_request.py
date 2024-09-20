from typing import Callable, Optional, Any
from uuid import uuid4 as uuid

from httpx import AsyncClient


class Request:
    def __init__(
        self,
        url: str,
        callback: Optional[Callable | str] = None,
        headers: Optional[dict] = None,
        cookies: Optional[dict] = None,
        data: Optional[Any] = None,
        json: Optional[Any] = None,
        method: str = "get",
        timeout: int = 20,
        proxy: Optional[dict] = None,
        meta: Optional[dict] = None,
    ):
        self.url = url
        self.callback = (
            callback
            if isinstance(callback, str) or callback is None
            else callback.__name__
        )  # type: ignore[union-attr]
        self.headers = headers
        self.cookies = cookies
        self.method = method
        self.timeout = timeout
        self.proxy = proxy
        self.data = data
        self.json = json
        self.meta = meta
        self.id: Optional[str] = None
        self.retry: Optional[int] = None

    def add_request_id(
        self, request_id: Optional[str] = None, retry: Optional[int] = None
    ):
        self.id = str(uuid()) if request_id is None else request_id
        self.retry = 0 if retry is None else retry

    @staticmethod
    def from_json(request_dict: dict):
        request_id = request_dict.pop("requestId", None)
        retry_count = request_dict.pop("retry", None)
        request_object = Request(**request_dict)
        request_object.add_request_id(request_id, retry_count)
        return request_object

    def update_na(self,obj, key, value):
        obj[key] = obj[key] if  obj.get(key) is not None else value


    async def send(self,timeout:Optional[int]=None, proxy:Optional[dict]=None):
        async with AsyncClient() as client:
            request_json = self.to_json()
            self.update_na(request_json, "timeout", timeout)
            self.update_na(request_json, "proxy", proxy)
            request_json.pop("requestId")
            request_json.pop("retry")
            request_json.pop("meta")
            request_json.pop("callback")
            request_json.pop("method")
            request_json = {k: v for k, v in request_json.items() if v is not None}
            raw_response = await getattr(client, self.method)(**request_json)
            response = Response(raw_response, self)
            return response

    def to_json(self):
        return {
            "url": self.url,
            "callback": self.callback,
            "headers": self.headers,
            "cookies": self.cookies,
            "method": self.method,
            "timeout": self.timeout,
            "proxy": self.proxy,
            "meta": self.meta,
            "data": self.data,
            "json": self.json,
            "requestId": self.id,
            "retry": self.retry,
        }


class Response:
    def __init__(self, raw_response, request: Request):
        self.url = raw_response.url
        self.text = raw_response.text
        self.content = raw_response.content
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
            "request": self.request.to_json(),
        }
