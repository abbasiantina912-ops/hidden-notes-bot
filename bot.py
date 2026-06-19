from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "PASTE_YOUR_TOKEN_HERE"

ADMIN_ID = 123456789  # اینو بعداً با آیدی خودت عوض کن


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام 👋\n"
        "میتونی به صورت ناشناس به تینا پیام بدی ✨"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    username = f"@{user.username}" if user.username else "ندارد"

    forward_text = (
        "📩 پیام ناشناس جدید\n\n"
        f"👤 نام: {user.first_name}\n"
        f"🔹 یوزرنیم: {username}\n"
        f"🆔 آیدی: {user.id}\n\n"
        f"💬 پیام:\n{text}"
    )

    # ارسال برای ادمین
    sent_msg = await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=forward_text
    )

    # جواب به کاربر
    await update.message.reply_text("پیامت ارسال شد ✅")


async def reply_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # فقط ادمین میتونه ریپلای کنه
    if update.message.reply_to_message and update.effective_user.id == ADMIN_ID:
        original = update.message.reply_to_message.text

        # پیدا کردن آیدی کاربر از متن (ساده‌ترین روش)
        lines = original.split("\n")
        user_id = None

        for line in lines:
            if "🆔 آیدی:" in line:
                user_id = int(line.replace("🆔 آیدی:", "").strip())

        if user_id:
            await context.bot.send_message(
                chat_id=user_id,
                text=f"💌 پاسخ جدید:\n\n{update.message.text}"
            )

            await update.message.reply_text("ارسال شد به کاربر ✅")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.TEXT & filters.REPLY, reply_handler))

    app.run_polling()


if __name__ == "__main__":
    main()
