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


@bot.message_handler(commands=["renew"])
def randomMJRecent(m):
    bot.send_message(m.chat.id, "Anus")


def main():
    bot.send_message(chat_id="652015662", text="Executed the main func")
#     results_main.clear()
#     response = requests.get("https://www.midjourney.com/showcase/recent/")
#     soup = BeautifulSoup(response.text, 'html.parser')
#     scripts = soup.find_all("script")
#     for script in scripts:
#         try:
#             bot.send_message(chat_id="652015662", text=f"Sending {script['id'][7:-2].lower()}...")
#             data = json.loads(script.text)
#             jobs = data['props']['pageProps']['jobs']
#             for job in jobs:
#                 results_main.append({"link": job['image_paths'][0],
#                                      "prompt": job['full_command']
#                                      })

#         except KeyError:
#             continue

while True:
    main()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))
    time.sleep(10)
    # time.sleep(86400)
