from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn

app = FastAPI()

# In-memory store
inventory = {
    "A1": {"id": "A1", "name": "Cola", "price_cents": 150, "quantity": 5},
    "B1": {"id": "B1", "name": "Chips", "price_cents": 100, "quantity": 3},
}

class Item(BaseModel):
    id: str
    name: str
    price_cents: int
    quantity: int

class VendRequest(BaseModel):
    item_id: str
    payment_cents: int

class ErrorResponse(BaseModel):
    error_code: str
    message: str

@app.get("/inventory", response_model=List[Item])
def get_inventory(x_machine_id: str = Header(None)):
    if not x_machine_id:
        raise HTTPException(
            status_code=400,
            detail={
                "error_code": "MISSING_MACHINE_ID",
                "message": "X-Machine-Id header is required."
            }
        )
    return list(inventory.values())

@app.post("/vend")
def vend_item(request: VendRequest, x_machine_id: str = Header(None)):
    if not x_machine_id:
        raise HTTPException(
            status_code=400,
            detail={
                "error_code": "MISSING_MACHINE_ID",
                "message": "X-Machine-Id header is required."
            }
        )