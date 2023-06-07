import os
import telebot
from telebot import types
from flask import Flask, request, render_template
import requests
import json
import getenv


from modes import modes
import ai
from dotenv import load_dotenv

load_dotenv()

mode_names = list(modes.keys())
current_mode = modes["TeleChatGPT"]
user_modes = {}

keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
for mode_name in mode_names:
    button = telebot.types.InlineKeyboardButton(text=mode_name,
                                                callback_data=mode_name)
    keyboard.add(button)

app = Flask(__name__, template_folder="templates")
img_url = "https://openai80.p.rapidapi.com/images/generations"
bot_key = os.getenv('BOT_KEY')
img_token = os.getenv('IMG_TOKEN')

bot = telebot.TeleBot(bot_key)
# webhook = os.environ['WEBHOOK']
bot.delete_webhook()
# bot.set_webhook(url=webhook)
# generate LLM response with system message


@bot.message_handler(func=lambda message: not message.text.startswith('/'))
def generate_message(message):
    chat_id = message.chat.id
    prompt = message.text
    reply = bot.send_message(chat_id, "Thinking...")
    req = ai.Completion.create(prompt=prompt, systemMessage=current_mode)
    response = req["text"]
    bot.edit_message_text(chat_id=chat_id,
                          message_id=reply.message_id,
                          text=response)


# Define the start command
@bot.message_handler(commands=['start'])
def start_command(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Enter a prompt, wait for a response.')


# Define the info command
@bot.message_handler(commands=['info'])
def info_command(message):
    chat_id = message.chat.id
    button = telebot.types.InlineKeyboardButton(
        text="TeleChatGPT", url="webhook")
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(button)
    bot.send_message(
        chat_id,
        'TelechatGPT is powered by ChatGPT. Click the button below for more info:',
        reply_markup=keyboard)


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
        "It can take a while to generate your image so please be patient")
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
        bot.send_message(message.chat.id,
                         f"Error: {ex}. Try image generation another time")
        return
    except Exception as ex:
        bot.send_message(message.chat.id, f"Error: {ex}")
        return
    for image_dict in images_list:
        photo_url = image_dict["url"]
        bot.send_photo(message.chat.id, photo_url)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        update = telebot.types.Update.de_json(
            request.stream.read().decode('utf-8'))
        bot.process_new_updates([update])  # Handle command

        return 'ok', 200
    else:
        return render_template("index.html")

# define callback function for mode buttons


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.message.chat.id
    user_modes[user_id] = modes[call.data]
    # check if the user has a stored mode and set it as the current mode
    if user_id in user_modes:
        global current_mode
        current_mode = user_modes[user_id]
    else:
        current_mode = modes["TeleChatGPT"]
    bot.answer_callback_query(call.id, text="You have selected " + call.data)

# define command handler to display mode buttons


@bot.message_handler(commands=['mode'])
def modes_handler(message):
    user_id = message.chat.id
    bot.send_message(user_id, text="Please select a mode:",
                     reply_markup=keyboard)


bot.polling()
# app.run(debug=True, host="0.0.0.0", port=8080)
