import telebot
from telebot import types

TOKEN = "8834409229:AAGRsS9_rzgdtg8JxLQ2aqSpyVN3i0HISV0"
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 8070693669   # آیدی مدیر


bot = telebot.TeleBot(TOKEN)

# ------------------ شروع ربات ------------------

@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = "به ربلت خدمات مزووایت رخساره خانوم 🥰 خوش اومدی"

    try:
        photos = bot.get_user_profile_photos(bot.get_me().id)

        if photos.total_count > 0:
            file_id = photos.photos[0][0].file_id
            bot.send_photo(message.chat.id, file_id, caption=welcome_text)
        else:
            bot.send_message(message.chat.id, welcome_text)

    except:
        bot.send_message(message.chat.id, welcome_text)

    main_menu(message.chat.id)

# ------------------ منوی اصلی ------------------

def main_menu(chat_id):
    markup = types.InlineKeyboardMarkup()

    btn1 = types.InlineKeyboardButton("🔵 ثبت مشخصات", callback_data="reg")
    btn2 = types.InlineKeyboardButton("🟢 ارسال عکس صورت (اختیاری)", callback_data="photo")
    btn3 = types.InlineKeyboardButton("🟣 خدمات مزووایت", callback_data="services")
    btn4 = types.InlineKeyboardButton("🟠 درباره مزووایت", callback_data="about")

    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    markup.add(btn4)

    bot.send_message(chat_id, "لطفاً یکی از گزینه‌ها را انتخاب کن:", reply_markup=markup)

# ------------------ هندلر دکمه‌ها ------------------

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "reg":
        ask_name(call.message)

    elif call.data == "photo":
        bot.send_message(call.message.chat.id,
                         "اگر دوست داری، عکس صورتت رو ارسال کن 🌸\n(این بخش کاملاً اختیاری هست)")

    elif call.data == "services":
        show_services(call.message)

    elif call.data == "about":
        show_about(call.message)

    elif call.data == "back":
        main_menu(call.message.chat.id)

# ------------------ ثبت مشخصات ------------------

def ask_name(message):
    msg = bot.send_message(message.chat.id, "نام و نام خانوادگی‌ت رو وارد کن:")
    bot.register_next_step_handler(msg, get_name)

def get_name(message):
    name = message.text
    msg = bot.send_message(message.chat.id, "شماره تماس‌ت رو وارد کن:")
    bot.register_next_step_handler(msg, lambda m: save_info(m, name))

def save_info(message, name):
    phone = message.text
    bot.send_message(message.chat.id, "اطلاعاتت ثبت شد 🌸")
    bot.send_message(ADMIN_ID, f"ثبت مشخصات جدید:\nنام: {name}\nشماره: {phone}")
    main_menu(message.chat.id)

# ------------------ ارسال عکس صورت (اختیاری) ------------------

@bot.message_handler(content_types=['photo'])
def forward_photo(message):
    bot.send_message(message.chat.id, "عکس دریافت شد و برای مدیر ارسال شد 🌸")
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    main_menu(message.chat.id)

# ------------------ خدمات مزووایت ------------------

def show_services(message):
    text = (
        "✨ خدمات مزووایت:\n"
        "- روشن‌سازی پوست\n"
        "- کاهش لک و تیرگی\n"
        "- آبرسانی عمیق\n"
        "- یکدست‌سازی رنگ پوست\n"
    )
    back_button(message.chat.id, text)

# ------------------ درباره مزووایت ------------------

def show_about(message):
    text = (
        "مزووایت یک روش درمانی برای روشن‌سازی و شفافیت پوست هست.\n"
        "با تزریق مواد مغذی و روشن‌کننده، پوست یکدست‌تر و شفاف‌تر میشه."
    )
    back_button(message.chat.id, text)

# ------------------ دکمه بازگشت ------------------

def back_button(chat_id, text):
    markup = types.InlineKeyboardMarkup()
    back = types.InlineKeyboardButton("⬅️ بازگشت به منوی اصلی", callback_data="back")
    markup.add(back)
    bot.send_message(chat_id, text, reply_markup=markup)

# ------------------ اجرا ------------------

bot.infinity_polling()
