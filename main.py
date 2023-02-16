import os
import json
from flask import Flask, request, Response
from bs4 import BeautifulSoup
import requests
import telebot

USERNAMES = ["@", "@", "@"]
ADMIN_IDS = [652015662]
results_main = []
the_bin = []
bot = telebot.TeleBot(os.environ.get("TOKEN"))
app = Flask(__name__)
username_commands = ['change_main_username', 'change_file_username', 'change_logs_username']

@app.before_request
def handle():
    try:
        if request.headers.get('content-type') != "application/json":
            ID = request.form.get(os.environ.get("PASS"))
            bot.send_message(os.environ.get("LOGS_USERNAME"),
                             f"Detected {request.method} request \nwith {ID} ID."
                             f"\n{len(results_main)} were seen in results_main.\n{len(the_bin)} "
                             f"were seen in bin\nUSERNAMES={str(USERNAMES)}")
            if request.method == 'POST' and ID != None:
                if ID == "Awake":
                    return ""
                elif ID == "Send":
                    send_main()
            else:
                bot.send_message(os.environ.get("LOGS_USERNAME"),
                                 f'Somebody tried with data: \n{str(request.form)}')
                return Response("No pass - @no_reception", status=403)

    except Exception as e:
        e = str(e)
        bot.send_message(os.environ.get("LOGS_USERNAME"), f"interesting error:\n{e}")


@app.route('/', methods=['POST', 'GET'])
def handle_admin():
    if request.headers.get('content-type') == "application/json":
        update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
        bot.process_new_updates([update])
        return ""

    if request.method == "POST":
        return Response("OK", status=200)
    else:
        return ""


@bot.message_handler(commands=username_commands)
def change_main_username(m):
    try:
        bot.send_message(os.environ.get("LOGS_USERNAME"),
                         f"Detected message with some user changing command\nfrom:\nid={m.chat.id}")
        if m.chat.id in ADMIN_IDS:
            for i, com in enumerate(username_commands):
                if com == m.text[1:21]:
                    change_usernames(m.text[22:], i)
                    break
    except Exception as e:
        e = str(e)
        bot.send_message(os.environ.get("LOGS_USERNAME"), f"interesting error:\n{e}")                


def change_usernames(username, pointer):
    bot.send_message(os.environ.get("LOGS_USERNAME"), f"Before changing user=\n{USERNAMES[pointer]}")
    USERNAMES[pointer] = username
    bot.send_message(os.environ.get("LOGS_USERNAME"), f"After changing user=\n{USERNAMES[pointer]}")


def get_main():
    response = requests.get("https://www.midjourney.com/showcase/recent/")
    soup = BeautifulSoup(response.text, 'html.parser')
    scripts = soup.find_all("script")
    for script in scripts:
        if script.get('id') != None:
            data = json.loads(script.text)
            jobs = data['props']['pageProps']['jobs']
            for job in jobs:
                if job['image_paths'][0] not in the_bin:
                    results_main.append({"link": job['image_paths'][0],
                                         "prompt": refactor_caption(job['full_command'])
                                         })

            break

    bot.send_message(os.environ.get("LOGS_USERNAME"), f"Got {len(results_main)} new images!")


def send_main():
    for i in range(3):
        try:
            if "@" in USERNAMES:
                bot.send_message(os.environ.get("LOGS_USERNAME"), "The bot needs to be taken care of ;(")
            elif len(results_main) != 0:
                image = results_main.pop()
                if len(the_bin) > 200:
                    del the_bin[0]
                the_bin.append(image["link"])
                bot.send_photo(
                    chat_id=USERNAMES[0],
                    photo=image["link"],
                    caption=image["prompt"],
                    parse_mode="Markdown"
                )
                requests.post("https://totest.adaptable.app",
                              data={
                                  os.environ.get("FILES_PASS"): "asdc23sdn213",
                                  "link": image["link"],
                                  "prompt": image["prompt"],
                                  "user": USERNAMES[1]
                                    }
                              )
                bot.send_message(os.environ.get("LOGS_USERNAME"),
                     f"{len(results_main)} left in results_main.\n{the_bin[0][27:-8]}\n-- first in bin.")
                
            else:
                bot.send_message(os.environ.get("LOGS_USERNAME"), "No images, called get_main()")
                get_main()
                continue
                
            break

        except Exception as e:
            e = str(e)
            bot.send_message(os.environ.get("LOGS_USERNAME"), f"error:\n{e}")
            if "Bad Request" not in e:
                break


def refactor_caption(caption):
    links = ""
    save = ""
    while caption.find("<https://") != -1:
        if caption.index("<https://") != 0:
            save += caption[:caption.index("<https://") - 1]
        caption = caption[caption.index("<https://") + 9:]
        links += caption[:caption.index(">")] + "\n"
        caption = caption[caption.index(">") + 1:]
    final = save + caption
    shit = [',', '-', '.', " "]
    while final[0] in shit:
        final = final[1:]

    return f"{links}\n`{final}`"


def main():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))


if __name__ == '__main__':
    main()
