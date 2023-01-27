import os
import json
import flask
from flask import Flask, request, Response
from bs4 import BeautifulSoup
import requests
import telebot

bot = telebot.TeleBot(os.environ.get("TOKEN"))
app = Flask(__name__)
results_main = []
main_dict = {}


@app.route('/', methods=['HEAD'])
def handle_head():
    bot.send_message("652015662", "HEAD ;(")
    renew_main()
    return ""


@app.route('/', methods=['POST', 'GET'])
def handle_request():
    if request.headers.get('content-type') == "application/json":
        update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
        bot.process_new_updates([update])
        return ""
    else:
        flask.abort(403)

    if request.method == "POST":
        return Response("OK", status=200)
    else:
        return ""


@bot.message_handler(commands=["start"])
def on_start(m):
    bot.send_message(chat_id=m.chat.id,
                     text="Hello. I can send you great arts from midjourney.com/showcase/recent with prompts."
                          "With me you can learn how to write your own text instructions and have a joy seeing cool pics, of course ;)"
                          'Send "/renew" if you want to make fresh images avaible for you. Get your images by sending "/image"')


@bot.message_handler(commands=["renew"])
def renew(m):
    main_dict[m.chat.id] = results_main.copy()
    bot.send_message(chat_id=m.chat.id, text='Your list of images was updated! Send "/image" to see ;) ')

    
@bot.message_handler(commands=["image"])
def sendNewImage(m):
    try:
        if len(main_dict[m.chat.id]) != 0:
            image = main_dict[m.chat.id].pop()
            bot.send_photo(
                chat_id=m.chat.id,
                photo=image["link"],
                caption=image["prompt"]
            )
        else:
            bot.send_message(chat_id=m.chat.id, text='You saw all images. Use "/renew" to see more or take a closer look to the images above ;) ')

    except KeyError:
#         bot.send_message(chat_id="@logsmj", text=str(e))
        bot.send_message(chat_id=m.chat.id, text='Looks like I got no images for you. Try to "/renew"')


def renew_main():
    results_main.clear()
    response = requests.get("https://www.midjourney.com/showcase/recent/")
    soup = BeautifulSoup(response.text, 'html.parser')
    scripts = soup.find_all("script")
    for script in scripts:
        if script.get('id') != None:
            data = json.loads(script.text)
            jobs = data['props']['pageProps']['jobs']
            for job in jobs:
                results_main.append({"link": job['image_paths'][0],
                                     "prompt": job['full_command']
                                     })

            break


renew_main()
app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))
