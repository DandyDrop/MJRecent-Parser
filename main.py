import os
import time
import json
import flask
from flask import Flask, request, Response
from bs4 import BeautifulSoup
import requests
import telebot

app = Flask(__name__)
bot = telebot.TeleBot("5809276134:AAGuKn5wiaMqQwB_7_yce0_mHLufcdvn4eA")
results_main = []

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

def main():
    results_main.clear()
    response = requests.get("https://www.midjourney.com/showcase/recent/")
    soup = BeautifulSoup(response.text, 'html.parser')
    scripts = soup.find_all("script")
    print(str(soup) + "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print("scripts:\n" + str(scripts) + "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    for script in scripts:
        try:
            bot.send_message(chat_id="652015662", text=f"Sending {script['id'][7:-2].lower()}...")
            data = json.loads(script.text)
            jobs = data['props']['pageProps']['jobs']
            for job in jobs:
                results_main.append({"link": job['image_paths'][0],
                                     "prompt": job['full_command']
                                     })

        except KeyError:
            continue

    bot.send_photo(chat_id="652015662", photo=results_main[0]['link'], caption=results_main[0]['prompt'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))
    print("Calling main...")
    main()

print(results_main)

