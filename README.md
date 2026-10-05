# Number API

### FastAPI — Task B

Run:

bash
uvicorn fastapi_app:app --reload


The FastAPI application runs on:

text
http://127.0.0.1:8000


API documentation:

text
http://127.0.0.1:8000/docs


Endpoint:

text
POST /stats


Example request:
json
{
  "numbers": [4, 8, 15]
}


Example response:

json
{
  "count": 3,
  "sum": 27,
  "average": 9.0,
  "max": 15,
  "seconds": 1.0
}


## Flask vs FastAPI Validation

In Flask, validation for `/check` is performed manually using Python conditions. The application checks whether the JSON is valid, whether `number` is present, whether it is a whole integer, and whether it is between 1 and 1000.

In FastAPI, validation for `/stats` is handled using a Pydantic model. The model defines the required `numbers` field, the allowed number of items, and the required integer type and range. Invalid requests automatically receive FastAPI's standard validation error.

## Why `/stats` Takes About 1 Second

The sum, average, and maximum are calculated by three separate asynchronous functions. Each function waits for 1 second using `asyncio.sleep(1)`.

The endpoint uses `asyncio.gather()` to run the three functions concurrently. Therefore, their one-second waits happen at the same time instead of sequentially.

Without concurrency:

text
1 second + 1 second + 1 second = about 3 seconds

With `asyncio.gather()`:
text
All three functions run concurrently = about 1 second


The actual measured execution time is returned in the `seconds` field.

This is enough for the README requirement.You don't need to put all your Postman test cases or Git commands in the README—the detailed test requests and Git commands belong in the **PR description.