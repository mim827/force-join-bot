import os, threading, asyncio
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, ContextTypes

app = Flask(__name__)
TOKEN = os.environ.get("BOT_TOKEN")
CHANNELS = ["@BRA_ERS", "@Dhaka83"]
LINKS = ["https://t.me/BRA_ERS", "https://t.me/Dhaka83"]

def home():
    return "Bot is Live!"

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or update.message.from_user.is_bot:
        return

    uid = update.effective_user.id

    # Admin হলে কিছু করবে না
    try:
        m = await context.bot.get_chat_member(update.effective_chat.id, uid)
        if m.status in ['administrator', 'creator']:
            return
    except: pass

    # চ্যানেলে জয়েন আছে কিনা চেক - ২টা চ্যানেল লুপ করে
    try:
        for ch in CHANNELS:
            cm = await context.bot.get_chat_member(ch, uid)
            if cm.status not in ['member', 'administrator', 'creator']:
                raise Exception("not joined")
    except:
        # জয়েন না থাকলে ডিলিট + ওয়ার্নিং
        try:
            await context.bot.delete_message(update.effective_chat.id, update.message.message_id)

            keyboard = []
            for i, link in enumerate(LINKS):
                keyboard.append([InlineKeyboardButton(f"✅ Join {CHANNELS[i]}", url=link)])
            markup = InlineKeyboardMarkup(keyboard)

            w = await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"⚠️ গ্রুপে কথা বলতে হলে আগে চ্যানেল জয়েন করো!",
                reply_markup=markup
            )
            await asyncio.sleep(10)
            await context.bot.delete_message(update.effective_chat.id, w.message_id)
        except Exception as e:
            print(f"Check error: {e}")

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, check))
    application.run_polling()
