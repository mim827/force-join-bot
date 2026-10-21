 import os
import asyncio
import threading
from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = os.getenv("CHANNEL", "@MIM9614")
LINK = f"https://t.me/{CHANNEL.replace('@','')}"

# Render এর জন্য ফেক ওয়েব সার্ভার
app_flask = Flask(__name__)
@app_flask.route('/')
def home():
    return "Bot is Alive 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host='0.0.0.0', port=port)

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.from_user:
        return
    try:
        cm = await context.bot.get_chat_member(update.effective_chat.id, update.effective_user.id)
        if cm.status in ['administrator', 'creator']:
            return
    except: pass
    try:
        m = await context.bot.get_chat_member(CHANNEL, update.effective_user.id)
        if m.status not in ['left', 'kicked']:
            return
    except: pass
    try:
        await update.message.delete()
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("✅ Join Channel", url=LINK)]])
        sent = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"⚠️ {update.effective_user.first_name} কথা বলতে {CHANNEL} জয়েন করো! (10s)",
            reply_markup=keyboard
        )
        await asyncio.sleep(10)
        await sent.delete()
    except Exception as e:
        print(e)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is Live 24/7!")

def main():
    threading.Thread(target=run_flask, daemon=True).start()
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, check))
    print("Bot Started 24/7")
    app.run_polling()

if __name__ == "__main__":
    main()
