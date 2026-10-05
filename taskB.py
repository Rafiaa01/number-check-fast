import asyncio
import time

from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field, StrictInt, field_validator

app = FastAPI()


class NumberStatsRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    numbers: list[StrictInt] = Field(..., min_length=1, max_length=10)

    @field_validator("numbers")
    @classmethod
    def validate_numbers(cls, numbers):
        for number in numbers:
            if not 1 <= number <= 1000:
                raise ValueError("each number must be between 1 and 1000")
        return numbers


async def calculate_sum(numbers):
    await asyncio.sleep(1)
    return sum(numbers)


async def calculate_average(numbers):
    await asyncio.sleep(1)
    return sum(numbers) / len(numbers)


async def calculate_max(numbers):
    await asyncio.sleep(1)
    return max(numbers)


@app.post("/stats")
async def stats(data: NumberStatsRequest):
    start_time = time.perf_counter()

    total, average, maximum = await asyncio.gather(
        calculate_sum(data.numbers),
        calculate_average(data.numbers),
        calculate_max(data.numbers),
    )

    elapsed_time = time.perf_counter() - start_time

    return {
        "count": len(data.numbers),
        "sum": total,
        "average": average,
        "max": maximum,
        "seconds": round(elapsed_time, 1),
    }
