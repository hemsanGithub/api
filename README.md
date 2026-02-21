# Vending Machine API

## Run Locally

pip install -r requirements.txt
uvicorn main:app --reload

## Run with Docker

docker build -t vending-api .
docker run -p 8000:8000 vending-api

## Endpoints

GET /inventory
Header: X-Machine-Id

POST /vend
Header: X-Machine-Id
Body:
{
  "item_id": "A1",
  "payment_cents": 200
}

## Special Rule
If A1 is vended with insufficient funds,
returns error_code = A1_BROKE