import os
import telebot
import time
from flask import Flask, requests

bot_token = "824978965:AAHgrsGzKA_7moZBxDxO2dw2X1f2XJ9RV6Y"
bot = telebot.Telebot(token = bot_token)
server = Flask(__name__)

@bot.message_handler(command=['start'])
def send_message(message):
    bot.reply_to(message, 'Welcome!')


@bot.message_handler(msg.text is not None)
def send_message(message):
    bot.reply_to(message, message.text)


@server.route("/")
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(requests.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url = "https://telegarm-anan.herokuapp.com/" + bot_token)
    return "!", 200

if __name__ == "__main__":
    server.run(host = "0.0.0.0", port = int(os.environ.get("PORT", 5000)))