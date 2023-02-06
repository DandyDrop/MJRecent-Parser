import os
import json
import flask
from flask import Flask, request, Response
from bs4 import BeautifulSoup
import requests
import telebot

bot = telebot.TeleBot(os.environ.get("TOKEN"))
app = Flask(__name__)
# results_main = []
# main_dict = {}


@app.route('/', methods=['POST'])
def handle_request():
    bot.send_message("@logsmj", "Detected POST request (adaptime)")
    if request.form.get("pass") == None:
        bot.send_message("@logsmj", "Detected POST request without a pass!")
    elif request.form.get("pass") == "210123scasd1fcas":
        bot.send_message("@logsmj", "Detected POST request with a right pass!")
    return ""


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

        
def main():
#     renew_main()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))
    
if __name__ == '__main__':
    main()
