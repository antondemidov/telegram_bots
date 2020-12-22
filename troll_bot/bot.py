import telebot
import random
import requests
import shutil
import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.getLevelName(os.getenv("LOGLEVEL", "INFO")))
try:
    TOKEN = os.getenv("TELEGRAM_BOT")
except Exception as e:
    logger.info("you don't have token in ENV variables")
    sys.exit

bot = telebot.TeleBot(TOKEN)
phrase_list = [
    "SOME",
    "PHRASES",
    "YOU",
    "NEED",
    ":)",
]


@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id, "Привет, я Бот Алеша")


@bot.message_handler(content_types=["text"])
def send_text(message):
    if (
        ("PHRASE_TO_CATCH" in message.text.lower())
    ):
        bot.send_message(message.chat.id, random.choice(phrase_list))
    elif "WEATHER" in message.text.lower():
        w = requests.get("https://wttr.in/Kyiv.png", stream=True)
        with open("img.png", "wb") as out_file:
            shutil.copyfileobj(w.raw, out_file)
        bot.send_photo(message.chat.id, photo=open("img.png", "rb"))


bot.polling()
