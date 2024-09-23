import os
from dotenv import load_dotenv
from telegram import (Update,
                      InlineKeyboardButton,
                      InlineKeyboardMarkup)
from telegram.ext import (ApplicationBuilder,
                          MessageHandler,
                          filters,
                          CommandHandler,
                          CallbackQueryHandler,
                          ContextTypes,
                          ConversationHandler)

from zoho_tools import create_leads

load_dotenv()

SUPPORT_BOT_TOKEN = os.getenv("SUPPORT_BOT_TOKEN")

ASK_FEEDBACK = 0
ASK_NAME = 1
ASK_EMAIL = 2
ASK_CITY = 3
ASK_FEEDBACK_TEXT = 4


def main_keyboard():
    keyboard = [
        [InlineKeyboardButton(
            "Submit Feedback",
            callback_data="submit_feedback"
        )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! This is customer support bot. Please choose an option:",
        reply_markup=main_keyboard()
    )
    return ASK_FEEDBACK


async def feedback_decision(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "submit_feedback":
        await query.edit_message_text(text="Please send your name")
        return ASK_NAME


async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text
    context.user_data["name"] = name
    await update.message.reply_text(text="What's your email?")
    return ASK_EMAIL


async def ask_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    email = update.message.text
    context.user_data["email"] = email
    await update.message.reply_text(text="Where do you live?")
    return ASK_CITY


async def ask_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = update.message.text
    context.user_data["city"] = city
    await update.message.reply_text(text="Please send your feedback")
    return ASK_FEEDBACK_TEXT


async def ask_feedback_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    feedback = update.message.text
    context.user_data["awaiting_feedback"] = feedback
    await update.message.reply_text(text="Thank you for your feedback")
    create_leads(context.user_data)
    await update.message.reply_text(
        "Please choose an option:",
        reply_markup=main_keyboard()
    )
    return ASK_FEEDBACK


def main():
    app = ApplicationBuilder().token(SUPPORT_BOT_TOKEN).build()
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_FEEDBACK: [CallbackQueryHandler(feedback_decision)],
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_name)],
            ASK_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_email)],
            ASK_CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_city)],
            ASK_FEEDBACK_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_feedback_text)],
        },
        fallbacks=[CommandHandler("start", start)],
    )
    app.add_handler(conversation_handler)
    app.run_polling()


if __name__ == "__main__":
    main()

