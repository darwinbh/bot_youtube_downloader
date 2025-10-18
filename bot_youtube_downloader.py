import os
from flask import Flask
from pytube import YouTube
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# 🧩 ضع هنا التوكن الخاص ببوتك
TOKEN = ""

app = Flask(__name__)

# دالة تحميل الفيديو من يوتيوب
def download_youtube_video(url):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        filename = stream.download(filename="video.mp4")
        return filename
    except Exception as e:
        print(f"❌ خطأ في التحميل: {e}")
        return None

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 أهلاً! أرسل رابط فيديو من يوتيوب وسأحمله لك 🎥")

# عند استلام رابط
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if "youtube.com" in url or "youtu.be" in url:
        await update.message.reply_text("⏳ جاري تحميل الفيديو... انتظر قليلاً 🎬")
        video_file = download_youtube_video(url)
        if video_file:
            await update.message.reply_video(video=open(video_file, "rb"))
            os.remove(video_file)
        else:
            await update.message.reply_text("❌ حدث خطأ أثناء التحميل 😢")
    else:
        await update.message.reply_text("📎 أرسل رابط يوتيوب صالح من فضلك.")

# تهيئة البوت
def run_bot():
    app_telegram = ApplicationBuilder().token(TOKEN).build()
    app_telegram.add_handler(CommandHandler("start", start))
    app_telegram.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 البوت يعمل الآن...")
    app_telegram.run_polling()

# Flask لتشغيل السيرفر المحلي
@app.route('/')
def home():
    return "✅ البوت والسيرفر يعملان الآن!"

if __name__ == "__main__":
    from threading import Thread
    Thread(target=lambda: app.run(port=5000)).start()
    run_bot()
