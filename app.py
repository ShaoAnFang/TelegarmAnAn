import os
import telebot
import time
from flask import Flask, requests

bot_token = "824978965:AAGYUamuCMH_FupAN_z-axubukiiGB6Gd4g"
bot = telebot.Telebot(token = bot_token)
server = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)
 
@server.route('/' + bot_token, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url = "https://telegarm-anan.herokuapp.com/" + bot_token)
    return "!", 200

if __name__ == "__main__":
    server.run(host = "0.0.0.0", port = int(os.environ.get("PORT", 5000)))