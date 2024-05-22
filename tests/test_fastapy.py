from dataclasses import dataclass
from typing import Any, Dict, List

from pydantic import BaseModel
from monads import MonadicResponseMiddleware, HttpError
from fastapi import FastAPI
from fastapi.testclient import TestClient
from monads.maybe import Just, Maybe, Nothing
from monads.result import Err, Ok, Result

app = FastAPI()


def check_not_found(x: Dict[str, Any]) -> Maybe[HttpError]:
    if "err" in x and "not found" in x["err"]:
        return Just(HttpError(404, x["err"]))
    elif "Failure" in x["err"]:
        return Just(HttpError(500, x["err"]))
    else:
        return Nothing()


MonadicResponseMiddleware.add_monadic_response_middleware(app, [check_not_found])


@dataclass
class Item:
    item_id: str


@dataclass
class Person:
    err: str
    value: int


@app.get("/people/")
async def people() -> List[Person]:
    return [Person("Sam", 10)]


@app.get("/people/{item_id}")
async def person_detail(item_id: str) -> Person:
    return Person("Sam", 10)


class ResultResponse(BaseModel):
    def __init__(self, result: Result[Any, Any]):
        self.result = result

    def __call__(self):
        if self.result.is_ok():
            return self.result.value
        else:
            raise HttpError(500, self.result.error)


# TODO: Fix this: not more compatible with modern fastapi
@app.get("/items/{item_id}")
async def read_item(item_id: str) -> ResultResponse:
    if item_id == "xyz":
        return ResultResponse(Ok(Item(item_id)))
    elif item_id == "gold":
        return ResultResponse(Err("Failure"))
    else:
        return ResultResponse(Err(f"Item {item_id} not found"))


client = TestClient(app)

"""
def test_monadic_response():
    response = client.get("/items/xyz")
    assert response.status_code == 200
    assert response.json() == {"item_id": "xyz"}
    response = client.get("/items/kkk")
    assert response.status_code == 404
    response = client.get("/items/gold")
    assert response.status_code == 500
"""


def test_regular_resposne():
    response = client.get("/people/")

    assert response.status_code == 200
    response = client.get("/people/xyz")
    assert response.status_code == 200
