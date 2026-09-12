import telebot

TOKEN ="8834409229:AAGRsS9_rzgdtg8JxLQ2aqSpyVN3i0HISV0"
bot = telebot.TeleBot(TOKEN)

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,
                 "سلام عزیزم 🌸\nبه بخش ثبت سفارش مزووایت صورت خوش اومدی.\nلطفاً اسم کاملت رو بفرست.")

@bot.message_handler(func=lambda m: True)
def collect_info(message):
    chat_id = message.chat.id

    if chat_id not in user_data:
        user_data[chat_id] = {"name": message.text}
        bot.send_message(chat_id, "شماره تماس رو بفرست عزیزم 📱")
        return

    if "phone" not in user_data[chat_id]:
        user_data[chat_id]["phone"] = message.text
        bot.send_message(chat_id, "چه زمانی دوست داری نوبت مزووایت داشته باشی؟ (مثلاً: فردا ساعت ۵)")
        return

    if "time" not in user_data[chat_id]:
        user_data[chat_id]["time"] = message.text

        name = user_data[chat_id]["name"]
        phone = user_data[chat_id]["phone"]
        time = user_data[chat_id]["time"]

        bot.send_message(chat_id,
                         f"عالیه عزیزم 🌸\nثبت شد:\n"
                         f"نام: {name}\n"
                         f"شماره: {phone}\n"
                         f"زمان نوبت: {time}\n"
                         f"به زودی باهات تماس می‌گیریم ❤️")

        # ارسال اطلاعات به مدیر
        admin_id = 8070693669  # آیدی عددی مدیر
        bot.send_message(admin_id,
                         f"یک سفارش جدید مزووایت ثبت شد:\n"
                         f"نام: {name}\n"
                         f"شماره: {phone}\n"
                         f"زمان: {time}")

        user_data.pop(chat_id)

bot.polling()      
