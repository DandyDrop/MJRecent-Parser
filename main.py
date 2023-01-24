import os
import time
import json
import flask
from flask import Flask, request, Response
from bs4 import BeautifulSoup
import requests
import telebot

# bot = telebot.TeleBot(os.environ.get("TOKEN"))
bot = telebot.TeleBot(os.environ.get("TOKEN"))
app = Flask(__name__)
# results_main = []
# main_dict = {}


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


app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))
    # time.sleep(86400)
