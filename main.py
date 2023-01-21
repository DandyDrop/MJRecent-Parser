import random
from bs4 import BeautifulSoup
import requests
import telebot
import json

bot = telebot.TeleBot("YOUR_BOT_TOKEN")
@bot.message_handler(commands=["rmj"])
def randomMJRecent(message):
    response = requests.get("https://www.midjourney.com/showcase/recent/")
    soup = BeautifulSoup(response.text, 'html.parser')
    scripts = soup.find_all("script")
    for script in scripts:
        try:
            bot.send_message(chat_id=message.from_user.id, text=f"Sending {script['id'][7:-2].lower()}...",
                             parse_mode='html')
            data = json.loads(script.text)
            jobs = data['props']['pageProps']['jobs']
            random.shuffle(jobs)
            job = jobs[0]
            image_url = job['image_paths'][0]
            bot.send_photo(
                chat_id=message.from_user.id,
                photo=image_url,
                caption=job['full_command']
            )
        except KeyError:
            continue

bot.polling()

