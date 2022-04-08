from dataclasses import dataclass
from typing import Any, Dict
from monads import MonadicResponseMiddleware, HttpError
from fastapi import FastAPI
from fastapi.testclient import TestClient
from monads.maybe import Just, Maybe, Nothing
from monads.result import Err, Ok, Result

app = FastAPI()


def check_not_found(x: Dict[str, Any]) -> Maybe[HttpError]:
    if "err" in x and "not found" in x["err"]:
        return Just(HttpError(404, x["err"]))
    else:
        return Nothing()


MonadicResponseMiddleware.add_monadic_response_middleware(app, [check_not_found])


@dataclass
class Item:
    item_id: str


@app.get("/items/{item_id}")
async def read_item(item_id: str) -> Result[Item, str]:
    if item_id == "xyz":
        return Ok(Item(item_id))
    else:
        return Err(f"Item {item_id} not found")


client = TestClient(app)


def test_monadic_response():
    response = client.get("/items/xyz")
    assert response.status_code == 200
    assert response.json() == {"item_id": "xyz"}
    response = client.get("/items/kkk")
    assert response.status_code == 404
