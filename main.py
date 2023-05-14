import os
import telebot
from flask import Flask, request, render_template
from revChatGPT.V1 import Chatbot

app=Flask(__name__)
chat_history = ""

# Set up the Telegram bot using your bot token
bot_key = os.environ['BOT_KEY']
key = os.environ['KEY']

bot = telebot.TeleBot(bot_key)
server = Flask(__name__)

# Define the response function
def generate_message(message):
  chatbot = Chatbot(config={
  "access_token": "{key}"})
  prompt = message.text
  response = ""
  for data in chatbot.ask(
    prompt
  ):
    response = data["message"]
  bot.send_message(chat_id=chat_id, text=response)


# Define the start command
@bot.message_handler(commands=['start'])
def start_command(message):
  chat_id = message.chat.id
  bot.send_message(chat_id, 'Enter a prompt, wait for a response.')


# Define the info command
@bot.message_handler(commands=['info'])
def info_command(message):
  chat_id = message.chat.id
  markup = telebot.types.InlineKeyboardMarkup()
  button = telebot.types.InlineKeyboardButton(
    text='TeleChatGPT', url='https://tele-chat-gpt.vercel.app')
  markup.add(button)
  bot.send_message(
    chat_id,
    'TelechatGPT is powered by ChatGPT. Click the button below for more info:',
    reply_markup=markup)


@bot.message_handler(commands=['bots'])
def bots_command(message):
  chat_id = message.chat.id
  button = telebot.types.InlineKeyboardButton(
    text="More bots here!", url="https://t.me/PatrizioTheDevbot")
  keyboard = telebot.types.InlineKeyboardMarkup()
  keyboard.add(button)
  bot.send_message(chat_id=chat_id,
                   text="To check on the other bots select the button",
                   reply_markup=keyboard)


# Define the parse_message function
def parse_message(message):
  if message.text.startswith('/'):
    # Handle command
    if message.text == '/start':
      start_command(message)
    elif message.text == '/info':
      info_command(message)
    elif message.text == '/bots':
      bots_command(message)
    else:
      chat_id = message.chat.id
      bot.send_message(chat_id, 'Unknown command.')
  else:
    # Handle regular message
    generate_message(message)


# Handle all messages, including regular messages
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
  parse_message(message)
  return None

bot.add_message_handler(handle_all_messages)
# Handle incoming webhook requests from Telegram
@app.route('/' + bot_key, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    message = update.message
    handle_all_messages(message)
    return 'ok', 200

@app.route("/", methods=["GET"])
def index():
  return render_template("index.html")

