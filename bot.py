import telebot
from telebot import types
import requests

# ---------------- CONFIG ----------------

TOKEN = "8860048564:AAFJLbLpblSRBfImGzbBGgw1PI7izGUZvNk"
ADMIN_ID = 8070693669

# ❗ API KEY دیپ‌سیک را اینجا قرار بده
AI_API_KEY = "sk-24f38cc1f46143f88297c4c530b870bc"

bot = telebot.TeleBot(TOKEN)

# ---------------- AI (DeepSeek) ----------------

def ai_answer(question):
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": question}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        # اگر DeepSeek خطا برگرداند
        if "error" in result:
            return f"❗ خطا از سمت DeepSeek:\n{result['error']['message']}"

        return result["choices"][0]["message"]["content"]

    except Exception as e:
        return f"❗ مشکلی پیش آمد:\n{str(e)}"

# ---------------- START ----------------

@bot.message_handler(commands=['start'])
def start(message):

    try:
        photos = bot.get_user_profile_photos(bot.get_me().id)
        if photos.total_count > 0:
            bot.send_photo(message.chat.id, photos.photos[0][0].file_id)
    except:
        pass

    bot.send_message(message.chat.id, "🌸 به ربات خدمات مزووایت خوش آمدید 🌸")

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🤖 پرسیدن سؤال از هوش مصنوعی", callback_data="ask_ai"))
    markup.add(types.InlineKeyboardButton("🗓 ثبت نوبت", callback_data="reserve"))
    markup.add(types.InlineKeyboardButton("📸 ارسال عکس صورت", callback_data="photo"))
    markup.add(types.InlineKeyboardButton("✨ درباره مزووایت", callback_data="about"))
    markup.add(types.InlineKeyboardButton("⚖️ مزایا و معایب مزووایت", callback_data="pros_cons"))

    bot.send_message(message.chat.id, "لطفاً یکی از گزینه‌ها را انتخاب کنید:", reply_markup=markup)

# ---------------- INLINE BUTTONS ----------------

user_state = {}

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):

    chat_id = call.message.chat.id

    if call.data == "ask_ai":
        user_state[chat_id] = {"step": "ai"}
        bot.send_message(chat_id, "❓ سؤال خود را وارد کنید:")

    elif call.data == "reserve":
        user_state[chat_id] = {"step": "name"}
        bot.send_message(chat_id, "👤 نام و نام خانوادگی:")

    elif call.data == "photo":
        user_state[chat_id] = {"step": "photo"}
        bot.send_message(chat_id, "📸 لطفاً عکس صورت خود را ارسال کنید:")

    elif call.data == "about":
        bot.send_message(
            chat_id,
            "✨ **مزووایت چیست؟**\n\n"
            "مزووایت یک روش روشن‌سازی و یکدست‌سازی پوست است که با تزریق مواد مغذی، روشن‌کننده و آبرسان، باعث کاهش تیرگی، لک‌ها و کدری پوست می‌شود."
        )

    elif call.data == "pros_cons":
        bot.send_message(
            chat_id,
            "⚖️ **مزایا و معایب مزووایت**\n\n"
            "✅ *مزایا:*\n"
            "• روشن‌سازی پوست\n"
            "• کاهش لک و تیرگی\n"
            "• آبرسانی و شفافیت\n"
            "• یکدست شدن رنگ پوست\n\n"
            "❌ *معایب:*\n"
            "• نیاز به چند جلسه برای نتیجه کامل\n"
            "• احتمال قرمزی یا حساسیت موقت\n"
            "• مناسب نبودن برای برخی پوست‌های خیلی حساس"
        )

# ---------------- MESSAGE HANDLER ----------------

@bot.message_handler(func=lambda m: m.chat.id in user_state)
def state_handler(message):

    chat_id = message.chat.id
    state = user_state[chat_id]

    if state["step"] == "ai":
        bot.send_message(chat_id, "⏳ در حال دریافت پاسخ…")
        answer = ai_answer(message.text)
        bot.send_message(chat_id, f"🤖 پاسخ:\n{answer}")
        del user_state[chat_id]
        return

    if state["step"] == "photo":
        bot.send_message(chat_id, "⚠️ لطفاً عکس را به صورت Photo ارسال کنید.")
        return

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