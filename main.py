import os, threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
CH = os.getenv("CHANNEL_USERNAME")
print(f"DEBUG TOKEN exists: {bool(TOKEN)}, CH: {CH}")

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is Live!"

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or update.message.from_user.is_bot:
        return
    uid = update.effective_user.id
    try:
        m = await context.bot.get_chat_member(update.effective_chat.id, uid)
        if m.status in ['administrator','creator']:
            return
    except: pass
    try:
        cm = await context.bot.get_chat_member(CH, uid)
        if cm.status in ['member','administrator','creator']:
            return
    except: pass
    try:
        await context.bot.delete_message(update.effective_chat.id, update.message.message_id)
        w = await context.bot.send_message(update.effective_chat.id, f"⚠️ Join {CH} first!")
        import asyncio
        await asyncio.sleep(10)
        await context.bot.delete_message(update.effective_chat.id, w.message_id)
    except Exception as e:
        print(f"Check error: {e}")

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
    if not TOKEN:
        print("ERROR: BOT_TOKEN is missing in Environment!")
        while True: pass
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check))
    print("Bot Started... Polling")
    application.run_polling()
