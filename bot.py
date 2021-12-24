import os
from configs import Config
from pyrogram import Client, filters, idle
from pyrogram.types import (
  InlineKeyboardMarkup,
  InlineKeyboardButton,
  Message,
  CallbackQuery,
)



app = Client(

  api_id = Config.API_ID,
  api_hash = Config.API_HASH,
  bot_token = Config.BOT_TOKEN,
  session_name = Config.SESSION_NAME
)


@app.on_message(filters.command("start"))
def start(app,msg):
  app.send_message(msg.chat.id, "hello there")


@app.on_message(filters.command("help"))
def help(app,msg):
  app.send_message(msg.chat.id, "How may i help you")



app.run()  # Automatically start() and idle()