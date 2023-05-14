import os
from flask import Flask, request, render_template
import telebot
from theb import Completion

# Set up the Flask app
app = Flask(__name__, template_folder="templates")

# Set up the Telegram bot using your bot token
bot_key = os.environ['BOT_KEY']
bot = telebot.TeleBot(bot_key)

#Webhook setup
WEBHOOK_URL_BASE = "https://tele-chat-gpt.vercel.app"
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE)

# Define the response function
def generate_message(message):
  # Get the user's prompt
  prompt = message['text']
  id = message["chat"]["id"]

  # Generate a response using theb package
  response = ""
  for token in Completion.create(prompt):
    response += token

  # Send the response back to the user
  bot.send_message(chat_id=id, text=response)

# Define the start command
@bot.message_handler(commands=['start'])
def start_command(message):
  chat_id = message['chat']['id']
  bot.send_message(chat_id, 'Enter a prompt, wait for a response.')

# Define the info command
@bot.message_handler(commands=['info'])
def info_command(message):
  chat_id = message['chat']['id']
  markup = telebot.types.InlineKeyboardMarkup()
  button = telebot.types.InlineKeyboardButton(
    text='TeleChatGPT', url='https://tele-chatgpt.patrickmedley.repl.co')
  markup.add(button)
  bot.send_message(
    chat_id,
    'TelechatGPT is powered by ChatGPT. Click the button below for more info:',
    reply_markup=markup)

@bot.message_handler(commands=['bots'])
def bots_command(message):
  chat_id = message['chat']['id']
  button = telebot.types.InlineKeyboardButton(
    text="More bots here!", url="https://t.me/PatrizioTheDevbot")
  keyboard = telebot.types.InlineKeyboardMarkup()
  keyboard.add(button)
  bot.send_message(chat_id=chat_id,
                   text="To check on the other bots select the button",
                   reply_markup=keyboard)

# Define the parse_message function
def parse_message(message):
  if message['text'].startswith('/'):
    # Handle command
    if message['text'] == '/start':
      start_command(message)
    elif message['text'] == '/info':
      info_command(message)
    elif message['text'] == '/bots':
      bots_command(message)
    else:
      id = message["chat"]["id"]
      bot.send_message(id, 'Unknown command.')
  else:
    # Handle regular message
    # Do something with the message
    generate_message(message)

# Define the webhook route
@app.route("/", methods=["POST", "GET"])
def index():
  if request.method == "POST":
    msg = request.get_json()
    message = msg["message"]
    parse_message(message)
  else:
    return render_template("index.html")
  return ("TELECHATGPT")
