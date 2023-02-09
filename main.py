import os
import json
from datetime import datetime
from flask import Flask, request, Response
from bs4 import BeautifulSoup
import requests
import telebot

prev_utc = "No date"
results_main = []
bot = telebot.TeleBot(os.environ.get("TOKEN"))
app = Flask(__name__)


@app.before_request
def handle():
    try:
        ip = request.remote_addr
        bot.send_message("@logsmj", f"Detected {request.method} request (FIRST) from {ip}")
        if request.method == 'POST':
            if request.form.get(os.environ.get("PASS")) != None:
                get_main()
            else:
                bot.send_message("@logsmj", f'Somebody tried with wrong pass: {request.form.get(os.environ.get("PASS"))}')
                return Response("No pass - @no_reception", status=403)

        elif request.method == 'HEAD':
            send_main()

    except Exception as e:
        e = str(e)
        bot.send_message("@logsmj", f"interesting error:\n{e}")

    return ""


def get_main():
    results_main.clear()
    response = requests.get("https://www.midjourney.com/showcase/recent/")
    soup = BeautifulSoup(response.text, 'html.parser')
    scripts = soup.find_all("script")
    for script in scripts:
        if script.get('id') != None:
            data = json.loads(script.text)
            jobs = data['props']['pageProps']['jobs']
            if now_utc == "No date":
                for job in jobs:
                    results_main.append({"link": job['image_paths'][0],
                                         "prompt": job['full_command']
                                         })
            else:
                for job in jobs:
                    if prev_utc.day <= day_job and prev_utc.hour <= hour_job and prev_utc.minute <= min_job: 
                        results_main.append({"link": job['image_paths'][0],
                                             "prompt": job['full_command']
                                             })

            break
            
    prev_utc = datetime.now().utcnow()
    bot.send_message("652015662", f"Got {len(results_main)} new images!\nTime set to {str(prev_utc)}")


def send_main():
    for i in range(3):
        try:
            if len(results_main) != 0:
                image = results_main.pop()
                bot.send_photo(
                    chat_id="@mjrecent",
                    photo=image["link"],
                    caption=image["prompt"]
                )
            else:
                bot.send_message("@logsmj", "No images")

            break
        except Exception as e:
            e = str(e)
            bot.send_message("@logsmj", f"error:\n{e}")
            if "Bad Request" in e:
                continue
            else:
                break


def main():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))


if __name__ == '__main__':
    main()
