from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from pytube import YouTube

TOKEN = "8121555720:AAHOZ3WNi5H7N0lrNrK4dyCoY_wTiaFpGzU"

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 أهلاً! أرسل لي رابط فيديو من YouTube وسأحمله لك 🎥")

# عند إرسال رابط
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if "youtube.com" not in url and "youtu.be" not in url:
        await update.message.reply_text("❌ هذا ليس رابط YouTube صالح.")
        return

    await update.message.reply_text("⏳ جارٍ تحميل الفيديو، انتظر قليلاً...")

    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        video_file = stream.download(filename="video.mp4")
        await update.message.reply_video(video=open(video_file, "rb"))
    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ أثناء التحميل: {e}")

# إنشاء التطبيق
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    print("🤖 البوت يعمل الآن...")
    app.run_polling()

if __name__ == "__main__":
    main()
