import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from paystack import initialize_payment
from database import SessionLocal
from models import Ticket

bot = Bot(os.getenv("BOT_TOKEN"))
dp = Dispatcher()

def menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎟 Buy Ticket", callback_data="BUY")],
        [InlineKeyboardButton(text="📄 My Tickets", callback_data="MY")]
    ])

@dp.message(F.text == "/start")
async def start(message: Message):
    await message.answer("Welcome to the raffle bot", reply_markup=menu())

@dp.callback_query(F.data == "BUY")
async def buy_ticket(call: CallbackQuery):
    url, reference = await initialize_payment(
        email=f"{call.from_user.id}@raffle.com",
        amount=1000
    )

    await call.message.answer(
        "Pay using Paystack:",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Pay Now", url=url)]
            ]
        )
    )

@dp.callback_query(F.data == "MY")
async def my_tickets(call: CallbackQuery):
    db = SessionLocal()
    count = db.query(Ticket).filter(
        Ticket.user_id == call.from_user.id
    ).count()
    db.close()

    await call.message.answer(f"You have {count} ticket(s)")
