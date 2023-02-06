import os
import json
import flask
import time
from flask import Flask, request, Response
from bs4 import BeautifulSoup
import requests
import telebot

bot = telebot.TeleBot(os.environ.get("TOKEN"))
app = Flask(__name__)

@app.route('/', methods=['POST'])
def handle_request():
    bot.send_message("@logsmj", "Detected POST request (adaptime)")
    if request.form.get("pass") == None:
        bot.send_message("@logsmj", "Detected POST request without a pass!")
    elif request.form.get("pass") == "210123scasd1fcas":
        bot.send_message("@logsmj", "Detected POST request with a right pass!")
    else:
        bot.send_message("@logsmj", "Wrong pass")
    return ""


@app.route('/', methods=['HEAD'])
def handle_request():
    send_main()
    return ""
 
    
def send_main():
    response = requests.get("https://www.midjourney.com/showcase/recent/")
    soup = BeautifulSoup(response.text, 'html.parser')
    scripts = soup.find_all("script")
    for script in scripts:
        if script.get('id') != None:
            data = json.loads(script.text)
            jobs = data['props']['pageProps']['jobs']
            for job in jobs:
                bot.send_photo(
                    chat_id="@logsmj",
                    photo=job['image_paths'][0],
                    caption=job['full_command']
                )
                time.sleep(10)

            break

        
def main():
    send_main()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))
    
if __name__ == '__main__':
    main()
