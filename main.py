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
    
    if request.item_id not in inventory:
        raise HTTPException(
            status_code=404,
            detail={
                "error_code": "ITEM_NOT_FOUND",
                "message": "Item does not exist."
            }
        )

    item = inventory[request.item_id]

    if item["quantity"] <= 0:
        raise HTTPException(
            status_code=404,
            detail={
                "error_code": "OUT_OF_STOCK",
                "message": "Item is out of stock."
            }
        )
    
    if request.payment_cents < item["price_cents"]:
        if request.item_id == "A1":
            raise HTTPException(
                status_code=400,
                detail={
                    "error_code": "A1_BROKE",
                    "message": "Legacy hardware error for A1 slot."
                }
            )
        raise HTTPException(
            status_code=400,
            detail={
                "error_code": "INSUFFICIENT_FUNDS",
                "message": "Payment amount is less than the item price."
            }
        )

    item["quantity"] -= 1
    change = request.payment_cents - item["price_cents"]

    return {
        "vended_item_id": request.item_id,
        "change_returned_cents": change
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
