import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import yt_dlp

# توكن البوت الخاص بك
TOKEN = "9251185654:AAHlnlji6ZL8xz9s3V_gHidY-XNw4IxgMgk"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🔥 **يا هلا ومرحبتين بيك يا وحش!** ⚡️\n\n"
        "أنا **بوت تحميل الفيديوهات الخارق** 🎬📱\n"
        "أقدر أحمل لك فيديوهات من:\n"
        "🎵 تيك توك | 📸 إنستغرام | 📺 يوتيوب | 📌 بنتريست\n\n"
        "فقط أرسل لي رابط أي فيديو وسأقوم بتحميله فوراً وبأعلى جودة! 🚀\n\n"
        "------------------------------------\n"
        "🛠 **تم تطوير وبرمجة هذا البوت بواسطة المبدع: [ كوستر ]** 😎✨"
    )
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    chat_id = update.message.chat_id
    
    if not url.startswith("http"):
        await context.bot.send_message(chat_id=chat_id, text="الرجاء إرسال رابط صالح فقط 🔗")
        return

    await context.bot.send_message(chat_id=chat_id, text="جاري التحميل والمعالجة يا غالي، ثواني ويكون الفيديو عندك... ⏳")

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloaded_video.%(ext)s',
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        if os.path.exists(filename):
            await context.bot.send_video(chat_id=chat_id, video=open(filename, 'rb'))
            os.remove(filename)
        else:
            await context.bot.send_message(chat_id=chat_id, text="عذراً، لم أتمكن من إيجاد ملف الفيديو للتحميل.")

    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"حدث خطأ أثناء التحميل: تأكد أن الرابط عام وصحيح ⚠️")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("البوت يعمل بنجاح ويقبل كل المنصات...")
    application.run_polling()
