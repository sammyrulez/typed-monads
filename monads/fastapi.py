from dataclasses import dataclass
from fastapi import FastAPI, Request
import json
from typing import Any, Callable, List, Union, Optional
from monads import Maybe, List as HList
from starlette.middleware.base import BaseHTTPMiddleware


class Async_iterator_wrapper:
    def __init__(self, obj):
        self._it = iter(obj)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            value = next(self._it)
        except StopIteration:
            raise StopAsyncIteration
        return value


@dataclass
class HttpError:
    status_code: int
    text: str


ErrorDecoder = List[Callable[[Any], Maybe[HttpError]]]


class MonadicResponseMiddleware:
    @staticmethod
    def add_monadic_response_middleware(app: FastAPI, decoder: ErrorDecoder) -> None:
        app.add_middleware(
            BaseHTTPMiddleware, dispatch=MonadicResponseMiddleware(decoder)
        )

    def __init__(self, error_decoder: ErrorDecoder):
        self.error_decoder: HList[Callable[[Any], Maybe[HttpError]]] = HList(
            error_decoder
        )

    def check_for_error(self, x: Any) -> HList[HttpError]:
        a = self.error_decoder.map(lambda f: f(x))
        a = a.filter(lambda e: e.toOptional() != None).map(lambda e: e.toOptional()).flatten()  # type: ignore
        return a  # type: ignore

    async def __call__(self, request: Request, call_next):
        response = await call_next(request)
        resp_body: Union[str, List[Any]] = [
            section async for section in response.__dict__["body_iterator"]
        ]
        try:
            resp_body_obj = json.loads(resp_body[0].decode())  # type: ignore
            if isinstance(resp_body_obj, dict) and len(resp_body_obj.keys()) == 1:
                if "value" in resp_body_obj:
                    resp_body_obj = resp_body_obj["value"]
                    resp_body = json.dumps(resp_body_obj)
                elif "err" in resp_body_obj:

                    def check_status_code(h, k):
                        if k.status_code > h:
                            h = k.status_code
                        return h

                    checked_errors = self.check_for_error(resp_body_obj)
                    decoded_errors = checked_errors.map(lambda e: e.text)
                    response.status_code = checked_errors.fold(check_status_code, 400)
                    resp_body = (
                        decoded_errors.value
                        if decoded_errors
                        else json.dumps(resp_body_obj)
                    )
        except:
            resp_body = str(resp_body)

        response.__setattr__("body_iterator", Async_iterator_wrapper(resp_body))
        return response
