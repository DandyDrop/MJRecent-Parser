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
