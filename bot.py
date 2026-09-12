import os
import telebot
from telebot import types

TOKEN ="8834409229:AAGRsS9_rzgdtg8JxLQ2aqSpyVN3i0HISV0"
bot = telebot.TeleBot(TOKEN)

# -------------------------
# منوی اصلی
# -------------------------
def main_menu():
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu.add("معرفی ماشین CNC")
    return menu

# -------------------------
# منوی معرفی CNC
# -------------------------
def cnc_menu():
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu.add("تراش CNC", "فرز CNC")
    menu.add("بازگشت")
    return menu

# -------------------------
# شروع ربات
# -------------------------
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "سلام وحید جان! به ربات معرفی ماشین CNC خوش اومدی 🌸",
        reply_markup=main_menu()
    )

# -------------------------
# هندل پیام‌ها
# -------------------------
@bot.message_handler(func=lambda m: True)
def menu_handler(message):

    # --- منوی اصلی ---
    if message.text == "معرفی ماشین CNC":
        bot.send_message(
            message.chat.id,
            "کدوم بخش رو می‌خوای ببینی؟",
            reply_markup=cnc_menu()
        )

    # --- تراش CNC ---
    elif message.text == "تراش CNC":
        bot.send_message(
            message.chat.id,
            "🔧 **معرفی تراش CNC**\n\n"
            "تراش CNC برای ساخت قطعات گرد، شفت‌ها، بوش‌ها و قطعات دقیق استفاده می‌شود.\n"
            "مزایا:\n"
            "- دقت بالا\n"
            "- سرعت تولید زیاد\n"
            "- مناسب برای برنج، آلومینیوم، فولاد\n"
        )

    # --- فرز CNC ---
    elif message.text == "فرز CNC":
        bot.send_message(
            message.chat.id,
            "🛠 **معرفی فرز CNC**\n\n"
            "فرز CNC برای ساخت قطعات تخت، شیارها، سوراخ‌کاری و مدل‌سازی سه‌بعدی استفاده می‌شود.\n"
            "مزایا:\n"
            "- قابلیت ساخت قطعات پیچیده\n"
            "- مناسب برای قالب‌سازی\n"
            "- دقت بالا در محورهای X,Y,Z\n"
        )

    # --- بازگشت ---
    elif message.text == "بازگشت":
        bot.send_message(
            message.chat.id,
            "به منوی اصلی برگشتی 🌸",
            reply_markup=main_menu()
        )

    else:
        bot.send_message(
            message.chat.id,
            "لطفاً از منوی زیر انتخاب کن:",
            reply_markup=main_menu()
        )

# -------------------------
# اجرای ربات
# -------------------------
bot.polling()
