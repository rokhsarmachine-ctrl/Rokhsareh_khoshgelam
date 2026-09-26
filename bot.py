import telebot
from telebot import types

TOKEN = "8557198522:AAEsN08N6TNy_NaBX9vZVVitnQUZYCs8MSs"
ADMIN_ID = 8070693669

bot = telebot.TeleBot(TOKEN)

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

    bot.send_message(message.chat.id, "🌸 به ربات رخساره خانوم خوش آمدید 🌸")

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💬 پرسیدن سؤال", callback_data="ask"))
    markup.add(types.InlineKeyboardButton("🗓 ثبت نوبت", callback_data="reserve"))
    markup.add(types.InlineKeyboardButton("📸 ارسال عکس صورت", callback_data="photo"))
    bot.send_message(message.chat.id, "لطفاً یکی از گزینه‌ها را انتخاب کنید:", reply_markup=markup)

# ---------------- INLINE BUTTONS ----------------

user_state = {}

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):

    chat_id = call.message.chat.id

    if call.data == "ask":
        user_state[chat_id] = {"step": "ask"}
        bot.send_message(chat_id, "❓ سؤال خود را وارد کنید:")

    elif call.data == "reserve":
        user_state[chat_id] = {"step": "name"}
        bot.send_message(chat_id, "👤 نام و نام خانوادگی:")

    elif call.data == "photo":
        user_state[chat_id] = {"step": "photo"}
        bot.send_message(chat_id, "📸 لطفاً عکس صورت خود را ارسال کنید:")

# ---------------- MESSAGE HANDLER ----------------

@bot.message_handler(func=lambda m: m.chat.id in user_state)
def state_handler(message):

    chat_id = message.chat.id
    state = user_state[chat_id]

    # ---- SIMPLE QUESTION ANSWER ----
    if state["step"] == "ask":
        bot.send_message(chat_id, f"💬 پاسخ شما:\n{message.text}")
        del user_state[chat_id]
        return

    # ---- PHOTO MODE ----
    if state["step"] == "photo":
        bot.send_message(chat_id, "⚠️ لطفاً عکس را به صورت Photo ارسال کنید.")
        return

    # ---- RESERVATION ----
    if state["step"] == "name":
        state["name"] = message.text
        state["step"] = "phone"
        bot.send_message(chat_id, "📞 شماره تماس:")

    elif state["step"] == "phone":
        state["phone"] = message.text
        state["step"] = "date"
        bot.send_message(chat_id, "📅 تاریخ نوبت:")

    elif state["step"] == "date":
        state["date"] = message.text

        bot.send_message(
            chat_id,
            f"✅ نوبت شما ثبت شد.\n\n"
            f"👤 نام: {state['name']}\n"
            f"📞 شماره: {state['phone']}\n"
            f"📅 تاریخ: {state['date']}"
        )

        bot.send_message(
            ADMIN_ID,
            f"📥 نوبت جدید:\n"
            f"👤 نام: {state['name']}\n"
            f"📞 شماره: {state['phone']}\n"
            f"📅 تاریخ: {state['date']}\n"
            f"🔗 آیدی: @{message.from_user.username}"
        )

        del user_state[chat_id]

# ---------------- PHOTO RECEIVER ----------------

@bot.message_handler(content_types=['photo'])
def receive_photo(message):

    chat_id = message.chat.id

    if chat_id in user_state and user_state[chat_id]["step"] == "photo":
        bot.send_message(chat_id, "📸 عکس دریافت شد.")
        bot.forward_message(ADMIN_ID, chat_id, message.message_id)
        del user_state[chat_id]

bot.infinity_polling()