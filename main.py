import os
import time
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
    bot.send_message(chat_id="652015662", text="Ye")         
    renew()
    return Response("OK", status=200)

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
    
    
@bot.message_handler(commands=["start", "renew"])
def start_set(m):
    bot.send_message(chat_id=m.chat.id, text='New images are here! Send "/photo" to see ;) ')
    main_dict[m.chat.id] = results_main
    
    
@bot.message_handler(commands=["photo"])
def sendNewImage(m):
    image = main_dict[m.chat.id].pop()
    bot.send_photo(
        chat_id=m.chat.id,
        photo=image["link"],
        caption=image["prompt"]
    )
    for key in main_dict:
        bot.send_message(chat_id="652015662", text=key)
        bot.send_message(chat_id="652015662", text=len(main_dict[key]))

    
def renew():
    bot.send_message(chat_id="652015662", text="Executed the main func")
    results_main.clear()
    response = requests.get("https://www.midjourney.com/showcase/recent/")
    soup = BeautifulSoup(response.text, 'html.parser')
    scripts = soup.find_all("script")
    for script in scripts:
        try:
            bot.send_message(chat_id="652015662", text=f"Getting {script['id'][7:-2].lower()}...")
            data = json.loads(script.text)
            jobs = data['props']['pageProps']['jobs']
            bot.send_message(chat_id="652015662", text=f"Got {len(jobs)} arts")
            for job in jobs:
                results_main.append({"link": job['image_paths'][0],
                                     "prompt": job['full_command']
                                     })

        except KeyError:
            continue

renew()           
app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))
