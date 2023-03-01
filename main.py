import os
import json
from flask import Flask, request
from bs4 import BeautifulSoup
import requests
import telebot
import pyshorteners

sh = pyshorteners.Shortener()
USERNAMES = ["@", "@", os.getenv('LOGS_USERNAME'), "@"]
ADMIN_IDS = [652015662, 5412948297]
PASSWORDS = [os.getenv('MAIN_REQUEST_PASS'), os.getenv('SEND_TO_SECOND_PASS')]
results_main = []
the_bin = []
bot = telebot.TeleBot(os.getenv('TOKEN'))
app = Flask(__name__)
username_commands = ['change_main_username', 'change_file_username', 'change_logs_username', 'change_onem_username']


@app.before_request
def handle():
    try:
        if request.headers.get('content-type') != "application/json":
            ID = request.form.get(PASSWORDS[0])
            bot.send_message(USERNAMES[2],
                             f"Detected {request.method} request\nwith {ID} ID."
                             f"\n{len(results_main)} were seen in results_main.\n{len(the_bin)} "
                             f"were seen in bin\nUSERNAMES={USERNAMES}")
            if request.method == 'POST' and ID:
                if ID == "Awake":
                    return ""
                elif ID == "Send":
                    send_main(m="pass")
            else:
                bot.send_message(USERNAMES[2],
                                 f'Somebody tried with data: \n{str(request.form)}')
                return "No pass - @no_reception"

    except Exception as e:
        e = str(e)
        bot.send_message(USERNAMES[2], f"interesting error:\n{e}")


@app.route('/', methods=['POST', 'GET'])
def handle_admin():
    if request.headers.get('content-type') == "application/json":
        try:
            update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
            if update.message.from_user.id in ADMIN_IDS:
                bot.process_new_updates([update])
            return ""

        except Exception as e:
            bot.send_message('652015662',
                             f'error in handle_admin():\n{str(e)}')
            return ""

    return ""


@bot.message_handler(commands=['show_bin', 'show_main', 'show_pass'])
def send_all_in_bin(m):
    bot.send_message(USERNAMES[2],
                     f'Detected message with "show_bin" command\nfrom:\nid={m.chat.id}')
    command = m.text[1:]
    all_str = ""
    if command == 'show_bin':
        for link in the_bin:
            all_str += f"{link[8:]}\n\n"
    elif command == 'show_main':
        for image in results_main:
            all_str += f'{image["link"]}\n'
    elif command == 'show_pass':
        for password in PASSWORDS:
            all_str += f'{password}\n'
    bot.send_message(m.chat.id, all_str)


@bot.message_handler(commands=username_commands)
def change_main_username(m):
    bot.send_message(USERNAMES[2],
                     f"Detected message with some username changing command\nfrom:\nid={m.chat.id}")
    for i, com in enumerate(username_commands):
        if com == m.text[1:m.text.index(" ")]:
            bot.send_message(USERNAMES[2], f"Before changing USERNAMES=\n{USERNAMES}")
            USERNAMES[i] = m.text[m.text.index(" ") + 1:]
            bot.send_message(USERNAMES[2], f"Now USERNAMES=\n{USERNAMES}")
            break


@bot.message_handler(commands=['push_to_bin'])
def pusher_to_bin(m):
    for i in range(int(m.text[13:])):
        try:
            image = results_main.pop()
            bot.send_message(m.chat.id,
                             text=f"Pushing {i}...")
            bot.send_photo(m.chat.id,
                           photo=image['link'],
                           caption=image['prompt'],
                           parse_mode="Markdown")
            the_bin.append(image)

        except Exception as e:
            bot.send_message(m.chat.id, f"Error:\n{str(e)}")


@bot.message_handler(commands=['renew'])
def get_main(m):
    results_main.clear()
    response = requests.get("https://www.midjourney.com/showcase/recent/")
    soup = BeautifulSoup(response.text, 'html.parser')
    scripts = soup.find_all("script")
    try:
        for script in scripts:
            if script.get('id'):
                data = json.loads(script.text)
                jobs = data['props']['pageProps']['jobs']
                for job in jobs:
                    if job['image_paths'][0] not in the_bin and job['image_paths'][0] not in results_main:
                        url_sh = sh.tinyurl.short(job['image_paths'][0])
                        results_main.append({"link": url_sh,
                                             "prompt": f"{refactor_caption(job['full_command'])}"
                                                       f"\n\nUse this image as reference:\n{url_sh[8:]}"
                                             })
                break
    except Exception as e:
        bot.send_message(USERNAMES[2],
                         f"Got the error in get_main:\n{str(e)}\n\nFirst 2000 symbols of soup:"
                         f"\n{str(soup)[:2000]}\n\nscripts=:\n{str(scripts)}")
    bot.send_message(USERNAMES[2], f"Got {len(results_main)} new images!")


@bot.message_handler(commands=['send'])
def send_main(m):
    if "@" in USERNAMES:
        bot.send_message(USERNAMES[2], "The bot needs to be taken care of ;(")
    elif len(results_main) != 0:
        for i in range(3):
            image = results_main.pop()
            if len(the_bin) > 200:
                del the_bin[0]
            the_bin.append(image["link"])
            try:
                send(image)
                break

            except Exception as e:
                e = str(e)
                if i == 0:
                    bot.send_message(USERNAMES[2], f"Error in send_main():\n{e}\n"
                                                   "\ntrying to send(image) one more time...")
                    send(image)
                if "Bad Request" not in e:
                    break

        bot.send_message(USERNAMES[2],
                         f"{len(results_main)} left in results_main."
                         f"\n{the_bin[0][20:]} - first in bin.")

    else:
        bot.send_message(USERNAMES[2], 'No images, called get_main(m="pass")')
        get_main(m="pass")


def send(image):
    bot.send_photo(
        chat_id=USERNAMES[0],
        photo=image["link"],
        caption=image["prompt"],
        parse_mode="Markdown"
    )
    bot.send_photo(
        chat_id=USERNAMES[3],
        photo=image["link"],
        caption=image["prompt"],
        parse_mode="Markdown"
    )
    requests.post(os.getenv('LINK_TO_SAVE'),
                  data={
                      PASSWORDS[1]: "asdc23sdn213",
                      "link": image["link"],
                      "prompt": image["prompt"],
                      "user": USERNAMES[1]
                  }
                  )


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
    app.run(host='0.0.0.0', port=os.getenv("PORT", 3000))


if __name__ == '__main__':
    main()







