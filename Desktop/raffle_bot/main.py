import asyncio
from bot import dp, bot
from webhook import app
from database import Base, engine
import uvicorn
from raffle_bot.bot import dp, bot
from fastapi import FastAPI


app = FastAPI()

Base.metadata.create_all(engine)

async def start_bot():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.create_task(start_bot())
    uvicorn.run(app, host="0.0.0.0", port=8000)

@app.get("/")
def health():
    return {"status": "ok"}
