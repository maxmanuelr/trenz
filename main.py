from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, field_validator
from datetime import datetime

app = FastAPI()

class WeightLog(BaseModel):
    weight: float
    date: str
    note: str | None = None

    @field_validator('weight')
    @classmethod
    def weight_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError('Weight must be greater than zero')
        return value
    
    @field_validator('date')
    @classmethod
    def date_must_be_valid(cls, value):
        try:
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format, e.g. 2026-05-19")
        return value
    
    

class CheckIn(BaseModel):
    weight: float
    calories: int
    note: str | None = None

    @field_validator('calories')
    @classmethod
    def calories_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError('Calories must be greater than zero')
        return value 


class CheckInResponse(BaseModel):
    weight: float
    calories: int 
    note: str | None = None
    received: bool 
    id: int
    created_at: str

class UpdateWeight(BaseModel):
    weight: float

@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/log/weight", status_code=status.HTTP_201_CREATED)
async def log_weight(weight_log: WeightLog):
    return {"received": True, "weight": weight_log.weight, "date": weight_log.date, "note": weight_log.note}


@app.get("/log/weight")
async def get_log_weight(limit: int = 7, unit: str = "lbs"):
    return {"limit": limit, "unit": unit, "entries": []}


@app.post("/checkin", status_code=status.HTTP_201_CREATED, response_model=CheckInResponse)
async def check_in(check_in: CheckIn):
    return {"received": True, "weight": check_in.weight, "calories": check_in.calories, "note": check_in.note}


@app.get("/checkin/{id}")
async def get_check_in(id:int):
    if id > 100:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Id can't be greater than 100"
        )
    return {"id": id, "found": True}


@app.put("/checkin/{id}")
async def update_check_in(id:int, new_weight: UpdateWeight):
    return {"updated": id, "weight": new_weight.weight}


@app.delete("/checkin/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_check_in(id:int):
    return 


