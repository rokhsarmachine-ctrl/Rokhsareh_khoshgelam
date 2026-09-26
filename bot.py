import telebot
from telebot import types
import requests

TOKEN = "8557198522:AAEsN08N6TNy_NaBX9vZVVitnQUZYCs8MSs"
ADMIN_ID = 8070693669
AI_API_KEY = "YOUR_COPILOT_AI_KEY"

bot = telebot.TeleBot(TOKEN)

# ---------------- AI ANALYSIS ----------------

def analyze_face(image_bytes):
    url = "https://api.copilot.microsoft.com/vision/analyze"
    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/octet-stream"
    }

    response = requests.post(url, headers=headers, data=image_bytes)
    result = response.json()

    skin_type = result.get("skin_type", "نامشخص")
    issues = result.get("issues", [])
    suggestion = result.get("suggestion", "پیشنهاد درمان یافت نشد")

    return skin_type, issues, suggestion

# ---------------- START ----------------

@bot.message_handler(commands=['start'])
def start(message):

    # ارسال لوگو
    try:
        logo = open("logo.jpg", "rb")
        bot.send_photo(message.chat.id, logo)
    except:
        bot.send_message(message.chat.id, "⚠️ لوگو پیدا نشد، فایل logo.jpg را کنار ربات قرار بده.")

    # پیام خوش‌آمدگویی
    bot.send_message(
        message.chat.id,
        "به ربات خدمات مزووایت رخساره خانوم 🥰 خوش اومدی\n"
        "برای شروع، یکی از گزینه‌های زیر رو انتخاب کن."
    )

    # دکمه‌های شیشه‌ای
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("🔍 تحلیل پوست با هوش مصنوعی", callback_data="ai")
    btn2 = types.InlineKeyboardButton("🗓 ثبت نوبت", callback_data="reserve")
    btn3 = types.InlineKeyboardButton("✨ مزووایت چیست؟", callback_data="info")
    btn4 = types.InlineKeyboardButton("📞 ارتباط با رخساره خانوم", url="https://t.me/Rokhsareh_Hanum")
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    markup.add(btn4)

    bot.send_message(message.chat.id, "منوی اصلی:", reply_markup=markup)

# ---------------- INLINE BUTTON HANDLER ----------------

user_state = {}

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):

    if call.data == "ai":
        bot.send_message(
            call.message.chat.id,
            "لطفاً یک عکس واضح از صورتت ارسال کن تا هوش مصنوعی تحلیل کنه 🌼"
        )

    elif call.data == "info":
        bot.send_message(
            call.message.chat.id,
            "مزووایت یک روش روشن‌سازی و یکدست‌سازی پوست هست که با مواد مخصوص انجام میشه ✨"
        )

    elif call.data == "reserve":
        user_state[call.message.chat.id] = {"step": "name"}
        bot.send_message(call.message.chat.id, "لطفاً نام و نام خانوادگی خود را وارد کنید:")

# ---------------- RESERVATION SYSTEM ----------------

@bot.message_handler(func=lambda m: m.chat.id in user_state)
def reservation_handler(message):

    state = user_state[message.chat.id]

    if state["step"] == "name":
        state["name"] = message.text
        state["step"] = "phone"
        bot.send_message(message.chat.id, "شماره تماس خود را وارد کنید:")

    elif state["step"] == "phone":
        state["phone"] = message.text
        state["step"] = "date"
        bot.send_message(message.chat.id, "تاریخ مورد نظر برای نوبت را وارد کنید (مثال: 1403/08/12):")

    elif state["step"] == "date":
        state["date"] = message.text
        state["step"] = "done"

        # پیام تایید برای کاربر
        bot.send_message(
            message.chat.id,
            f"نوبت شما با موفقیت ثبت شد 🌸\n\n"
            f"👤 نام: {state['name']}\n"
            f"📞 شماره: {state['phone']}\n"
            f"🗓 تاریخ: {state['date']}\n\n"
            f"رخساره خانوم به زودی با شما تماس می‌گیرند 💖"
        )

        # ارسال به مدیر
        bot.send_message(
            ADMIN_ID,
            f"📥 نوبت جدید ثبت شد:\n"
            f"👤 نام: {state['name']}\n"
            f"📞 شماره: {state['phone']}\n"
            f"🗓 تاریخ: {state['date']}\n"
            f"آیدی: @{message.from_user.username}"
        )

        del user_state[message.chat.id]

# ---------------- PHOTO HANDLER ----------------

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded = bot.download_file(file_info.file_path)

    bot.send_message(message.chat.id, "در حال تحلیل عکس با هوش مصنوعی... 🌼")

    skin_type, issues, suggestion = analyze_face(downloaded)

    bot.send_message(
        message.chat.id,
        f"🔍 نتیجه تحلیل پوست:\n"
        f"• نوع پوست: {skin_type}\n"
        f"• مشکلات: {', '.join(issues)}\n\n"
        f"✨ پیشنهاد درمان:\n{suggestion}"
    )

    bot.send_message(
        ADMIN_ID,
        f"📥 مراجعه‌کننده جدید:\n"
        f"نام: {message.from_user.first_name}\n"
        f"آیدی: @{message.from_user.username}\n"
        f"نوع پوست: {skin_type}\n"
        f"مشکلات: {', '.join(issues)}\n"
        f"پیشنهاد درمان: {suggestion}"
    )

bot.infinity_polling()