import os
import telebot
from flask import Flask, request, render_template
from threading import Thread
import time
import requests
from Bard import Chatbot

app = Flask(__name__)
session_dict = {}
token = "VwjnU-fsrPuM_5iag-PVDc-7Rbp92i3pQEfE7B23WN8Di9TSVa-WAjdDJKxtJDaos-uwQg."
img_url = "https://openai80.p.rapidapi.com/images/generations"
bot_key = os.environ['BOT_KEY']
bot = telebot.TeleBot(bot_key)
webhook = os.environ['WEBHOOK']
bot.set_webhook(url=webhook)


# Define the response function
@bot.message_handler()
def generate_message(message):
  prompt = message.text
  chat_id = message.chat.id
  chatbot = Chatbot(token)
  response_dict = chatbot.ask(prompt)
  response = response_dict['content']
  bot.send_message(chat_id, response)
  
  


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
  button = telebot.types.InlineKeyboardButton(text='TeleChatGPT', url=webhook)
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


@bot.message_handler(commands=['img'])
def image_info(message):
  if message.text == "/img":
    bot.send_message(
      message.chat.id,
      "Please send a prompt with the command to generate an image. For example /img a dancing giraffe."
    )
  else:
    prompt = message.text[5:]
    bot.send_message(
      message.chat.id,
      "It can take a while to generate your image so please be patient")
    payload = {"prompt": prompt, "n": 2, "size": "1024x1024"}
    headers = {
      "Content-Type": "application/json",
      "X-RapidAPI-Key": "4c695ea717mshd319d684b42713ap1035c3jsnaac2d74ef2c2",
      "X-RapidAPI-Host": "openai80.p.rapidapi.com"
    }
    response = requests.post(img_url, json=payload, headers=headers)
    response_dict = response.json()
    print(response_dict)
    print(response)
    images_list = response_dict["data"]
    print(images_list)
    
    for image_dict in images_list:
      photo_url = image_dict["url"]
      bot.send_photo(message.chat.id, photo_url)


@app.route("/", methods=["GET", "POST"])
def index():
  if request.method == "POST":
    update = telebot.types.Update.de_json(
      request.stream.read().decode('utf-8'))
    message = update.message
    parse_message(message)
    return 'ok', 200
  else:
    return render_template("index.html")


def parse_message(message):
  if message.text.startswith('/'):
    # Handle command
    if message.text == '/start':
      start_command(message)
    elif message.text == '/info':
      info_command(message)
    elif message.text == '/bots':
      bots_command(message)
    elif message.text.startswith('/img'):
      image_info(message)
    else:
      chat_id = message.chat.id
      bot.send_message(chat_id, 'Unknown command.')
  else:
    # Handle regular message
    generate_message(message)
