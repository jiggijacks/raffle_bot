from fastapi import FastAPI, Request
from database import SessionLocal
from models import Ticket

app = FastAPI()

@app.post("/webhook/paystack")
async def paystack_webhook(request: Request):
    payload = await request.json()

    if payload["event"] != "charge.success":
        return {"status": "ignored"}

    user_id = int(payload["data"]["customer"]["email"].split("@")[0])
    reference = payload["data"]["reference"]

    db = SessionLocal()
    ticket = Ticket(user_id=user_id, reference=reference)
    db.add(ticket)
    db.commit()
    db.close()

    return {"status": "ticket issued"}
