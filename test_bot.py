from telegram import Bot

TOKEN = "8121555720:AAHOZ3WNi5H7N0lrNrK4dyCoY_wTiaFpGzU"

print("🔹 بدأ التحقق من التوكن...")

try:
    bot = Bot(token=TOKEN)
    me = bot.get_me()
    print("✅ التوكن صالح!")
    print(me)
except Exception as e:
    print("❌ خطأ:", e)

input("اضغط Enter للخروج...")
