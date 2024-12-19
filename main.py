import asyncio
import telegram
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.ext import CommandHandler
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from collections import defaultdict
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

genai.configure(api_key="AIzaSyD27H8KIoHUOYHsY6AaR4qp6A1XskIWK9g")
model = genai.GenerativeModel("gemini-1.5-flash")
TOKEN="7377477076:AAHTEi5RtWjg6vxW9xdttRwK9xPQ2g8cFsc"

user_chats = defaultdict(lambda: model.start_chat(
    history=[
        {"role": "user", "parts": "Hello"},
        {"role": "model", "parts": "Great to meet you. What would you like to know?"},
    ]
))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def new(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_chats[update.effective_user.id]= model.start_chat()
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ##print(update.message.text)
    response =  user_chats[update.effective_user.id].send_message(update.message.text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response.text)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="/new --new conversation")



if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    help_handler = CommandHandler('help', help)
    application.add_handler(help_handler)

    new_handler = CommandHandler('new', new)
    application.add_handler(new_handler)

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(echo_handler)

    application.run_polling()