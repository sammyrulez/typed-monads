from dataclasses import dataclass
from fastapi import FastAPI, Request
import json
from typing import Any, Callable, List, Union
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
class MonadicHttpError:
    status_code: int
    text: str


ErrorDecoder = List[Callable[[Any], Maybe[MonadicHttpError]]]


class MonadicResponseMiddleware:
    @staticmethod
    def add_monadic_response_middleware(app: FastAPI, decoder: ErrorDecoder) -> None:
        app.add_middleware(
            BaseHTTPMiddleware, dispatch=MonadicResponseMiddleware(decoder)
        )

    def __init__(self, error_decoder: ErrorDecoder):
        self.error_decoder: HList[Callable[[Any], Maybe[MonadicHttpError]]] = HList(
            error_decoder
        )

    def check_for_error(self, x: Any) -> Maybe[MonadicHttpError]:
        return (
            self.error_decoder.map(lambda f: f(x))
            .filter(
                lambda m: m.toOptional() != None
            )  # ugly but type consistent TODO: Maybe is present?
            .head()
            .flatten()
        )

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

                    def decode_error(m: MonadicHttpError):
                        response.status_code = m.status_code
                        return m

                    new1 = self.check_for_error(resp_body_obj)
                    kd = new1.map(decode_error)
                    resp_body = kd.or_else(json.dumps(resp_body_obj)).get()
        except:
            resp_body = str(resp_body)

        response.__setattr__("body_iterator", Async_iterator_wrapper(resp_body))
        return response
