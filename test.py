import os
import telebot
from telebot import types
from flask import Flask, request, render_template
import requests
from revChatGPT.V1 import Chatbot

app = Flask(__name__)
img_url = "https://openai80.p.rapidapi.com/images/generations"
bot_key = "5906970415:AAEgFJyTc00trD2pLT28jobP2Er73sfX1q0"
token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJwYXRyaXppb21lZGxleUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZX0sImh0dHBzOi8vYXBpLm9wZW5haS5jb20vYXV0aCI6eyJ1c2VyX2lkIjoidXNlci1Nd2pLT1FIa3VESE51Z3hHR1R3a0NOYW4ifSwiaXNzIjoiaHR0cHM6Ly9hdXRoMC5vcGVuYWkuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTA0MDM5ODE5NTY0NzAwNTc0NzgzIiwiYXVkIjpbImh0dHBzOi8vYXBpLm9wZW5haS5jb20vdjEiLCJodHRwczovL29wZW5haS5vcGVuYWkuYXV0aDBhcHAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTY5MjgxMTUzMSwiZXhwIjoxNjk0MDIxMTMxLCJhenAiOiJUZEpJY2JlMTZXb1RIdE45NW55eXdoNUU0eU9vNkl0RyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgbW9kZWwucmVhZCBtb2RlbC5yZXF1ZXN0IG9yZ2FuaXphdGlvbi5yZWFkIG9yZ2FuaXphdGlvbi53cml0ZSBvZmZsaW5lX2FjY2VzcyJ9.MjAUrDnw_lf6zJ-fk6nirvUCIcAFlcXqcWr2p0YsahBnl2rRu1XrEOPcqh1vMoF9DzwonoFLDh4Cy4MtG7DaiMEo-pny99vOH9MXbrKDSwOQg9czhgD7Uoxe5RR5ErczAdruzjE_pjp372edsk2oAIxAZ5G_1lYC7Ooz9-MCuVK75vGTSQCRhBmV--_kRhSsZv9QvRmpm9OHkyyto839m2UZvv7RK-I28c106FYAUnRdvQbRnRnCtBaxaYPQIrOV8wrradO4C07HCrk4iPxc1Cpsxv996l2hEEQ0Eh638p_wo_gR1fTgVtEpRYgjn4PDMX6u-Z88T7ACruJZaYXlgw"

img_token = "4c695ea717mshd319d684b42713ap1035c3jsnaac2d74ef2c2"
bot = telebot.TeleBot(bot_key)
webhook = 'web'
# bot.set_webhook(url=webhook)
bot.delete_webhook()
# Define the response function


@bot.message_handler()
def generate_message(message):
    chat_id = message.chat.id
    prompt = message.text
    reply = bot.send_message(chat_id, "Thinking...")
    chatbot = Chatbot(config={
        "access_token": token,
        "conversation_id": chat_id

    })
    prompt = prompt
    response = ""
    for data in chatbot.ask(
        prompt
    ):
        response = data["message"]
    print(data)
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
    markup = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton(
        text='TeleChatGPT', url=webhook)
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


bot.polling()
