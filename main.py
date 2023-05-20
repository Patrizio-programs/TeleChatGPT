import os
import telebot
from telebot import types
from flask import Flask, request, render_template
import requests
from modes import modes
from api import headers, completions

app = Flask(__name__)
img_url = "https://openai80.p.rapidapi.com/images/generations"
bot_key = os.environ['BOT_KEY']
token = os.environ['CHAT_TOKEN']
img_token = os.environ['IMG_TOKEN']
bot = telebot.TeleBot(bot_key)
webhook = os.environ['WEBHOOK']
current_mode = modes['TeleChatGPT']()
bot.set_webhook(url=webhook)

# Define the response function
@bot.message_handler()
def generate_message(message):
  chat_id = message.chat.id
    # Handle regular message
  system_message = current_mode.system_message
  prompt = message.text
  reply = bot.send_message(chat_id, "Thinking...")
  payload = {
      "model":
      "gpt-3.5-turbo",
      "max_tokens":
      4000,
      "messages": [{
        "role": "system",
        "content": system_message
      }, {
        "role": "user",
        "content": prompt
      }]
    }
  response = requests.post(completions, json=payload, headers=headers)
  response_json = response.json()
  data= response_json['choices'][0]['message']['content']
  print(response_json)
  bot.edit_message_text(chat_id=chat_id,
                          message_id=reply.message_id,
                          text=data)
    
# Define the mode update function
@bot.message_handler(commands=['mode'])
def choose_mode(message):
  keyboard = types.InlineKeyboardMarkup()
  for mode in modes:
    button = types.InlineKeyboardButton(text=mode, callback_data=mode)
    keyboard.add(button)
  bot.send_message(message.chat.id,
                   "Please choose a mode:",
                   reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def mode_callback(call):
  mode_name = call.data
  mode = modes[mode_name]()
  global current_mode
  current_mode = mode
  bot.answer_callback_query(callback_query_id=call.id,
                            text=f"Mode changed to {mode_name}")

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
        return

    prompt = message.text[5:]
    bot.send_message(
        message.chat.id,
        "It can take a while to generate your image so please be patient"
    )
    payload = {"prompt": prompt, "n": 2, "size": "1024x1024"}
    headers = {
        "Content-Type": "application/json",
        "X-RapidAPI-Key": img_token,
        "X-RapidAPI-Host": "openai80.p.rapidapi.com"
    }

    try:
        response = requests.post(img_url, json=payload, headers=headers)
        response.raise_for_status()
        response_dict = response.json()
        images_list = response_dict["data"]
    except requests.exceptions.HTTPError as ex:
        bot.send_message(
            message.chat.id,
            f"Error: {ex}. Try image generation another time"
        )
        return
    except Exception as ex:
        bot.send_message(
            message.chat.id,
            f"Error: {ex}"
        )
        return
    for image_dict in images_list:
        photo_url = image_dict["url"]
        bot.send_photo(message.chat.id, photo_url)


@app.route("/", methods=["GET", "POST"])
def index():
  if request.method == "POST":
   update = telebot.types.Update.de_json(
      request.stream.read().decode('utf-8'))
   bot.process_new_updates([update])
    return 'ok', 200
  else:
    return render_template("index.html")
