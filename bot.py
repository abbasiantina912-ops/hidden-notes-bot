import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("8807540774:AAGpcvFozdAy0ZedTUXBj5gFPkprtlgLFjE")
ADMIN_ID = 1032476437  # آیدی خودت رو اینجا بذار

# برای نگه داشتن مپ پیام‌ها (برای ریپلای)
user_map = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام 👋\n"
        "میتونی به صورت ناشناس به تینا پیام بدی ✨"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    username = f"@{user.username}" if user.username else "ندارد"

    formatted = (
        "📩 پیام ناشناس جدید\n\n"
        f"👤 نام: {user.first_name}\n"
        f"🔹 یوزرنیم: {username}\n"
        f"🆔 آیدی: {user.id}\n\n"
        f"💬 پیام:\n{text}"
    )

    # ارسال برای ادمین + ذخیره برای ریپلای
    sent = await context.bot.send_message(chat_id=ADMIN_ID, text=formatted)

    # ذخیره ارتباط پیام
    user_map[sent.message_id] = user.id

    await update.message.reply_text("پیامت ارسال شد ✅")


async def reply_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if update.message.reply_to_message:
        replied_id = update.message.reply_to_message.message_id

        if replied_id in user_map:
            user_id = user_map[replied_id]

            await context.bot.send_message(
                chat_id=user_id,
                text=f"💌 پاسخ جدید:\n\n{update.message.text}"
            )

            await update.message.reply_text("ارسال شد ✅")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.TEXT & filters.REPLY, reply_handler))

    app.run_polling()


if __name__ == "__main__":
    main()
