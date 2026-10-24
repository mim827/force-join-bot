import os, threading, asyncio
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, ContextTypes

app = Flask(__name__)
TOKEN = os.environ.get("BOT_TOKEN")

# শুধু তোমার একটা চ্যানেল
CHANNELS = ["@MIM2746"]
LINKS = ["https://t.me/MIM2746"]

@app.route('/')
def home():
    return "Bot is Live! 24H Running"

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or update.message.from_user.is_bot:
        return
    
    uid = update.effective_user.id
    user = update.effective_user
    username = f"@{user.username}" if user.username else user.first_name

    # এডমিন হলে কিছু করবে না
    try:
        m = await context.bot.get_chat_member(update.effective_chat.id, uid)
        if m.status in ['administrator', 'creator']:
            return
    except:
        pass

    # চ্যানেলে জয়েন চেক
    try:
        for ch in CHANNELS:
            cm = await context.bot.get_chat_member(ch, uid)
            if cm.status not in ['member', 'administrator', 'creator']:
                raise Exception("not joined")
    except:
        text = f"মেসেজ করার আগে, {username} 😳 আপনাকে আমাদের চ্যানেলে জয়েন করতে হবে। (সতর্কবার্তা: 1/10)"
        buttons = [[InlineKeyboardButton("📢 চ্যানেলে জয়েন করুন / Join Channel", url=LINKS[0])]]
        
        try:
            await update.message.delete()
        except:
            pass
            
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

async def main_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, check))
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    print("Bot Started - 24H")
    await asyncio.Event().wait()

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    asyncio.run(main_bot())
