import asyncio
import sqlite3
import datetime
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup

# ---------------- CONFIG ----------------
TOKEN = "8834409229:AAGRsS9_rzgdtg8JxLQ2aqSpyVN3i0HISV0"
ADMIN_ID = 8070693669
LOGO_PATH = "logo.jpg"

# ---------------- DATABASE ----------------
conn = sqlite3.connect("mezowhite.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS orders(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    name TEXT,
    phone TEXT,
    description TEXT,
    ai_analysis TEXT,
    photo_path TEXT,
    date TEXT
)
""")
conn.commit()

# ---------------- STATES ----------------
class OrderState(StatesGroup):
    name = State()
    phone = State()
    description = State()
    photo = State()

# ---------------- AI ----------------
def copilot_ai_analysis(text):
    text = text.lower()

    if "لک" in text or "تیرگی" in text:
        return "تحلیل هوش مصنوعی: پوست دارای لک و تیرگی است."

    if "جوش" in text or "آکنه" in text:
        return "تحلیل هوش مصنوعی: پوست مستعد آکنه است."

    if "خشک" in text:
        return "تحلیل هوش مصنوعی: پوست خشک است."

    return "تحلیل هوش مصنوعی: نیاز به بررسی بیشتر دارد."

# ---------------- BOT ----------------
bot = Bot(token=TOKEN)
dp = Dispatcher()

# ---------------- START ----------------
@dp.message(Command("start"))
async def start(msg: types.Message):

    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("✨ ثبت سفارش مزووایت", "📞 تماس با پشتیبانی")
    kb.add("📸 ارسال عکس پوست", "ℹ️ راهنمای مزووایت")

    if os.path.exists(LOGO_PATH):
        try:
            with open(LOGO_PATH, "rb") as photo:
                await msg.answer_photo(
                    photo=photo,
                    caption="سلام عزیزم به ربات تلگرامی خدمات مزووایت رخساره خانوم خوشگل 🥰 آقا وحید خوش اومدی",
                    reply_markup=kb
                )
                return
        except:
            pass

    await msg.answer(
        "سلام عزیزم به ربات تلگرامی خدمات مزووایت رخساره خانوم خوشگل 🥰 آقا وحید خوش اومدی",
        reply_markup=kb
    )

# ---------------- ORDER ----------------
@dp.message(lambda m: m.text == "✨ ثبت سفارش مزووایت")
async def order_start(msg: types.Message, state: FSMContext):
    await msg.answer("نام و نام خانوادگی خود را وارد کن:")
    await state.set_state(OrderState.name)

@dp.message(OrderState.name)
async def get_name(msg: types.Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer("شماره تماس را وارد کن:")
    await state.set_state(OrderState.phone)

@dp.message(OrderState.phone)
async def get_phone(msg: types.Message, state: FSMContext):
    await state.update_data(phone=msg.text)
    await msg.answer("مشکل پوستی‌ات را توضیح بده:")
    await state.set_state(OrderState.description)

@dp.message(OrderState.description)
async def get_description(msg: types.Message, state: FSMContext):
    await state.update_data(description=msg.text)

    ai_result = copilot_ai_analysis(msg.text)
    await state.update_data(ai_analysis=ai_result)

    await msg.answer(
        f"🔍 تحلیل هوش مصنوعی:\n{ai_result}\n\n"
        "اگر عکس صورت داری ارسال کن.\nاگر نداری بنویس: «ندارم»"
    )

    await state.set_state(OrderState.photo)

@dp.message(OrderState.photo, content_types=['photo', 'text'])
async def get_photo(msg: types.Message, state: FSMContext):
    data = await state.get_data()

    photo_path = "NO_PHOTO"

    if msg.photo:
        photo = msg.photo[-1]
        photo_path = f"files/{photo.file_id}.jpg"
        await photo.download(photo_path)

    cur.execute("""
        INSERT INTO orders(user_id, name, phone, description, ai_analysis, photo_path, date)
        VALUES(?,?,?,?,?,?,?)
    """, (
        msg.from_user.id,
        data["name"],
        data["phone"],
        data["description"],
        data["ai_analysis"],
        photo_path,
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    ))

    conn.commit()

    await msg.answer("سفارش مزووایت با موفقیت ثبت شد عزیزم ❤️")
    await state.clear()

# ---------------- ADMIN ----------------
@dp.message(Command("admin"))
async def admin(msg: types.Message):
    if msg.from_user.id != ADMIN_ID:
        return

    cur.execute("SELECT id, name, phone, description, ai_analysis, photo_path, date FROM orders")
    rows = cur.fetchall()

    if not rows:
        await msg.answer("هیچ سفارشی ثبت نشده.")
        return

    for r in rows:
        order_id, name, phone, desc, ai, photo_path, date = r

        await msg.answer(
            f"🆔 سفارش: {order_id}\n"
            f"👤 نام: {name}\n"
            f"📞 تماس: {phone}\n"
            f"📄 توضیحات: {desc}\n"
            f"🤖 تحلیل هوش مصنوعی:\n{ai}\n"
            f"📅 تاریخ: {date}"
        )

        if photo_path != "NO_PHOTO":
            try:
                await msg.answer_photo(open(photo_path, "rb"))
            except:
                await msg.answer("❗ عکس قابل ارسال نیست.")

# ---------------- RUN ----------------
async def main():
    if not os.path.exists("files"):
        os.mkdir("files")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())