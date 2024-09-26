# Practice_Tellegram_Bot_CRM_OpenAI


This is af set of Telegram bots built using Python and the `python-telegram-bot` library. The bots are created in educational purpose for the intensive

## Prerequisites

Before running the bot, make sure you have the following installed:

- Python 3.12

## Setup

1. Clone the repository:
```bash
git clone https://github.com/AlyonkaB/Practice_Tellegram_Bot_CRM_OpenAI.git
```

2. Install all libraries from requirements.txt

```bash
pip3 install -r requirements.txt
```

3. Create two new Telegram bots by talking to the `@BotFather` bot and follow the instructions to obtain an API tokens ADMIN_BOT_TOKEN and SUPPORT_BOT_TOKEN

4. Register account in Zoho CRM and obtain app credentials ZOHO_REFRESH_TOKEN, ZOHO_ACCESS_TOKEN,  ZOHO_CLIENT_ID, ZOHO_CLIENT_SECRET

5. Register OpenAI API account and obtain OPENAI_API_KEY

4. Create a new file named `.env` in the project root directory and add the following lines, providing corresponding values:

```
ADMIN_BOT_TOKEN=
SUPPORT_BOT_TOKEN=
ZOHO_API_TOKEN_URL=https://accounts.zoho.eu/oauth/v2/token
ZOHO_API_CRM_URL=https://www.zohoapis.eu/crm/v2/Leads
ZOHO_REFRESH_TOKEN=
ZOHO_ACCESS_TOKEN = 
ZOHO_CLIENT_ID=
ZOHO_CLIENT_SECRET=
OPENAI_API_KEY=
```


## Running the Bot

To run the bot, execute the following command in the project root directory:

```bash
python bot.py
```


The bot should now be running and ready to receive messages from Telegram.

## Usage

send /start to bot in telegram and continue interactin with it
