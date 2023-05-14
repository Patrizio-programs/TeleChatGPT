import os
import telebot
from flask import Flask, request, render_template
from revChatGPT.V1 import Chatbot
import asyncio

app=Flask(__name__)
app.config['TIMEOUT'] = 60  # Set the timeout to 60 seconds
# Set up the Telegram bot using your bot token
bot_key = os.environ['BOT_KEY']
key = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJwYXRyaXppb21lZGxleUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZX0sImh0dHBzOi8vYXBpLm9wZW5haS5jb20vYXV0aCI6eyJ1c2VyX2lkIjoidXNlci1Nd2pLT1FIa3VESE51Z3hHR1R3a0NOYW4ifSwiaXNzIjoiaHR0cHM6Ly9hdXRoMC5vcGVuYWkuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTA0MDM5ODE5NTY0NzAwNTc0NzgzIiwiYXVkIjpbImh0dHBzOi8vYXBpLm9wZW5haS5jb20vdjEiLCJodHRwczovL29wZW5haS5vcGVuYWkuYXV0aDBhcHAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTY4NDA5MTQ0NSwiZXhwIjoxNjg1MzAxMDQ1LCJhenAiOiJUZEpJY2JlMTZXb1RIdE45NW55eXdoNUU0eU9vNkl0RyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgbW9kZWwucmVhZCBtb2RlbC5yZXF1ZXN0IG9yZ2FuaXphdGlvbi5yZWFkIG9mZmxpbmVfYWNjZXNzIn0.gYbTpZWMhBevTHspTPSkUNtdWDGD5CJByWz3zz5wqsM53b9tQktfWqg6QRHQBzoRO-GSxU1VLxWR7V9yMLQmDt3K73d0PewwEFpjlE4qBRN3C1ueeVR9-4jVSddmugV2D1tirabW0Al5ZkxlfTjX3pmwwY-YhjSSJWiJ8po2QiBunsYgH6d8vYZnAKyE39qyh6PmnxCExgNkV_TF3iTUq8otCXBH9835qija77K1dz_VLAdxCMEFBrGsUzKOIlLIphEn2VtV8gKCmTAnSg6M1FmfogvgpwnryAiB0-ySSHg07p4kpOVEgKyI9O6XLWeWSFPo8pxNBrduIeVum81rbw"
bot = telebot.TeleBot(bot_key)
server = Flask(__name__)

# Define the response function
async def generate_message(message):
  chatbot = Chatbot(config={
    "access_token": key
  }, conversation_id=str(message.chat.id)) # generate conversation id using chat id
  prompt = message.text
  response = ""
  for data in chatbot.ask(prompt):
    response = data["message"]
  await bot.send_message(chat_id=message.chat.id, text=response)


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
async def parse_message(message):
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
      await bot.send_message(chat_id, 'Unknown command.')
  else:
    # Handle regular message
    await generate_message(message)

# Handle all messages, including regular messages
@bot.message_handler(func=lambda message: True)
async def handle_all_messages(message):
  await parse_message(message)
  return None

# Handle incoming webhook requests from Telegram
@app.route('/' + bot_key, methods=['POST'])
async def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    message = update.message
    await handle_all_messages(message)
    return 'ok', 200

@app.route("/", methods=["GET"])
def index():
  return render_template("index.html")
