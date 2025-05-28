import nest_asyncio
import asyncio
from telegram import Update
import os
from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder, ContextTypes,
    MessageHandler, CommandHandler, filters
)

# Hozirgi event loop’ni patch qilish
nest_asyncio.apply()

# Env ni yuklash
load_dotenv()
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✍️ Write your request below, we will respond shortly.")

# Foydalanuvchi xabari kelganda
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    msg = (
        "📥 New website request!\n\n"
        f"👤 From: {user.full_name} (@{user.username})\n"
        f"💬 Message: {text}"
    )
    await context.bot.send_message(chat_id=CHAT_ID, text=msg)
    await update.message.reply_text(
        "🎉 Thank you!\n"
        "Your request has been submitted.\n"
        "Our team will contact you within 24 hours."
    )

# Botni ishga tushirish
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await app.bot.set_my_description(
        description=(
            "📥 Want a website?\n\n"
            "Just write your request below "
            "(e.g., \"I want an online store for my food business\").\n\n"
            "✅ SDC will receive it and contact you soon."
        )
    )

    print("🤖 Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
