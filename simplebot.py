from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, Bot
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler, CallbackQueryHandler

import os
from dotenv import load_dotenv


load_dotenv()
ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN")


async def hello(update: Update, context):
    message_text = update.message.text
    await update.message.reply_text(f"Hello, I'v got your message. \\ {message_text}")


def main_menu_keyboard():
    keybord = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Button 1", callback_data="button_1")],
            [InlineKeyboardButton("Button 2", callback_data="button_2")],
            [InlineKeyboardButton("Get leads", callback_data="get_leads")],
            [
                InlineKeyboardButton("Button 4", callback_data="button_4"),
                InlineKeyboardButton("Button 5", callback_data="button_5"),
            ],
        ]
    )
    return keybord


async def begin(update: Update, context):
    await update.message.reply_text("Choose one button", reply_markup=main_menu_keyboard())


async def button_handler(update: Update, context):
    query = update.callback_query
    await query.message.reply_text(text=f"You chose {query.data}", reply_markup=main_menu_keyboard())


def main():
    app = ApplicationBuilder().token(ADMIN_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", begin))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()


if __name__ == "__main__":
    main()
