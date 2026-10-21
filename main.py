import os, asyncio, threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
CH = os.getenv("CHANNEL_USERNAME", "@MIM9614")

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot Live"

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or update.message.from_user.is_bot:
        return
    uid = update.effective_user.id
    try:
        m = await context.bot.get_chat_member(update.effective_chat.id, uid)
        if m.status in ['administrator','creator']:
            return
    except:
        pass
    try:
        cm = await context.bot.get_chat_member(CH, uid)
        if cm.status in ['member','administrator','creator']:
            return
    except:
        pass
    try:
        await context.bot.delete_message(update.effective_chat.id, update.message.message_id)
        w = await context.bot.send_message(update.effective_chat.id, f"⚠️ Join {CH} first!", parse_mode="HTML")
        await asyncio.sleep(10)
        await context.bot.delete_message(update.effective_chat.id, w.message_id)
    except Exception as e:
        print(e)

def run_bot():
    app_bot = Application.builder().token(TOKEN).build()
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check))
    print("Bot Started...")
    app_bot.run_polling()

if __name__ == '__main__':
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
