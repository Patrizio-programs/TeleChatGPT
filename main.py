import os
import telebot
import openai
from flask import Flask, request

app=Flask(__name__)

openai.api_key = 'pk-qGZJtLelPnaOwizOBlZJUtcPhBOPTqMxuvhFSpAarHKYXXOg'
openai.api_base = 'https://api.pawan.krd/v1'
chat_history = ""

# Set up the Telegram bot using your bot token
bot_key = os.environ['BOT_KEY']
bot = telebot.TeleBot(bot_key)
server = Flask(__name__)


# Define the response function
def generate_message(message):
  user_message = message.text
  global chat_history
  # Get the user's prompt
  prompt = f"{chat_history}\nHuman: {user_message}\nAI:"

  # Generate a response using the OpenAI package
  response = openai.Completion.create(model="gpt-3.5-turbo",
                                      prompt=prompt,
                                      temperature=0.7,
                                      max_tokens=256,
                                      top_p=1,
                                      frequency_penalty=0,
                                      presence_penalty=0,
                                      stop=["Human:",
                                            "AI:"]).choices[0].text.strip()

  # Update chat history with new prompt and response
  chat_history += f"\nHuman: {user_message}\nAI: {response}"

  # Send the response back to the user
  chat_id = message.chat.id
  print(response)
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

  
  


# Handle incoming webhook requests from Telegram
@server.route('/' + bot_key, methods=['POST'])
def webhook():
  update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
  bot.process_new_updates([update])
  return 'ok', 200


@app.route("/", methods=["GET"])
def index():
  return ("TELECHATGPT")

bot.polling()
