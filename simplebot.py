from telegram import Update, InlineKeyboardMarkup
from telegram.ext import (ApplicationBuilder,
                          CommandHandler,
                          CallbackQueryHandler)

import os
from dotenv import load_dotenv

from keyboards import main_menu_keyboard, list_leads_keyboard
from zoho_tools import make_zoho_api_get_request, delete_lead


load_dotenv()

ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN")
ZOHO_API_CRM_URL = os.getenv("ZOHO_API_CRM_URL")


async def hello(update: Update):
    message_text = update.message.text
    await update.message.reply_text(
        f"Hello, I'v got your message."
        f" \\ {message_text}"
    )


async def begin(update: Update, context):
    await update.message.reply_text(
        "Choose one button",
        reply_markup=main_menu_keyboard()
    )


async def button_handler(update: Update, context):
    query = update.callback_query
    leads = make_zoho_api_get_request(ZOHO_API_CRM_URL)
    list_lead_id = [lead['id'] for lead in leads["data"]]

    if query.data == "get_leads":
        await query.edit_message_text(
            text="List leads:",
            reply_markup=InlineKeyboardMarkup(list_leads_keyboard())
        )

    elif query.data == "delete_leads":

        await query.edit_message_text(
            text="Select a lead to delete:",
            reply_markup=InlineKeyboardMarkup(list_leads_keyboard())
        )
    elif query.data in list_lead_id and query.message.text == "Select a lead to delete:":
        delete_lead(query.data)

    elif query.data == "back":
        await query.edit_message_text(
            "Main menu or previous options here.",
            reply_markup=main_menu_keyboard()
        )


def main():
    app = ApplicationBuilder().token(ADMIN_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", begin))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()


if __name__ == "__main__":
    main()
