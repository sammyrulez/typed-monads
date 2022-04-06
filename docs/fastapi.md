FastAPI is a modern, fast (high-performance), web framework for building APIs with Python.

You can use a monadic structure to wrap the response of your endpoint

```python
from monads.fastapi import MonadicHttpError

def check_not_found(x: Dict[str, Any]) -> Maybe[MonadicHttpError]:
    if "err" in x and "not found" in x["err"]:
        return Just(MonadicHttpError(404, x["err"]))
    else:
        return Nothing()


MonadicResponseMiddleware.add_monadic_response_middleware(app, [check_not_found])

def read_from_source(item_id) -> Result[Item,str] # return an item or an error with a localized message
    ...


@app.get("/items/{item_id}")
async def read_item(item_id: str) -> Result[Item, str]:
    return read_from_source(item_id).map(lambda item: item.sku = '#REDACTED#') # the transformation occurs only if there were no errors

```

_FastAPI support is under heavy development_ details may change in the future.

