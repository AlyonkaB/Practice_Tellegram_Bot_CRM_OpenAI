import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

load_dotenv()

SUPPORT_BOT_TOKEN = os.getenv("SUPPORT_BOT_TOKEN")


def main_keyboard():
    keyboard = [
        [InlineKeyboardButton(
            "Submit Feedback",
            callback_data="submit_feedback")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! This is customer support bot. Please choose an option:",
        reply_markup=main_keyboard(),
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "submit_feedback":
        context.user_data["awaiting_feedback"] = True
        await query.edit_message_text(text="Please send your feedback")
    else:
        pass


async def handler_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data["awaiting_feedback"]:
        # feedback = update.message.text
        await update.message.reply_text("Thank you for your feedback")
        del context.user_data["awaiting_feedback"]
        # create lead(feedback)
    await update.message.reply_text(
        "Please choose an option:", reply_markup=main_keyboard()
    )


def main():
    app = ApplicationBuilder().token(SUPPORT_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.ALL, handler_message))
    app.run_polling()


if __name__ == "__main__":
    main()
