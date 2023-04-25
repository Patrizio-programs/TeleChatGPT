import os
import telebot
from flask import Flask, request
import requests
from threading import Thread
import time

app = Flask(__name__)
# Set up the Telegram bot using your bot token
bot_key = os.environ['BOT_KEY']
bot = telebot.TeleBot(bot_key)
chatgpt_url = os.environ['url']
api_key = os.environ['API_KEY']


# Define the start command
@bot.message_handler(commands=['start'])
def start_command(message):
  chat_id = message['chat']['id']
  bot.send_message(chat_id, 'Enter a prompt, wait for a response.')


# Define the info command
@bot.message_handler(commands=['info'])
def info_command(message):
  chat_id = message['chat']['id']
  bot.send_message(
    chat_id,
    'TelechatGPT is powered by ChatGPT. Check this link for more info: https://patriziothedev.com/#/TeleChatGPT'
  )


#requesturl
#https://api.telegram.org/bot5540954974:AAHAy3eyPb_ZABlXIWjQBHDV7mv4hdRommU/setWebhook?url=https://tele-chatgpt.patrickmedley.repl.co
@bot.message_handler(func=lambda message: True)
def generate_message(message_dict):
  # Get the user's prompt
  prompt = message_dict["text"]

  id = message_dict["chat"]["id"]

  # Set up the request headers and data
  headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}'
  }
  data = {
    "model": "gpt-3.5-turbo",
    "messages": [{
      "role": "user",
      "content": prompt
    }]
  }

  # Send the request to ChatGPT
  response = requests.post(chatgpt_url, headers=headers, json=data)

  # Get the response data
  response_data = response.json()
  # Check if the response contains the 'choices' key
  if 'choices' not in response.json():
    bot.send_message(chat_id=id, text='Error generating message')
    return

  # Get the generated message from the response
  choices = response.json()['choices']
  # Get the first item in the 'choices' list
  first_choice = choices[0]
  # Get the 'message' dictionary from the first choice
  message_dict = first_choice['message']
  # Get the 'content' value from the 'message' dictionary
  message_content = message_dict['content']

  bot.send_message(chat_id=id, text=message_content)


def parse_message(message):
  if message['text'].startswith('/'):
    # Handle command
    if message['text'] == '/start':
      start_command(message)
    elif message['text'] == '/info':
      info_command(message)
    else:
      bot.reply_to(message, 'Unknown command.')
  else:
    # Handle regular message
    # Do something with the message
    generate_message(message)


# Flask route setup
@app.route("/", methods=["POST", "GET"])
def index():
  if request.method == "POST":
    msg = request.get_json()
    message = msg["message"]
    parse_message(message)
  else:
    return ("TeleChatGPT Online")
  return ("TELECHATGPT")


# Keep the server alive
def keep_alive():
  server = Thread(target=app.run, args=('0.0.0.0', 8080), daemon=True)
  server.start()
  while True:
    time.sleep(6)


if __name__ == "__main__":
  keep_alive()
