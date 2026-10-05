import telebot
from telebot import types
import google.generativeai as genai
from groq import Groq
import os

# -----------------------------
# ⚙️ تنظیمات ربات
# -----------------------------
BOT_TOKEN = "8860048564:AAFJLbLpblSRBfImGzbBGgw1PI7izGUZvNk"
ADMIN_ID = 8070693669

# کلیدهای API از Railway
GEMINI_KEY = os.getenv("GEMINI_KEY")
GROQ_KEY = os.getenv("GROQ_KEY")

if not GEMINI_KEY:
    raise ValueError("❌ خطا: متغیر GEMINI_KEY در Railway تعریف نشده است!")

if not GROQ_KEY:
    raise ValueError("❌ خطا: متغیر GROQ_KEY در Railway تعریف نشده است!")

bot = telebot.TeleBot(BOT_TOKEN)

# -----------------------------
# 🤖 تنظیمات Gemini
# -----------------------------
genai.configure(api_key=GEMINI_KEY)
gemini_model = genai.GenerativeModel("gemini-3.5-flash")

# -----------------------------
# 🤖 تنظیمات Groq
# -----------------------------
groq_client = Groq(api_key=GROQ_KEY)

# -----------------------------
# 🔄 تابع هوش مصنوعی با سوئیچ مخفی
# -----------------------------
def ai_answer_engine(prompt):
    """
    اول تلاش با Gemini
    اگر خطا داد → سوئیچ مخفی به Groq
    هیچ‌جا مشخص نمی‌شود کدام مدل پاسخ داده
    """

    try:
        response = gemini_model.generate_content(prompt)
        return response.text

    except:
        try:
            groq_response = groq_client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            return groq_response.choices[0].message.content

        except:
            return "عزیزم یه مشکلی کوچولو پیش اومد… دوباره امتحان کن 🌸"


# -----------------------------
# دیتابیس ساده
# -----------------------------
user_phone_db = {}
ai_first_message_sent = {}

# -----------------------------
# 🚀 شروع ربات
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

    markup.add(types.InlineKeyboardButton("🌸 ❓ پرسیدن سوال", callback_data="ask"))
    markup.add(types.InlineKeyboardButton("🌸 🗓 ثبت نوبت", callback_data="reserve"))
    markup.add(types.InlineKeyboardButton("🌸 📸 ارسال عکس صورت", callback_data="photo"))
    markup.add(types.InlineKeyboardButton("🌸 ✨ درباره مزووایت", callback_data="mezowhite"))
    markup.add(types.InlineKeyboardButton("🌸 💆‍♀️ مراقبت‌های قبل و بعد", callback_data="care"))

    bot.send_message(chat_id, "عزیزم یکی از گزینه‌های زیر رو انتخاب کن 🌸", reply_markup=markup)

# -----------------------------
# 🎛 هندل دکمه‌ها
# -----------------------------
@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    if call.data == "ask":
        bot.send_message(call.message.chat.id, "❓ عزیزم سوالت رو بپرس:")

    elif call.data == "reserve":
        bot.send_message(call.message.chat.id, "👤 اسم خوشگلت رو بگو عزیزم:")
        bot.register_next_step_handler(call.message, get_name)

    elif call.data == "photo":
        bot.send_message(call.message.chat.id, "📸 قربونت، عکس صورتت رو بفرست:")

    elif call.data == "mezowhite":
        send_mezowhite_info(call.message.chat.id)

    elif call.data == "care":
        send_care_info(call.message.chat.id)

# -----------------------------
# ✨ درباره مزووایت
# -----------------------------
def send_mezowhite_info(chat_id):
    bot.send_message(chat_id,
        "✨ عزیزم مزووایت یه روش فوق‌العاده برای روشن‌سازی و یکدست‌سازی پوستته 🌸\n"
        "با تزریق مواد مغذی، پوستت مثل گل شکوفه می‌کنه 💖✨\n\n"
        "🌟 مزایا:\n"
        "• روشن‌تر شدن پوست\n"
        "• کاهش لک‌ها\n"
        "• آبرسانی قوی\n"
        "• یکدست شدن رنگ پوست\n\n"
        "⚠️ معایب کوچولو:\n"
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
        "💆‍♀️ عزیزم قبل از مزووایت:\n"
        "• آب کافی بخور 💧\n"
        "• الکل نخور 🚫\n"
        "• صورتت رو ملایم بشور 🧼\n\n"
        "💖 بعد از مزووایت:\n"
        "• تا ۸ ساعت صورتت رو نشور 🚿❌\n"
        "• کرم ترمیم‌کننده بزن 🧴\n"
        "• از آفتاب دوری کن ☀️❌\n"
        "• لایه‌بردار نزن تا ۳ روز ❌\n"
        "• آب زیاد بخور 💧"
    )

# -----------------------------
# 📝 ثبت نوبت
# -----------------------------
def get_name(message):
    user_data = {"name": message.text}

    bot.send_message(message.chat.id, "📞 عزیزم شماره تماس رو بفرست:")
    bot.register_next_step_handler(message, lambda msg: get_phone(msg, user_data))

def get_phone(message, user_data):
    user_data["phone"] = message.text
    user_phone_db[message.chat.id] = message.text

    bot.send_message(message.chat.id, "📅 تاریخ مورد نظرت رو بگو عزیزم:")
    bot.register_next_step_handler(message, lambda msg: get_date(msg, user_data))

def get_date(message, user_data):
    user_data["date"] = message.text

    bot.send_message(message.chat.id, "✅ نوبتت با موفقیت ثبت شد عزیزم 🌸")

    bot.send_message(
        ADMIN_ID,
        f"📥 نوبت جدید:\n"
        f"👤 نام: {user_data['name']}\n"
        f"📞 شماره: {user_data['phone']}\n"
        f"📅 تاریخ: {user_data['date']}"
    )

# -----------------------------
# 📸 دریافت عکس صورت
# -----------------------------
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        username = message.from_user.username
        username_text = f"🔹 یوزرنیم: @{username}" if username else "🔹 یوزرنیم: ندارد"

        phone = user_phone_db.get(message.chat.id, None)
        phone_text = f"🔹 شماره: {phone}" if phone else "🔹 شماره: ثبت نشده"

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

        bot.reply_to(message, "🌸 قربونت، عکس صورتت رسید 💖")

    except Exception as e:
        bot.reply_to(message, f"⚠️ عزیزم یه مشکلی پیش اومد:\n{e}")

# -----------------------------
# 🤖 پاسخ‌دهی هوشمند
# -----------------------------
@bot.message_handler(content_types=['text'])
def ai_answer(message):

    chat_id = message.chat.id
    text = message.text.strip().lower()

    intro_keywords = [
        "معرفی", "خودت رو معرفی کن", "تو کی هستی", "کی هستی",
        "هوش مصنوعی کیه", "ربات کیه", "معرفی کن", "خودتو معرفی کن"
    ]

    if any(key in text for key in intro_keywords):
        intro = (
            "سلام زیبای من 🌸\n"
            "من هوش مصنوعی ربات خدمات مزووایت رخساره خانوم 🥰 هستم.\n"
            "با عشق کنارتم عزیزم 💖\n\n"
        )
        bot.reply_to(message, intro)
        return

    if not ai_first_message_sent.get(chat_id, False):
        intro = (
            "سلام زیبای من 🌸\n"
            "من هوش مصنوعی ربات خدمات مزووایت رخساره خانوم 🥰 هستم، "
        )
        ai_first_message_sent[chat_id] = True
    else:
        intro = ""

    reply = ai_answer_engine(message.text)
    bot.reply_to(message, intro + reply)

# -----------------------------
# ▶️ اجرا
# -----------------------------
bot.infinity_polling()