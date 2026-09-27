import telebot
from telebot import types
import google.generativeai as genai

# -----------------------------
# ⚙️ تنظیمات ربات
# -----------------------------
BOT_TOKEN = "8557198522:AAGtu84u20Qo3w8eb-ANxXBI1J5bG2kCNeA"
ADMIN_ID = 8070693669   # آیدی عددی مدیر
GEMINI_KEY = "YOUR_GEMINI_API_KEY"

bot = telebot.TeleBot(BOT_TOKEN)

# -----------------------------
# 🤖 تنظیمات Gemini
# -----------------------------
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def ask_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except:
        return "⚠️ در پردازش پیام شما خطایی رخ داد."

# -----------------------------
# 🗂 دیتای کاربران
# -----------------------------
user_data = {}

# -----------------------------
# 🚀 شروع ربات
# -----------------------------
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()

    btn1 = types.InlineKeyboardButton("❓ پرسیدن سؤال", callback_data="ask")
    btn2 = types.InlineKeyboardButton("🗓 ثبت نوبت", callback_data="reserve")
    btn3 = types.InlineKeyboardButton("📸 ارسال عکس صورت", callback_data="photo")
    btn4 = types.InlineKeyboardButton("✨ درباره مزووایت", callback_data="mezowhite")
    btn5 = types.InlineKeyboardButton("💆‍♀️ مراقبت‌های قبل و بعد", callback_data="care")

    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    markup.add(btn4)
    markup.add(btn5)

    bot.send_message(
        message.chat.id,
        "سلام عزیزم 🌸\n"
        "به ربات خدمات مزووایت رخساره خانوم 🥰 خوش اومدی ✨\n"
        "لطفاً یکی از گزینه‌های زیر رو انتخاب کن:",
        reply_markup=markup
    )

# -----------------------------
# 🎛 هندل دکمه‌ها
# -----------------------------
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "ask":
        bot.send_message(call.message.chat.id, "❓ سؤال خود را بپرس عزیزم:")

    elif call.data == "reserve":
        bot.send_message(call.message.chat.id, "👤 لطفاً نام خود را وارد کنید:")
        bot.register_next_step_handler(call.message, get_name)

    elif call.data == "photo":
        bot.send_message(call.message.chat.id, "📸 لطفاً عکس صورت خود را ارسال کنید:")

    elif call.data == "mezowhite":
        send_mezowhite_info(call.message.chat.id)

    elif call.data == "care":
        send_care_info(call.message.chat.id)

# -----------------------------
# ✨ بخش درباره مزووایت
# -----------------------------
def send_mezowhite_info(chat_id):
    text = (
        "✨ **مزووایت چیست؟**\n"
        "مزووایت یک روش روشن‌سازی و یکدست‌سازی پوست است که با تزریق مواد مغذی، روشن‌کننده و آبرسان به لایه میانی پوست انجام می‌شود.\n\n"

        "🌟 **مزایای مزووایت:**\n"
        "• روشن‌تر شدن پوست و کاهش تیرگی‌ها\n"
        "• کاهش لک‌های سطحی و عمقی\n"
        "• آبرسانی قوی و شفافیت پوست\n"
        "• یکدست شدن رنگ پوست\n"
        "• کاهش خستگی و کدری صورت\n"
        "• مناسب برای انواع پوست\n\n"

        "⚠️ **معایب و نکات مهم:**\n"
        "• احتمال قرمزی و التهاب خفیف تا چند ساعت\n"
        "• نیاز به چند جلسه برای نتیجه بهتر\n"
        "• در پوست‌های خیلی حساس ممکن است کمی سوزش ایجاد شود\n"
        "• باید توسط فرد متخصص انجام شود\n"
        "• مراقبت‌های بعد از کار بسیار مهم هستند\n"
    )

    bot.send_message(chat_id, text)

# -----------------------------
# 💆‍♀️ مراقبت‌های قبل و بعد مزووایت
# -----------------------------
def send_care_info(chat_id):
    text = (
        "💆‍♀️ **مراقبت‌های قبل از مزووایت:**\n"
        "• نوشیدن آب کافی از ۲۴ ساعت قبل 💧\n"
        "• عدم مصرف الکل و دخانیات 🚫\n"
        "• شست‌وشوی ملایم صورت قبل از مراجعه 🧼\n"
        "• عدم استفاده از کرم‌های سنگین یا لایه‌بردار ❌\n"
        "• اگر پوست خیلی حساس دارید، اطلاع دهید 🌸\n\n"

        "💖 **مراقبت‌های بعد از مزووایت:**\n"
        "• عدم شست‌وشوی صورت تا ۶–۸ ساعت 🚿❌\n"
        "• استفاده از کرم ترمیم‌کننده طبق دستور متخصص 🧴\n"
        "• پرهیز از آفتاب مستقیم تا ۴۸ ساعت ☀️❌\n"
        "• عدم استفاده از لایه‌بردار، اسکراب یا کرم‌های قوی تا ۳ روز ❌\n"
        "• نوشیدن آب کافی برای آبرسانی بهتر 💧\n"
        "• عدم انجام ورزش سنگین تا ۲۴ ساعت 🏃‍♀️❌\n"
        "• اگر قرمزی یا التهاب داشتید، طبیعی است و طی چند ساعت رفع می‌شود 🌿\n\n"

        "✨ رعایت این نکات باعث می‌شود نتیجه مزووایت خیلی بهتر و ماندگارتر باشد."
    )

    bot.send_message(chat_id, text)

# -----------------------------
# 📝 ثبت نوبت
# -----------------------------
def get_name(message):
    user_data[message.chat.id] = {}
    user_data[message.chat.id]["name"] = message.text

    bot.send_message(message.chat.id, "📞 شماره تماس را وارد کنید:")
    bot.register_next_step_handler(message, get_phone)

def get_phone(message):
    user_data[message.chat.id]["phone"] = message.text

    bot.send_message(message.chat.id, "📅 تاریخ مورد نظر را وارد کنید:")
    bot.register_next_step_handler(message, get_date)

def get_date(message):
    user_data[message.chat.id]["date"] = message.text

    info = user_data[message.chat.id]

    bot.send_message(
        message.chat.id,
        "✅ نوبت شما با موفقیت ثبت شد 🌸\n"
        "مدیر به‌زودی با شما تماس خواهد گرفت 💕"
    )

    bot.send_message(
        ADMIN_ID,
        f"📥 نوبت جدید:\n\n"
        f"👤 نام: {info['name']}\n"
        f"📞 شماره: {info['phone']}\n"
        f"📅 تاریخ: {info['date']}"
    )

# -----------------------------
# 📸 دریافت عکس صورت (اختیاری)
# -----------------------------
@bot.message_handler(content_types=['photo'])
def handle_optional_photo(message):
    try:
        file_id = message.photo[-1].file_id

        bot.send_photo(
            ADMIN_ID,
            file_id,
            caption=f"📸 عکس صورت مشتری\n\n🆔 User ID: {message.chat.id}"
        )

        bot.reply_to(message, "🌸 عکس صورت شما با موفقیت دریافت شد 💖")

    except Exception as e:
        bot.reply_to(message, "⚠️ ارسال عکس با خطا مواجه شد.")
        print("PHOTO ERROR:", e)

# -----------------------------
# 🤖 پاسخ‌دهی هوشمند با Gemini
# -----------------------------
@bot.message_handler(func=lambda m: True)
def ai_answer(message):
    user_text = message.text
    answer = ask_gemini(user_text)
    bot.reply_to(message, f"🤖 پاسخ هوش مصنوعی:\n\n{answer}")

# -----------------------------
# ▶️ اجرا
# -----------------------------
bot.infinity_polling()