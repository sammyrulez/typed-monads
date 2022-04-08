FastAPI is a modern, fast (high-performance), web framework for building APIs with Python.

You can use a monadic structure to wrap the response of your endpoint

```python
from monads import MonadicResponseMiddleware, HttpError

def check_not_found(x: Dict[str, Any]) -> Maybe[HttpError]:
    if is_not_found_error(x):
        return Just(HttpError(404, "The item was't there!"))
    else:
        return Nothing()


MonadicResponseMiddleware.add_monadic_response_middleware(app, [check_not_found])

def read_from_source(item_id) -> Result[Item,str] # return an item or an error with a localized message
    ...

@app.get("/items/{item_id}")
async def read_item(item_id: str) -> Result[Item, str]:
    return read_from_source(item_id).map(lambda item: item.price = item.price * 1.2) # the transformation occurs only if there were no errors

```

The response is either the expected payload or, in case of error a list of objects, generated  by  the _error checker_ Callables

_FastAPI support is under heavy development_ details may change in the future.

