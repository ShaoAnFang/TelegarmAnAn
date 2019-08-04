import os
import telebot
import time
from flask import Flask, requests

bot_token = "824978965:AAGYUamuCMH_FupAN_z-axubukiiGB6Gd4g"
bot = telebot.Telebot(token = bot_token)
server = Flask(__name__)

@bot.message_handler(command=['start'])
def send_message(message):
    bot.reply_to(message, 'Welcome!')


@bot.message_handler(func=lambda msg: msg.text is not None and '@' in msg.text)
# lambda function finds messages with the '@' sign in them
# in case msg.text doesn't exist, the handler doesn't process it
def at_converter(message):
    texts = message.text.split()
    at_text = findat(texts)
    if at_text == '@': # in case it's just the '@', skip
        pass
    else:
        insta_link = "https://instagram.com/{}".format(at_text[1:])
        bot.reply_to(message, insta_link)


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