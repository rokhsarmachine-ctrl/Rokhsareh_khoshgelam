import telebot
from telebot import types
import google.generativeai as genai
import os

# -----------------------------
# ⚙️ تنظیمات ربات
# -----------------------------
BOT_TOKEN = "8860048564:AAFJLbLpblSRBfImGzbBGgw1PI7izGUZvNk"
ADMIN_ID = 8070693669

# ❗ کلید Gemini از Variable خوانده می‌شود
GEMINI_KEY = os.getenv("GEMINI_KEY")

if not GEMINI_KEY:
    raise ValueError("❌ خطا: متغیر GEMINI_KEY در Railway تعریف نشده است!")

bot = telebot.TeleBot(BOT_TOKEN)

# -----------------------------
# 🤖 تنظیمات Gemini
# -----------------------------
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-3.5-flash")

def ask_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ خطا در Gemini:\n{e}"

# -----------------------------
# دیتابیس ساده برای ذخیره شماره‌ها
# -----------------------------
user_phone_db = {}   # {chat_id: phone_number}

# -----------------------------
# 🚀 شروع ربات + عکس پروفایل ربات
# -----------------------------
@bot.message_handler(commands=['start'])
def start(message):

    welcome_text = (
        "سلام عزیزم 🌸\n"
        "به ربات خدمات مزووایت رخساره خانوم خوشگل🥰 خوش اومدی ✨"
    )

    try:
        bot_info = bot.get_me()
        photos = bot.get_user_profile_photos(bot_info.id)

        if photos.total_count > 0:
            file_id = photos.photos[0][0].file_id
            bot.send_photo(message.chat.id, file_id, caption=welcome_text)
        else:
            bot.send_message(message.chat.id, welcome_text)

    except:
        bot.send_message(message.chat.id, welcome_text)

    main_menu(message.chat.id)

# -----------------------------
# 🌸 منوی اصلی
# -----------------------------
def main_menu(chat_id):
    markup = types.InlineKeyboardMarkup()

    markup.add(types.InlineKeyboardButton("🌸 ❓ پرسیدن سوال - هوش مصنوعی", callback_data="ask"))
    markup.add(types.InlineKeyboardButton("🌸 🗓 ثبت نوبت", callback_data="reserve"))
    markup.add(types.InlineKeyboardButton("🌸 📸 ارسال عکس صورت", callback_data="photo"))
    markup.add(types.InlineKeyboardButton("🌸 ✨ درباره مزووایت", callback_data="mezowhite"))
    markup.add(types.InlineKeyboardButton("🌸 💆‍♀️ مراقبت‌های قبل و بعد", callback_data="care"))

    bot.send_message(chat_id, "لطفاً یکی از گزینه‌های زیر رو انتخاب کن:", reply_markup=markup)

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
# ✨ درباره مزووایت
# -----------------------------
def send_mezowhite_info(chat_id):
    bot.send_message(chat_id,
        "✨ **مزووایت چیست؟**\n"
        "روشی برای روشن‌سازی و یکدست‌سازی پوست با تزریق مواد مغذی.\n\n"
        "🌟 **مزایا:**\n"
        "• روشن‌تر شدن پوست\n"
        "• کاهش لک‌ها\n"
        "• آبرسانی قوی\n"
        "• یکدست شدن رنگ پوست\n\n"
        "⚠️ **معایب:**\n"
        "• قرمزی چند ساعته\n"
        "• نیاز به چند جلسه\n"
        "• احتمال سوزش\n"
        "• نیاز به متخصص حرفه‌ای"
    )

# -----------------------------
# 💆‍♀️ مراقبت‌های قبل و بعد
# -----------------------------
def send_care_info(chat_id):
    bot.send_message(chat_id,
        "💆‍♀️ **قبل از مزووایت:**\n"
        "• نوشیدن آب کافی 💧\n"
        "• عدم مصرف الکل 🚫\n"
        "• شست‌وشوی ملایم صورت 🧼\n\n"
        "💖 **بعد از مزووایت:**\n"
        "• عدم شست‌وشوی صورت تا ۸ ساعت 🚿❌\n"
        "• کرم ترمیم‌کننده 🧴\n"
        "• دوری از آفتاب ☀️❌\n"
        "• عدم لایه‌بردار تا ۳ روز ❌\n"
        "• نوشیدن آب 💧"
    )

# -----------------------------
# 📝 ثبت نوبت
# -----------------------------
def get_name(message):
    user_data = {"name": message.text}

    bot.send_message(message.chat.id, "📞 شماره تماس را وارد کنید:")
    bot.register_next_step_handler(message, lambda msg: get_phone(msg, user_data))

def get_phone(message, user_data):
    user_data["phone"] = message.text

    # ذخیره شماره برای استفاده هنگام ارسال عکس
    user_phone_db[message.chat.id] = message.text

    bot.send_message(message.chat.id, "📅 تاریخ مورد نظر را وارد کنید:")
    bot.register_next_step_handler(message, lambda msg: get_date(msg, user_data))

def get_date(message, user_data):
    user_data["date"] = message.text

    bot.send_message(message.chat.id, "✅ نوبت شما ثبت شد 🌸")

    bot.send_message(
        ADMIN_ID,
        f"📥 نوبت جدید:\n"
        f"👤 نام: {user_data['name']}\n"
        f"📞 شماره: {user_data['phone']}\n"
        f"📅 تاریخ: {user_data['date']}"
    )

# -----------------------------
# 📸 دریافت عکس صورت (نسخه کامل + شماره + یوزرنیم)
# -----------------------------
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # یوزرنیم
        username = message.from_user.username
        username_text = f"🔹 یوزرنیم: @{username}" if username else "🔹 یوزرنیم: ندارد"

        # شماره تلفن از دیتابیس
        phone = user_phone_db.get(message.chat.id, None)
        phone_text = f"🔹 شماره: {phone}" if phone else "🔹 شماره: ثبت نشده"

        # ارسال به ادمین
        bot.send_photo(
            ADMIN_ID,
            downloaded_file,
            caption=(
                "📸 عکس صورت مشتری\n"
                f"🆔 آیدی: {message.chat.id}\n"
                f"{username_text}\n"
                f"{phone_text}"
            )
        )

        bot.reply_to(message, "🌸 عکس صورت شما با موفقیت دریافت شد 💖")

    except Exception as e:
        bot.reply_to(message, f"⚠️ خطا در دریافت عکس:\n{e}")

# -----------------------------
# 🤖 پاسخ‌دهی هوشمند با Gemini
# -----------------------------
@bot.message_handler(content_types=['text'])
def ai_answer(message):
    reply = ask_gemini(message.text)
    bot.reply_to(message, reply)

# -----------------------------
# ▶️ اجرا
# -----------------------------
bot.infinity_polling()