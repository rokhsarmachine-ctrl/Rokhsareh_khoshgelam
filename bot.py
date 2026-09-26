import telebot
from telebot import types
import requests

TOKEN = "8557198522:AAEsN08N6TNy_NaBX9vZVVitnQUZYCs8MSs"
ADMIN_ID = 8070693669
AI_API_KEY = "YOUR_AI_KEY"

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
    except:
        return "پاسخی دریافت نشد."

# ---------------- START ----------------

@bot.message_handler(commands=['start'])
def start(message):

    # نمایش عکس پروفایل ربات
    try:
        photos = bot.get_user_profile_photos(bot.get_me().id)
        if photos.total_count > 0:
            bot.send_photo(message.chat.id, photos.photos[0][0].file_id)
    except:
        pass

    bot.send_message(message.chat.id, "به ربات رخساره خانوم خوش آمدید.")

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("پرسیدن سؤال", callback_data="ask_ai"))
    markup.add(types.InlineKeyboardButton("ثبت نوبت", callback_data="reserve"))
    markup.add(types.InlineKeyboardButton("ارسال عکس صورت (اختیاری)", callback_data="send_photo"))
    bot.send_message(message.chat.id, "انتخاب کنید:", reply_markup=markup)

# ---------------- INLINE BUTTON HANDLER ----------------

user_state = {}

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):

    if call.data == "ask_ai":
        user_state[call.message.chat.id] = {"step": "ai"}
        bot.send_message(call.message.chat.id, "سؤال خود را وارد کنید:")

    elif call.data == "reserve":
        user_state[call.message.chat.id] = {"step": "name"}
        bot.send_message(call.message.chat.id, "نام و نام خانوادگی:")

    elif call.data == "send_photo":
        user_state[call.message.chat.id] = {"step": "photo"}
        bot.send_message(call.message.chat.id, "عکس صورت خود را ارسال کنید:")

# ---------------- MESSAGE HANDLER ----------------

@bot.message_handler(func=lambda m: m.chat.id in user_state)
def state_handler(message):

    state = user_state[message.chat.id]

    # ---- AI ----
    if state["step"] == "ai":
        answer = ai_answer(message.text)
        bot.send_message(message.chat.id, answer)
        del user_state[message.chat.id]
        return

    # ---- PHOTO ----
    if state["step"] == "photo":
        bot.send_message(message.chat.id, "لطفاً عکس را به صورت *Photo* ارسال کنید.")
        return

    # ---- RESERVATION ----
    if state["step"] == "name":
        state["name"] = message.text
        state["step"] = "phone"
        bot.send_message(message.chat.id, "شماره تماس:")

    elif state["step"] == "phone":
        state["phone"] = message.text
        state["step"] = "date"
        bot.send_message(message.chat.id, "تاریخ نوبت:")

    elif state["step"] == "date":
        state["date"] = message.text

        bot.send_message(
            message.chat.id,
            f"نوبت ثبت شد.\n"
            f"نام: {state['name']}\n"
            f"شماره: {state['phone']}\n"
            f"تاریخ: {state['date']}"
        )

        bot.send_message(
            ADMIN_ID,
            f"نوبت جدید:\n"
            f"نام: {state['name']}\n"
            f"شماره: {state['phone']}\n"
            f"تاریخ: {state['date']}\n"
            f"آیدی: @{message.from_user.username}"
        )

        del user_state[message.chat.id]

# ---------------- PHOTO RECEIVER ----------------

@bot.message_handler(content_types=['photo'])
def receive_photo(message):

    # اگر کاربر در حالت ارسال عکس باشد
    if message.chat.id in user_state and user_state[message.chat.id]["step"] == "photo":
        bot.send_message(message.chat.id, "عکس دریافت شد.")
        bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
        del user_state[message.chat.id]
    else:
        # اگر عکس خارج از حالت ارسال شد، فقط نادیده گرفته می‌شود
        pass

bot.infinity_polling()