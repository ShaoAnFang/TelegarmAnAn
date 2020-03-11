import os
from flask import Flask, request, send_from_directory, send_file, url_for

TOKEN = "824978965:AAGYUamuCMH_FupAN_z-axubukiiGB6Gd4g"
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)
server.config['UPLOAD_FOLDER'] = '/upload'

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route('/edm2020_01/<string:filename>')
def returnImagez(filename):
    return send_file('/app/upload/{}'.format(filename))

@server.route('/edm2020_02/<string:filename>')
def returnImage(filename):
    #return str(os.getcwd())
    #return str(os.listdir()) 
    #['upload', 'runtime.txt', 'README.md', 'app.py', 'Procfile', '.heroku', 'requirements.txt', '.profile.d']
    return send_file('/app/upload/{}'.format(filename))
    #return send_from_directory(server.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://telegarm-anan.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
