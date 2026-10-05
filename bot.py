import telebot
from telebot import types
import google.generativeai as genai
import os

-----------------------------

⚙️ تنظیمات ربات

-----------------------------
BOT_TOKEN = "8860048564:AAFJLbLpblSRBfImGzbBGgw1PI7izGUZvNk"
ADMIN_ID = 8070693669

❗ کلید Gemini از Variable خوانده می‌شود
GEMINIKEY = os.getenv("GEMINIKEY")
if not GEMINI_KEY:
    raise ValueError("❌ خطا: متغیر GEMINI_KEY در Railway تعریف نشده است!")

bot = telebot.TeleBot(BOT_TOKEN)

-----------------------------

🤖 تنظیمات Gemini

-----------------------------
genai.configure(apikey=GEMINIKEY)
model = genai.GenerativeModel("gemini-3.5-flash")

def ask_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ خطا در Gemini:\n{e}"

-----------------------------

دیتابیس ساده

-----------------------------
userphonedb = {}
aifirstmessage_sent = {}

-----------------------------

🚀 شروع ربات

-----------------------------
@bot.message_handler(commands=['start'])
def start(message):

    welcome_text = (
        "سلام عزیزم 🌸\n"
        "به ربات خدمات مزووایت رخساره خانوم خوشگل🥰 خوش اومدی ✨"
    )

    try:
        botinfo = bot.getme()
        photos = bot.getuserprofilephotos(botinfo.id)

        if photos.total_count > 0:
            fileid = photos.photos[0][0].fileid
            bot.sendphoto(message.chat.id, fileid, caption=welcome_text)
        else:
            bot.sendmessage(message.chat.id, welcometext)

    except:
        bot.sendmessage(message.chat.id, welcometext)

    main_menu(message.chat.id)

-----------------------------

🌸 منوی اصلی

-----------------------------
def mainmenu(chatid):
    markup = types.InlineKeyboardMarkup()

    markup.add(types.InlineKeyboardButton("🌸 ❓ پرسیدن سوال - هوش مصنوعی", callback_data="ask"))
    markup.add(types.InlineKeyboardButton("🌸 🗓 ثبت نوبت", callback_data="reserve"))
    markup.add(types.InlineKeyboardButton("🌸 📸 ارسال عکس صورت", callback_data="photo"))
    markup.add(types.InlineKeyboardButton("🌸 ✨ درباره مزووایت", callback_data="mezowhite"))
    markup.add(types.InlineKeyboardButton("🌸 💆‍♀️ مراقبت‌های قبل و بعد", callback_data="care"))

    bot.sendmessage(chatid, "لطفاً یکی از گزینه‌های زیر رو انتخاب کن:", reply_markup=markup)

-----------------------------

🎛 هندل دکمه‌ها

-----------------------------
@bot.callbackqueryhandler(func=lambda call: True)
def callback(call):

    if call.data == "ask":
        bot.send_message(call.message.chat.id,
            " سؤال خود را بپرس عزیزم❓️"
        )

    elif call.data == "reserve":
        bot.send_message(call.message.chat.id, "👤 لطفاً نام خود را وارد کنید:")
        bot.registernextstephandler(call.message, getname)

    elif call.data == "photo":
        bot.send_message(call.message.chat.id, "📸 لطفاً عکس صورت خود را ارسال کنید:")

    elif call.data == "mezowhite":
        sendmezowhiteinfo(call.message.chat.id)

    elif call.data == "care":
        sendcareinfo(call.message.chat.id)

-----------------------------

✨ درباره مزووایت

-----------------------------
def sendmezowhiteinfo(chat_id):
    bot.sendmessage(chatid,
        "✨ مزووایت چیست؟\n"
        "روشی برای روشن‌سازی و یکدست‌سازی پوست با تزریق مواد مغذی.\n\n"
        "🌟 مزایا:\n"
        "• روشن‌تر شدن پوست\n"
        "• کاهش لک‌ها\n"
        "• آبرسانی قوی\n"
        "• یکدست شدن رنگ پوست\n\n"
        "⚠️ معایب:\n"
        "• قرمزی چند ساعته\n"
        "• نیاز به چند جلسه\n"
        "• احتمال سوزش\n"
        "• نیاز به متخصص حرفه‌ای"
    )

-----------------------------

💆‍♀️ مراقبت‌های قبل و بعد

-----------------------------
def sendcareinfo(chat_id):
    bot.sendmessage(chatid,
        "💆‍♀️ قبل از مزووایت:\n"
        "• نوشیدن آب کافی 💧\n"
        "• عدم مصرف الکل 🚫\n"
        "• شست‌وشوی ملایم صورت 🧼\n\n"
        "💖 بعد از مزووایت:\n"
        "• عدم شست‌وشوی صورت تا ۸ ساعت 🚿❌\n"
        "• کرم ترمیم‌کننده 🧴\n"
        "• دوری از آفتاب ☀️❌\n"
        "• عدم لایه‌بردار تا ۳ روز ❌\n"
        "• نوشیدن آب 💧"
    )

-----------------------------

📝 ثبت نوبت

-----------------------------
def get_name(message):
    user_data = {"name": message.text}

    bot.send_message(message.chat.id, "📞 شماره تماس را وارد کنید:")
    bot.registernextstephandler(message, lambda msg: getphone(msg, user_data))

def getphone(message, userdata):
    user_data["phone"] = message.text
    userphonedb[message.chat.id] = message.text

    bot.send_message(message.chat.id, "📅 تاریخ مورد نظر را وارد کنید:")
    bot.registernextstephandler(message, lambda msg: getdate(msg, user_data))

def getdate(message, userdata):
    user_data["date"] = message.text

    bot.send_message(message.chat.id, "✅ نوبت شما ثبت شد 🌸")

    bot.send_message(
        ADMIN_ID,
        f"📥 نوبت جدید:\n"
        f"👤 نام: {user_data['name']}\n"
        f"📞 شماره: {user_data['phone']}\n"
        f"📅 تاریخ: {user_data['date']}"
    )

-----------------------------

📸 دریافت عکس صورت

-----------------------------
@bot.messagehandler(contenttypes=['photo'])
def handle_photo(message):
    try:
        fileid = message.photo[-1].fileid
        fileinfo = bot.getfile(file_id)
        downloadedfile = bot.downloadfile(fileinfo.filepath)

        username = message.from_user.username
        username_text = f"🔹 یوزرنیم: @{username}" if username else "🔹 یوزرنیم: ندارد"

        phone = userphonedb.get(message.chat.id, None)
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

        bot.reply_to(message, "🌸 عکس صورت شما با موفقیت دریافت شد 💖")

    except Exception as e:
        bot.reply_to(message, f"⚠️ خطا در دریافت عکس:\n{e}")

-----------------------------

🤖 پاسخ‌دهی هوشمند + معرفی دوباره در صورت درخواست

-----------------------------
@bot.messagehandler(contenttypes=['text'])
def ai_answer(message):

    chat_id = message.chat.id
    text = message.text.strip().lower()

    # لیست کلمات کلیدی معرفی دوباره
    intro_keywords = [
        "معرفی", "خودت رو معرفی کن", "تو کی هستی", "کی هستی",
        "هوش مصنوعی کیه", "ربات کیه", "معرفی کن", "خودتو معرفی کن"
    ]

    # اگر کاربر درخواست معرفی کرد → همیشه معرفی کن
    if any(key in text for key in intro_keywords):
        intro = (
            "سلام زیبا جوی عزیز 🌸\n"
            "من هوش مصنوعی خدمات مزووایت ربات تلگرامی رخساره خانوم 🥰 هستم.\n"
            "در خدمتتم عزیزم 💖\n\n"
        )
        bot.reply_to(message, intro)
        return

    # معرفی فقط اولین بار
    if not aifirstmessagesent.get(chatid, False):
        intro = (
            "سلام زیبا جوی عزیز 🌸\n"
            "من هوش مصنوعی ربات تلگرامی خدمات مزووایت رخساره خانوم 🥰 هستم، "

        )
        aifirstmessagesent[chatid] = True
    else:
        intro = ""

    reply = ask_gemini(message.text)
    bot.reply_to(message, intro + reply)

-----------------------------

▶️ اجرا

-----------------------------
bot.infinity_polling()