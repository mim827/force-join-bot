 import os
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = os.getenv("CHANNEL", "@MIM9614")
LINK = f"https://t.me/{CHANNEL.replace('@','')}"

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.from_user:
        return

    # Admin হলে ইগনোর
    try:
        cm = await context.bot.get_chat_member(update.effective_chat.id, update.effective_user.id)
        if cm.status in ['administrator', 'creator']:
            return
    except:
        pass

    # জয়েন চেক
    try:
        m = await context.bot.get_chat_member(CHANNEL, update.effective_user.id)
        if m.status not in ['left', 'kicked']:
            return
    except:
        pass

    # ইউজারের মেসেজ ডিলেট
    try:
        await update.message.delete()
    except:
        pass

    # ওয়ার্নিং পাঠাও
    try:
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("✅ Join Channel", url=LINK)]])
        sent = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"⚠️ {update.effective_user.first_name} গ্রুপে কথা বলতে হলে আগে {CHANNEL} জয়েন করো! (10s)",
            reply_markup=keyboard
        )
        # 10 সেকেন্ড পর ওয়ার্নিং ডিলেট
        await asyncio.sleep(10)
        await sent.delete()
    except Exception as e:
        print(f"Error: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot Active!")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, check))
    print("Bot Started")
    app.run_polling()

if __name__ == "__main__":
    main()
