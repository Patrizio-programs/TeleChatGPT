import os
import telebot
from telebot import types
from flask import Flask, request, render_template
import requests
from revChatGPT.V1 import Chatbot

# LLM imports
from gpt_llm import ChatGPT, chat_token
from modes import modes
from langchain.prompts import (
    SystemMessagePromptTemplate,
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)

mode_names = list(modes.keys())
current_mode = modes["TeleChatGPT"]


# mode button keyboard
keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
for mode_name in mode_names:
    button = telebot.types.InlineKeyboardButton(
        text=mode_name, callback_data=mode_name)
    keyboard.add(button)

chatbot = ChatGPT(token=chat_token)

app = Flask(__name__, template_folder="templates")
img_url = "https://openai80.p.rapidapi.com/images/generations"
bot_key = "6160231980:AAGz70x3VQqYgKnVgXGx6o3R5wZaJzdBBVs"
# token = os.environ['CHAT_TOKEN']
# img_token = os.environ['IMG_TOKEN']
bot = telebot.TeleBot(bot_key)
# webhook = os.environ['WEBHOOK']
bot.delete_webhook()

# bot.set_webhook(url=webhook)

# generate LLM response with system message


@bot.message_handler(func=lambda message: not message.text.startswith('/'))
def generate_message(message):
    chat_id = message.chat.id
    prompt = message.text
    print(current_mode)
    reply = bot.send_message(chat_id, "Thinking...")

    # SORT OUT LLM CONFIG- NEED TO FIND A WAY TO SEPERATE THIS FUNCTION FOR BETTER READABILITY

    system_message = current_mode
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        system_message)
    human_message = prompt
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        human_message)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt])
    messages = chat_prompt.format_prompt().to_messages()
    response = chatbot(str(chat_prompt.format_prompt()))
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
        text='TeleChatGPT', url="webhook")
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


# define callback function for mode buttons
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    global current_mode
    current_mode = modes[call.data]
    bot.answer_callback_query(call.id, text="You have selected " + call.data)
    print(current_mode)

# define command handler to display mode buttons


@bot.message_handler(commands=['modes'])
def modes_handler(message):
    bot.send_message(
        message.chat.id, text="Please select a mode:", reply_markup=keyboard)


bot.polling()
