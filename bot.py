import telebot
from telebot import types
import requests

TOKEN = "8557198522:AAEsN08N6TNy_NaBX9vZVVitnQUZYCs8MSs"
ADMIN_ID = 8070693669
AI_API_KEY = "YOUR_REAL_AI_KEY"   # کلید واقعی هوش مصنوعی

bot = telebot.TeleBot(TOKEN)

# ---------------- AI TEXT ANSWER ----------------

def ai_answer(question):
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        return result["choices"][0]["message"]["content"]

    except Exception as e:
        return "متأسفم عزیزم، مشکلی در ارتباط با هوش مصنوعی پیش اومد 🌸"

# ---------------- START ----------------

@bot.message_handler(commands=['start'])
def start(message):

    # نمایش عکس پروفایل ربات
    try:
        photos = bot.get_user_profile_photos(bot.get_me().id)
        if photos.total_count > 0:
            file_id = photos.photos[0][0].file_id
            bot.send_photo(message.chat.id, file_id)
    except:
        pass

    bot.send_message(
        message.chat.id,
        "به ربات خدمات مزووایت رخساره خانوم 🥰 خوش اومدی\n"
        "لطفاً یکی از گزینه‌های زیر رو انتخاب کن."
    )

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🤖 پرسیدن سؤال از هوش مصنوعی", callback_data="ask_ai"))
    markup.add(types.InlineKeyboardButton("🗓 ثبت نوبت", callback_data="reserve"))
    markup.add(types.InlineKeyboardButton("✨ مزووایت چیست؟", callback_data="info"))
    markup.add(types.InlineKeyboardButton("📞 ارتباط با رخساره خانوم", url="https://t.me/Rokhsareh_Hanum"))

    bot.send_message(message.chat.id, "منوی اصلی:", reply_markup=markup)

# ---------------- INLINE BUTTON HANDLER ----------------

user_state = {}

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):

    if call.data == "ask_ai":
        user_state[call.message.chat.id] = {"step": "ai_question"}
        bot.send_message(call.message.chat.id, "سؤال خود را از هوش مصنوعی بپرس:")

    elif call.data == "info":
        bot.send_message(call.message.chat.id, "مزووایت یک روش روشن‌سازی و یکدست‌سازی پوست هست ✨")

    elif call.data == "reserve":
        user_state[call.message.chat.id] = {"step": "name"}
        bot.send_message(call.message.chat.id, "لطفاً نام و نام خانوادگی خود را وارد کنید:")

# ---------------- MESSAGE HANDLER ----------------

@bot.message_handler(func=lambda m: m.chat.id in user_state)
def state_handler(message):

    state = user_state[message.chat.id]

    # ---- AI QUESTION ----
    if state["step"] == "ai_question":
        question = message.text
        bot.send_message(message.chat.id, "در حال دریافت پاسخ از هوش مصنوعی… 🤖")
        answer = ai_answer(question)
        bot.send_message(message.chat.id, answer)
        del user_state[message.chat.id]
        return

    # ---- RESERVATION ----
    if state["step"] == "name":
        state["name"] = message.text
        state["step"] = "phone"
        bot.send_message(message.chat.id, "شماره تماس خود را وارد کنید:")

    elif state["step"] == "phone":
        state["phone"] = message.text
        state["step"] = "date"
        bot.send_message(message.chat.id, "تاریخ مورد نظر برای نوبت را وارد کنید:")

    elif state["step"] == "date":
        state["date"] = message.text

        bot.send_message(
            message.chat.id,
            f"نوبت شما با موفقیت ثبت شد 🌸\n\n"
            f"👤 نام: {state['name']}\n"
            f"📞 شماره: {state['phone']}\n"
            f"🗓 تاریخ: {state['date']}\n\n"
            f"رخساره خانوم به زودی با شما تماس می‌گیرند 💖"
        )

        bot.send_message(
            ADMIN_ID,
            f"📥 نوبت جدید ثبت شد:\n"
            f"👤 نام: {state['name']}\n"
            f"📞 شماره: {state['phone']}\n"
            f"🗓 تاریخ: {state['date']}\n"
            f"آیدی: @{message.from_user.username}"
        )

        del user_state[message.chat.id]

bot.infinity_polling()