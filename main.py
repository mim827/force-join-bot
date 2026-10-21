import os
import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import threading

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "@MIM9614")
CHANNEL_LINK = f"https://t.me/{CHANNEL_USERNAME.replace('@','')}"

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is Live!"

async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_user:
        return
    if update.message.from_user.is_bot:
        return
    user_id = update.effective_user.id
    try:
        member = await context.bot.get_chat_member(update.effective_chat.id, user_id)
        if member.status in ['administrator', 'creator']:
            return
    except:
        pass
    try:
        ch_member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if ch_member.status in ['member', 'administrator', 'creator']:
            return
    except:
        pass
    try:
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
    except:
        pass
    try:
        warn = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"⚠️ {update.effective_user.mention_html()} আপনাকে প্রথমে চ্যানেলে জয়েন করতে হবে!\n\n👉 {CHANNEL_USERNAME}\n\nজয়েন করে আবার মেসেজ দিন।",
            parse_mode="HTML"
        )
        await asyncio.sleep(10)
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=warn.message_id)
    except Exception as e:
        print(f"Warn error: {e}")

def run_bot():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_join))
    print("Bot Started...")
    application.run_polling()

if __name__ == '__main__':
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
