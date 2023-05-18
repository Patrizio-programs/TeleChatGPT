import os
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.executor import start_webhook
from Bard import Chatbot

TOKEN = os.environ['BOT_KEY']
WEBHOOK_URL = os.environ['WEBHOOK']
IMG_API_URL = "https://openai80.p.rapidapi.com/images/generations"
headers = {
  "Content-Type": "application/json",
  "X-RapidAPI-Key": "4c695ea717mshd319d684b42713ap1035c3jsnaac2d74ef2c2",
  "X-RapidAPI-Host": "openai80.p.rapidapi.com"
}

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Define the response function
@dp.message_handler()
async def generate_message(message: types.Message):
    prompt = message.text
    chat_id = message.chat.id
    reply = await bot.send_message(chat_id, "Thinking...")
    chatbot = Chatbot(TOKEN)
    response_dict = chatbot.ask(prompt)
    response = response_dict['content']
    await bot.edit_message_text(chat_id=chat_id, message_id=reply.message_id, text=response)

# Define the start command
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, 'Enter a prompt, wait for a response.')

# Define the info command
@dp.message_handler(commands=['info'])
async def info_command(message: types.Message):
    chat_id = message.chat.id
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text='TeleChatGPT', url=WEBHOOK_URL)
    markup.add(button)
    await bot.send_message(
        chat_id,
        'TelechatGPT is powered by ChatGPT. Click the button below for more info:',
        reply_markup=markup)


@dp.message_handler(commands=['bots'])
async def bots_command(message: types.Message):
    chat_id = message.chat.id
    button = types.InlineKeyboardButton(
      text="More bots here!", url="https://t.me/PatrizioTheDevbot")
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(button)
    await bot.send_message(chat_id=chat_id,
                            text="To check on the other bots select the button",
                            reply_markup=keyboard)


@dp.message_handler(commands=['img'])
async def image_info(message: types.Message):
    if len(message.text.split()) == 1:
        await bot.send_message(
            message.chat.id,
            "Please send a prompt with the command to generate an image. For example /img a dancing giraffe."
        )
    else:
        prompt = message.text[5:]
        await bot.send_message(
            message.chat.id,
            "It can take a while to generate your image so please be patient")
        payload = {"prompt": prompt, "n": 2, "size": "1024x1024"}
        response = requests.post(IMG_API_URL, json=payload, headers=headers)
        response_dict = response.json()
        images_list = response_dict["data"]
        for image_dict in images_list:
            photo_url = image_dict["url"]
            await bot.send_photo(message.chat.id, photo_url)

# Register webhook handlers
async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dp):
    logging.warning('Shutting down..')
    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    # Remove webhook
    await bot.delete_webhook()

    # Cancel all tasks started by aiohttp (e.g. long polling)
    for task in asyncio.all_tasks():
        task.cancel()

    # Wait for all tasks to be cancelled
    await asyncio.gather(*asyncio.all_tasks())

    logging.warning('Bye!')

# Start the webhook
start_webhook(
    dispatcher=dp,
    webhook_path='/',
    on_startup=on_startup,
    on_shutdown=on_shutdown,
    skip_updates=True,
    host='0.0.0.0',
    port=int(os.environ.get('PORT', 5000))
)
