import os, time, random
import telebot
from flask import Flask, request, send_from_directory, send_file
from telebot import types
import Movies as mv
import Constellation

TOKEN = "824978965:AAGYUamuCMH_FupAN_z-axubukiiGB6Gd4g"
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)
#server.config['UPLOAD_FOLDER'] = '/upload'

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    chat_id = message.chat.id

    if message.text == "photo":
        #pass
        #可以傳本地圖片
        #bot.reply_to(message, os.getcwd())
        #os.chdir('/Users/clark.fang/Dropbox/Python/TelegarmBot')
        #photo = open('checked.png', 'rb')
        #bot.send_photo(chat_id, photo)
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(f"{ message.text } CLICK", callback_data='clicked'),
                   types.InlineKeyboardButton(f"{ message.text } CLICK 2", callback_data='clicked'))

        markup.add(types.InlineKeyboardButton("Google", url='http://www.google.com'))

        #也可以傳圖片的網址
        bot.send_photo(chat_id, "https://www.google.com/url?sa=i&url=https%3A%2F%2Fvocus.cc%2Facgntalk%2F5ae7dd37fd89780001a05755&psig=AOvVaw1tHmgG4-XKapNEfcMOTPW1&ust=1590807006141000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCLDL4IaI2OkCFQAAAAAdAAAAABAM")

    elif message.text == "電影" :
        moviesList = mv.get_movies()
        for item in range(0,3):
            randomItem = random.randint(0,len(moviesList))
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(f"點擊查看", url= moviesList[randomItem]['info_url']))
            bot.send_photo(chat_id, moviesList[randomItem]['poster_url'], reply_markup=markup)
            time.sleep(0.1)
    elif message.text.find('星座') != -1 and len(message.text) == 2:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("水瓶", callback_data='水瓶'),
                   types.InlineKeyboardButton("雙子", callback_data='雙子'),
                   types.InlineKeyboardButton("天秤", callback_data='天秤'))

        markup.add(types.InlineKeyboardButton("牡羊", callback_data='牡羊'),
                   types.InlineKeyboardButton("獅子", callback_data='獅子'),
                   types.InlineKeyboardButton("射手", callback_data='射手'))

        markup.add(types.InlineKeyboardButton("雙魚", callback_data='雙魚'),
                   types.InlineKeyboardButton("巨蟹", callback_data='巨蟹'),
                   types.InlineKeyboardButton("天蠍", callback_data='天蠍'))

        markup.add(types.InlineKeyboardButton("魔羯", callback_data='魔羯'),
                   types.InlineKeyboardButton("金牛", callback_data='金牛'),
                   types.InlineKeyboardButton("處女", callback_data='處女'))

        bot.send_message(chat_id, "----------請選擇星座----------", reply_markup=markup)

    elif message.text[0] == '星' and message.text[1] == '座' and message.text[2] == ' ':
        star = message.text.split('星座 ')[1]
        resultString = Constellation.constellation(star)
        bot.reply_to(message, resultString)

    else:
        #bot.reply_to(message, message.text)

        #蓋在鍵盤上面的選單
        # markup = types.ReplyKeyboardMarkup()
        # itembtna = types.KeyboardButton('a')
        # itembtnv = types.KeyboardButton('v')
        # itembtnc = types.KeyboardButton('c')
        # itembtnd = types.KeyboardButton('d')
        # itembtne = types.KeyboardButton('e')

        # markup.add(itembtnc, itembtnd, itembtne)
        # markup.add(itembtna, itembtnv)
        
        # markup.row(itembtna, itembtnv)
        # markup.row(itembtnc, itembtnd, itembtne)

        #在對話框bubble下面出現的選單 
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(f"{ message.text } CLICK", callback_data='clicked'),
                   types.InlineKeyboardButton(f"{ message.text } CLICK 2", callback_data='clicked'))

        markup.add(types.InlineKeyboardButton("Google", url='http://www.google.com'))
        bot.send_message(chat_id, "目前只有電影和星座 其他都是Echo", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'clicked')
def command_click_inline(call):
    chat_id = call.message.chat.id
    content = call.message.text

    #bot.send_message(chat_id, "InlineKeyboardButton")
    bot.answer_callback_query(call.id, text= f" Did receive { content } ")


#星座call back
@bot.callback_query_handler(func=lambda call: call.data)
def command_click_inline(call):
    chat_id = call.message.chat.id
    resultString = Constellation.constellation(call.data)
    bot.send_message(chat_id, resultString)


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
    #bot.set_webhook(url='https://ee36f7c6dae9.ngrok.io/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
    #server.run(host="127.0.0.1", port=int(os.environ.get('PORT', 5000)),debug=True)
