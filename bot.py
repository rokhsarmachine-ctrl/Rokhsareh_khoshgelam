
import telebot
from telebot import types

TOKEN = "8834409229:AAGRsS9_rzgdtg8JxLQ2aqSpyVN3i0HISV0"
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 8070693669   

    
# شروع ربات 

@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = "به ربات خدمات مزووایت رخساره خانوم خوشگل🥰 خوش اومدی"

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

# منوی اصلی 

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

# هندلر دکمه‌ها

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    data = call.data

    if data == "reg":
        ask_name(call.message)

    elif data == "photo":
        bot.send_message(call.message.chat.id,
                         "اگر دوست داری، عکس صورتت رو ارسال کن 🌸\n(این بخش کاملاً اختیاری هست)")

    elif data == "services":
        services_menu(call.message)

    elif data == "about":
        show_about(call.message)

    elif data == "benefits":
        show_benefits(call.message)

    elif data == "side_effects":
        show_side_effects(call.message)

    elif data == "care":
        show_care(call.message)

    elif data == "back":
        main_menu(call.message.chat.id)

# منوی خدمات مزووایت

def services_menu(message):
    markup = types.InlineKeyboardMarkup()

    btn1 = types.InlineKeyboardButton("✨ مزایا مزووایت", callback_data="benefits")
    btn2 = types.InlineKeyboardButton("⚠️ معایب / عوارض احتمالی", callback_data="side_effects")
    btn3 = types.InlineKeyboardButton("💆‍♀️ مراقبت‌های لازم بعد از مزووایت", callback_data="care")
    btn4 = types.InlineKeyboardButton("⬅️ بازگشت", callback_data="back")

    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    markup.add(btn4)

    bot.send_message(message.chat.id, "بخش مورد نظرت رو انتخاب کن:", reply_markup=markup)

#  مزایا

def show_benefits(message):
    text = (
        "✨ مزایا مزووایت:\n"
        "- روشن‌سازی و شفافیت پوست\n"
        "- کاهش لک، تیرگی و کدری\n"
        "- آبرسانی عمیق و رفع خشکی\n"
        "- یکدست شدن رنگ پوست\n"
        "- تحریک کلاژن‌سازی\n"
        "- افزایش درخشندگی و لطافت پوست\n"
    )
    back_button(message.chat.id, text)

# معایب

def show_side_effects(message):
    text = (
        "⚠️ معایب و عوارض احتمالی مزووایت:\n"
        "- قرمزی و التهاب خفیف تا چند ساعت\n"
        "- خشکی یا پوسته‌پوسته شدن موقت\n"
        "- احتمال حساسیت در پوست‌های خیلی حساس\n"
        "- نیاز به چند جلسه برای نتیجه کامل\n"
        "- ممنوعیت برای افراد باردار یا دارای بیماری پوستی فعال\n"
    )
    back_button(message.chat.id, text)

#  مراقبت‌های لازم

def show_care(message):
    text = (
        "💆‍♀️ مراقبت‌های لازم بعد از مزووایت:\n"
        "- تا ۲۴ ساعت شست‌وشوی صورت نداشته باش\n"
        "- از آفتاب مستقیم دوری کن و ضدآفتاب بزن\n"
        "- از کرم‌های سنگین یا لایه‌بردار استفاده نکن\n"
        "- تا ۲۴ ساعت آرایش نکن\n"
        "- آب زیاد بنوش تا آبرسانی پوست بهتر انجام بشه\n"
        "- اگر قرمزی داشتی، کمپرس سرد کمک می‌کنه\n"
    )
    back_button(message.chat.id, text)

#  درباره مزووایت

def show_about(message):
    text = (
        "مزووایت یک روش درمانی برای روشن‌سازی و شفافیت پوست هست.\n"
        "با تزریق مواد مغذی و روشن‌کننده، پوست یکدست‌تر و شفاف‌تر میشه."
    )
    back_button(message.chat.id, text)

# ثبت مشخصات

def ask_name(message):
    msg = bot.send_message(message.chat.id, "نام و نام خانوادگیت رو وارد کن:")
    bot.register_next_step_handler(msg, get_name)

def get_name(message):
    name = message.text.strip()
    msg = bot.send_message(message.chat.id, "شماره تماست رو وارد کن:")
    bot.register_next_step_handler(msg, lambda m: get_time(m, name))

def get_time(message, name):
    phone = message.text.strip()
    msg = bot.send_message(message.chat.id, "چه ساعتی دوست داری درخواستت ثبت بشه؟ (مثلاً: ساعت ۷ عصر)")
    bot.register_next_step_handler(msg, lambda m: save_info(m, name, phone))

def save_info(message, name, phone):
    time = message.text.strip()

    bot.send_message(message.chat.id, "اطلاعاتت ثبت شد🌹")

    bot.send_message(
        ADMIN_ID,
        f"ثبت درخواست جدید:\n"
        f"نام: {name}\n"
        f"شماره: {phone}\n"
        f"ساعت دلخواه: {time}"
    )

    main_menu(message.chat.id)

#  ارسال عکس صورت (اختیاری)

@bot.message_handler(content_types=['photo'])
def forward_photo(message):
    bot.send_message(message.chat.id, "عکس دریافت شد و برای مدیر ارسال شد 🌹")
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    main_menu(message.chat.id)

#  دکمه بازگشت

def back_button(chat_id, text):
    markup = types.InlineKeyboardMarkup()
    back = types.InlineKeyboardButton("⬅️ بازگشت به منوی اصلی", callback_data="back")
    markup.add(back)
    bot.send_message(chat_id, text, reply_markup=markup)

# اجرا

bot.infinity_polling()