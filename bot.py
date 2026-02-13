import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = '7732193903:AAEMaziFnapMisBsVFGn_-7pwG7-9kPIdIU'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Welcome Abdullah! Send me a YouTube link to download.')

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    await update.message.reply_text('⏳ Processing... Please wait.')
    
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': 'video_%(id)s.%(ext)s',
        'noplaylist': True,
        'cookiefile': 'cookies.txt',  # السطر ده هو السر
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
        with open(filename, 'rb') as video:
            await context.bot.send_video(chat_id=update.effective_chat.id, video=video)
        
        os.remove(filename)
    except Exception as e:
        await update.message.reply_text(f"❌ Error: Video is too large or YouTube is blocking the server.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    app.run_polling()

if __name__ == '__main__':
    main()
