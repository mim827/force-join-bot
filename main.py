import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL", "@MIM9614")
CHANNEL_LINK = f"https://t.me/{CHANNEL_USERNAME.replace('@','')}"

async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type not in ["group", "supergroup"]:
        return
    try:
        user_id = update.message.from_user.id
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ['left', 'kicked']:
            raise Exception("Not Joined")
    except:
        try:
            await update.message.delete()
        except:
            pass
        keyboard = [[InlineKeyboardButton("✅ Join Channel", url=CHANNEL_LINK)]]
        await update.message.reply_text(
            f"⚠️ গ্রুপে কথা বলতে হলে আগে চ্যানেল জয়েন করো!",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Bot চালু আছে!")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_join))
    print("Bot Started...")
    app.run_polling()

if __name__ == "__main__":
    main()
