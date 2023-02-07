@bot.message_handler(commands=["image"])
def sendNewImage(m):
    try:
        if len(main_dict[m.chat.id]) != 0:
            image = main_dict[m.chat.id].pop()
            bot.send_photo(
                chat_id=m.chat.id,
                photo=image["link"],
                caption=image["prompt"],
                reply_markup=markup
            )
        else:
            bot.send_message(chat_id=m.chat.id, text='You saw all images. Use "/renew" to see more or take a closer look to the images above ;) ')

    except KeyError:
#         bot.send_message(chat_id="@logsmj", text="")
        bot.send_message(chat_id=m.chat.id, text='Looks like I got no images for you. Try to "/renew"')
    
    
# @app.route('/', methods=['HEAD'])
# def handle_request():
#     bot.send_message("@logsmj", "Detected HEAD request (adaptime)")
#     send_main()
#     return ""

# @app.route('/', methods=['POST'])
# def handle_request1():
#     bot.send_message("@logsmj", "Detected POST request (adaptime)")
#     get_main()
#     return ""

# @app.route('/', methods=['POST'])
# def handle_request():
#     bot.send_message("@logsmj", "Detected POST request (adaptime)")
#     if request.form.get("pass") == None:
#         bot.send_message("@logsmj", "Detected POST request without a pass!")
#     elif request.form.get("pass") == "210123scasd1fcas":
#         bot.send_message("@logsmj", "Detected POST request with a right pass!")
#     else:
#         bot.send_message("@logsmj", "Wrong pass")
#     return ""
