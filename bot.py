import telebot
from telebot import types

TOKEN = "8834409229:AAGRsS9_rzgdtg8JxLQ2aqSpyVN3i0HISV0"
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 8070693669   # آیدی مدیر

# دیتای موقت کاربران
user_data = {}

# -----------------------------
# منوی اصلی
# -----------------------------
def main_menu():
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu.add("ثبت سفارش مزووایت")
    menu.add("معرفی خدمات مزووایت")
    return menu

# -----------------------------
# منوی معرفی خدمات مزووایت
# -----------------------------
def mesowhite_menu():
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu.add("مزایا مزووایت")
    menu.add("عوارض احتمالی")
    menu.add("مواد مورد استفاده")
    menu.add("بازگشت به منوی اصلی")
    return menu

# -----------------------------
# شروع ربات + نمایش لوگو
# -----------------------------
@bot.message_handler(commands=['start'])
def start(message):

    # ارسال لوگو
    try:
        photo = open("logo.jpg", "rb")
        bot.send_photo(message.chat.id, photo)
    
    # پیام خوش‌آمدگویی
    bot.send_message(
        message.chat.id,
        "سلام عزیزم 🌹\nبه ربات خدمات مزووایت رخساره خانوم 🥰 خوش اومدی.\nاز منوی زیر انتخاب کن:",
        reply_markup=main_menu()
    )

# -----------------------------
# معرفی خدمات
# -----------------------------
@bot.message_handler(func=lambda m: m.text == "معرفی خدمات مزووایت")
def show_mesowhite_menu(message):
    bot.send_message(
        message.chat.id,
        "کدوم بخش رو می‌خوای ببینی؟",
        reply_markup=mesowhite_menu()
    )

@bot.message_handler(func=lambda m: m.text == "مزایا مزووایت")
def benefits(message):
    bot.send_message(
        message.chat.id,
        "✨ مزایای مزووایت:\n"
        "- روشن شدن پوست\n"
        "- کاهش لک و تیرگی\n"
        "- آبرسانی عمیق\n"
        "- یکدست شدن رنگ پوست\n"
        "- شفافیت و درخشندگی"
    )

@bot.message_handler(func=lambda m: m.text == "عوارض احتمالی")
def side_effects(message):
    bot.send_message(
        message.chat.id,
        "⚠️ عوارض احتمالی مزووایت:\n"
        "- قرمزی موقت\n"
        "- حساسیت خفیف\n"
        "- خشکی پوست\n"
        "این موارد معمولاً کوتاه‌مدت هستند 🌸"
    )

@bot.message_handler(func=lambda m: m.text == "مواد مورد استفاده")
def materials(message):
    bot.send_message(
        message.chat.id,
        "🧴 مواد مورد استفاده:\n"
        "- ویتامین C\n"
        "- گلوتاتیون\n"
        "- کوجیک اسید\n"
        "- هیالورونیک اسید\n"
        "- آمینواسیدهای روشن‌کننده"
    )

@bot.message_handler(func=lambda m: m.text == "بازگشت به منوی اصلی")
def back_to_main(message):
    bot.send_message(
        message.chat.id,
        "به منوی اصلی برگشتی عزیزم 🌹",
        reply_markup=main_menu()
    )

# -----------------------------
# ثبت سفارش مزووایت
# -----------------------------
@bot.message_handler(func=lambda m: m.text == "ثبت سفارش مزووایت")
def register_start(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}
    bot.send_message(chat_id, "اسم کاملت رو بفرست عزیزم 🌸")

# -----------------------------
# مراحل ثبت سفارش (عکس اختیاری)
# -----------------------------
@bot.message_handler(content_types=['text', 'photo'])
def collect_info(message):
    chat_id = message.chat.id

    if chat_id not in user_data:
        return

    # مرحله ۱: نام
    if "name" not in user_data[chat_id]:
        user_data[chat_id]["name"] = message.text
        bot.send_message(chat_id, "شماره تماس رو بفرست عزیزم 📱")
        return

    # مرحله ۲: شماره تماس
    if "phone" not in user_data[chat_id]:
        user_data[chat_id]["phone"] = message.text
        bot.send_message(chat_id, "چه زمانی دوست داری نوبت مزووایت داشته باشی؟ (مثلاً: فردا ساعت ۵)")
        return

    # مرحله ۳: زمان نوبت
    if "time" not in user_data[chat_id]:
        user_data[chat_id]["time"] = message.text
        bot.send_message(
            chat_id,
            "اگر دوست داری، یک عکس از صورتت بفرست تا بررسی کنم ه🌹\n\n"
            "اگر عکس نمی‌خوای بفرستی، فقط بنویس: «تمام»"
        )
        return

    # مرحله ۴: عکس اختیاری
    if "photo" not in user_data[chat_id]:

        # اگر عکس فرستاد
        if message.content_type == "photo":
            user_data[chat_id]["photo"] = message.photo[-1].file_id

        # اگر نوشت "تمام"
        elif message.text.strip() == "تمام":
            user_data[chat_id]["photo"] = None

        else:
            bot.send_message(chat_id, "اگر عکس نمی‌خوای بفرستی، فقط بنویس: «تمام» 🌹")
            return

        # ارسال اطلاعات به مدیر
        name = user_data[chat_id]["name"]
        phone = user_data[chat_id]["phone"]
        time = user_data[chat_id]["time"]

        bot.send_message(
            ADMIN_ID,
            f"📩 یک سفارش جدید ثبت شد:\n\n"
            f"👤 نام: {name}\n"
            f"📱 شماره: {phone}\n"
            f"⏰ زمان نوبت: {time}"
        )

        # اگر عکس وجود داشت، ارسال شود
        if user_data[chat_id]["photo"] is not None:
            bot.send_photo(ADMIN_ID, user_data[chat_id]["photo"])

        bot.send_message(chat_id, "عالیه عزیزم🌹 سفارش ثبت شد. به زودی باهات تماس می‌گیریم😃")

        user_data.pop(chat_id)
        return

# -----------------------------
# اجرای ربات
# -----------------------------
bot.polling()
