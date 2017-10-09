from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
import requests
import json

from telegram.replykeyboardremove import ReplyKeyboardRemove

updater = Updater('449150567:AAFwxZjQO_BrE1RVe4qH467vIiDlRD7Hu24')

states = {}
id_global_1 = -1


def get_genre_list():
    data = json.loads(requests.get('http://127.0.0.1:8000/genreList/').text)
    return data


def get_dialog_list(id_post):
    r = requests.post('http://127.0.0.1:8000/dialogListByGenreId/', json={"genre_id": id_post})
    data = r.json()
    return data


def get_dialog_text_list(id_post):
    r = requests.get('http://127.0.0.1:8000/getDialogById/{0}'.format(id_post))
    return r.json()


START = 'start'
CHOICE_GENRE = 'choice-genre'
CHOICE_DIALOG = 'choice-dialog'
CHOICE_DIALOG_TEXT = 'choice-dialog-text'
END = 'end'


def start(bot, update):
    global states
    states[update.message.chat_id] = {'step': START}
    main_function(bot, update)


def help(bot, update):
    bot.send_message(update.message.chat_id, "Hello, it's Majara Bot and Welcome to our Bot.")


def end_function(bot, update):
    bot.send_message(update.message.chat_id, "Thank You For Using This Bot!")


def main_function(bot, update):
    global states, id_global_1
    chat_id = update.message.chat_id
    if chat_id in states:
        step = states[chat_id]['step']
        if step == START:
            g_list = get_genre_list()
            keyboard = []
            for genre in g_list:
                title = genre.get('title', '')
                keyboard.append([title])
            keyboard.append(['Exit'])
            markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            bot.send_message(chat_id, "Genre's:", reply_markup=markup)
            states[chat_id]['step'] = CHOICE_GENRE
        if step == CHOICE_GENRE:
            text = update.message.text
            if text == "Exit":
                end_function(bot, update)
            g_list = get_genre_list()
            for genre in g_list:
                title_get = genre.get('title', '')
                id_get = genre.get('id')
                if title_get == text:
                    id_global_1 = update.message.text = id_get
                    data = get_dialog_list(update.message.text)
                    keyboard = []
                    for dialog in data:
                        title = dialog.get('title')
                        keyboard.append([title])
                    keyboard.append(['Back'])
                    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
                    bot.send_message(chat_id, "Dialog's:", reply_markup=markup)
                    if len(keyboard) > 1:
                        states[chat_id]['step'] = CHOICE_DIALOG
                    else:
                        markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
                        bot.send_message(chat_id, "Dialog List is Empty.", reply_markup=markup)
                        states[chat_id]['step'] = CHOICE_DIALOG

        if step == CHOICE_DIALOG:
            if update.message.text == 'Back':
                start(bot, update)

            data = get_dialog_list(id_global_1)
            for dialog in data:
                title_get = dialog.get('title')
                id_get = dialog.get('id')
                if title_get == update.message.text:
                    update.message.text = id_get
            data = get_dialog_text_list(update.message.text)[0]
            dialog_text = data.get('Dialog_Text')
            list_show = []
            for dialog in dialog_text:
                dialog_id = dialog[0]
                dialog_from = dialog[1]
                dialog_text = dialog[3]
                dialog_type = dialog[2]
                dialog_image = dialog[4]
                data = "Dialog ID: {0}\n" \
                       "Dialog From: {1}\nDialog Text: {2}" \
                       "\nType: {3}\nImage:{4}".format(dialog_id, dialog_from, dialog_text, dialog_type, dialog_image)
                list_show.append(data)
                bot.send_message(update.message.chat_id, data)


def main():
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(MessageHandler([Filters.text], main_function))
    updater.start_polling()


if __name__ == '__main__':
    main()
