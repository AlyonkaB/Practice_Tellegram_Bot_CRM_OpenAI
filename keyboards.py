import os

from dotenv import load_dotenv
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from zoho_tools import make_zoho_api_get_request


load_dotenv()

ZOHO_API_CRM_URL = os.getenv("ZOHO_API_CRM_URL")


def main_menu_keyboard():
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Get leads", callback_data="get_leads")],
            [InlineKeyboardButton("Update_leads", callback_data="update_leads")],
            [InlineKeyboardButton("Delete_leads", callback_data="delete_leads")],
        ]
    )
    return keyboard


def back_keyboard():
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Back", callback_data="back")],
        ]
    )
    return keyboard


def list_leads_keyboard():
    leads = make_zoho_api_get_request(ZOHO_API_CRM_URL)
    keyboard = []
    for lead in leads["data"]:
        keyboard.append(
            [
                InlineKeyboardButton(
                    f"{lead['First_Name']}"
                    f" {lead['Last_Name']}:"
                    f" {lead['Email']}",
                    callback_data=lead["id"],
                )
            ]
        )
    keyboard.append([InlineKeyboardButton("Back", callback_data="back")])
    return keyboard
