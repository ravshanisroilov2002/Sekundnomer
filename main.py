import asyncio
from os import getenv
from dotenv import  load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from datetime import datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
load_dotenv()
TOKEN = getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_birth = {}

def life_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⏱ Sekund", callback_data="seconds"),
            InlineKeyboardButton(text="📆 Kun", callback_data="days")
        ],
        [
            InlineKeyboardButton(text="📅 Hafta", callback_data="weeks"),
            InlineKeyboardButton(text="🗓 Oy", callback_data="months")
        ]
    ])


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Assalomu alaykum! Tug'ilgan sanangizni kiriting:\n\nMisol: 15/03/2005")

@dp.message()
async def get_birthdate(message: types.Message):
    try:
        birth_date = datetime.strptime(message.text, "%d/%m/%Y")
        await message.answer("Sana qabul qilindi ✅ Endi tanlang 👇")
        user_birth[message.from_user.id] = birth_date
        await message.answer("Hisoblash turini tanlang:", reply_markup=life_keyboard())
    except:
        await message.answer("❌ Noto‘g‘ri format! dd/mm/yyyy shaklida yozing.")

@dp.callback_query()
async def calculate(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    birth = user_birth.get(user_id)

    if not birth:
        await callback.message.answer("Avval tug‘ilgan sanani kiriting!")
        return

    now = datetime.now()
    diff = now - birth

    if callback.data == "seconds":
        result = int(diff.total_seconds())
        await callback.message.answer(f"⏱ Siz {result:,} sekund yashagansiz!")

    elif callback.data == "days":
        await callback.message.answer(f"📆 Siz {diff.days:,} kun yashagansiz!")

    elif callback.data == "weeks":
        weeks = diff.days // 7
        await callback.message.answer(f"📅 Siz {weeks:,} hafta yashagansiz!")

    elif callback.data == "months":
        months = diff.days // 30
        await callback.message.answer(f"🗓 Siz taxminan {months:,} oy yashagansiz!")

    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())