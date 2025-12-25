import httpx
import uuid
import os

PAYSTACK_SECRET = os.getenv("PAYSTACK_SECRET")

async def initialize_payment(email: str, amount: int):
    reference = str(uuid.uuid4())

    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET}",
        "Content-Type": "application/json"
    }

    payload = {
        "email": email,
        "amount": amount * 100,
        "reference": reference
    }

    async with httpx.AsyncClient() as client:
        r = await client.post(
            "https://api.paystack.co/transaction/initialize",
            json=payload,
            headers=headers
        )

    data = r.json()
    return data["data"]["authorization_url"], reference
