from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class WeightLog(BaseModel):
    weight: float
    date: str
    note: Optional[str] = None

class CheckIn(BaseModel):
    weight: float
    calories: int
    note: Optional[str] = None

class UpdateWeight(BaseModel):
    weight: float

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/log/weight", status_code=status.HTTP_201_CREATED)
def log_weight(weight_log: WeightLog):
    if weight_log.weight <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Weight can't be negative or zero"
        )
    return {"received": True, "weight": weight_log.weight, "date": weight_log.date, "note": weight_log.note}

@app.get("/log/weight")
def get_log_weight(limit: int = 7, unit: str = "lbs"):
    return {"limit": limit, "unit": unit, "entries": []}

@app.post("/checkin", status_code=status.HTTP_201_CREATED)
def check_in(check_in: CheckIn):
    return {"received": True, "weight": check_in.weight, "calories": check_in.calories, "note": check_in.note}

@app.get("/checkin/{id}")
def get_check_in(id:int):
    if id > 100:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Id can't be greater than 100"
        )
    return {"id": id, "found": True}


@app.put("/checkin/{id}")
def update_check_in(id:int, new_weight: UpdateWeight):
    return {"updated": id, "weight": new_weight.weight}

@app.delete("/checkin/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_check_in(id:int):
    return 

@app.post("/log/weight", status_code=status.HTTP_201_CREATED)
def log_weight(weight_log: WeightLog):
    if weight_log.weight <= 0:
        raise HTTPException(status_code=400, detail="Weight can't be negative or zero")
    return {...}