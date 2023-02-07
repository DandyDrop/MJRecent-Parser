import os
import json
from flask import Flask, request
from bs4 import BeautifulSoup
import requests
import telebot

results_main = []
bot = telebot.TeleBot(os.environ.get("TOKEN"))
app = Flask(__name__)

@app.before_request
def handle():
    try:
        if request.method == 'POST':
            bot.send_message("@logsmj", "Detected POST request (FIRST)")
            get_main()
        elif request.method == 'HEAD':
            bot.send_message("@logsmj", "Detected HEAD request (FIRST)")
            send_main()
        else:
            bot.send_message("@logsmj", f"Detected some {request.method} request (FIRST)")
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
            for job in jobs:
                results_main.append({"link": job['image_paths'][0],
                                     "prompt": job['full_command']
                                     })

            break
            
    bot.send_message("652015662", f"Got {len(results_main)} new images!")
    
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
            if "Bad Request" in e and request.method == 'HEAD':
                continue
            else:
                break
        
        
def main():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))
    
if __name__ == '__main__':
    main()
