import telebot
import os
import random
from googletrans import Translator
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)
translator = Translator()


def import_english_words():
    """Return a list of words

    Getting all words from file and separate between them.
    """
    my_dir = os.path.dirname(__file__)
    txt_file_path = os.path.join(my_dir, 'english_words.txt')
    with open(txt_file_path) as file:
        data = file.read()

    words = data.split("-")
    return words


def get_random_word(words):
    """Return a String (a word)

    Choose random word from the list.
    """
    return words[random.randrange(len(words)-1)]


def get_translate(word):
    """Return a String

    translate the word from english to hebrew.
    If cant find translation delete this word from file and get a new word.
    """
    try:
        return translator.translate(word, dest='he', src='en').text

    except:
        english_words.remove(word)
        word = get_random_word(english_words)

    finally:
        return translator.translate(word, dest='he', src='en').text


def game_words(english_word):
    """Return an InlineKeyboardMarkup

    create 3 different translations to a word, only 2 are correct.
    :callback_data True: The correct translation.
    :callback_data False: Incorrect translation.
    """
    english_word_translated = get_translate(english_word)
    trash_translate1 = get_translate(get_random_word(english_words))
    trash_translate2 = get_translate(get_random_word(english_words))

    list_of_translations = [InlineKeyboardButton(english_word_translated, callback_data="True"),
                            InlineKeyboardButton(trash_translate1, callback_data="False"),
                            InlineKeyboardButton(trash_translate2, callback_data="False")]

    random.shuffle(list_of_translations)
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(list_of_translations[0], list_of_translations[1], list_of_translations[2])
    return markup


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Lets start. Tell me how you want to practice - \n "
                                      "/word - get a random word with translate \n "
                                      "/game - get a word and choose the correct translate")


@bot.message_handler(commands=['word'])
def send_word(message):
    english_word = get_random_word(english_words)
    english_word_translated = get_translate(english_word)
    bot.send_message(message.chat.id, "The word is: " + english_word + " \n The translate is " + english_word_translated)
    bot.send_message(message.chat.id, "Want another word? /word or maybe move to /game ?")
    bot.send_message(message.chat.id, "To cancel press /cancel")


@bot.message_handler(commands=['cancel'])
def send_cancel(message):
    bot.send_message(message.chat.id, "See you next time! press /start to start again.")


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    """Send message to user is his answer to the translation is true or false.

    """
    if call.data == "True":
        bot.send_message(call.message.chat.id, "Answer is correct! \n "
                                               "/new for another word. ")

        bot.send_message(call.message.chat.id, "/cancel to finish")

    elif call.data == "False":
        bot.send_message(call.message.chat.id, "Answer is not correct, try again. /cancel to finsh")


@bot.message_handler(commands=['game', 'new'])
def message_handler(message):
    english_word = get_random_word(english_words)
    bot.send_message(message.chat.id, english_word, reply_markup=game_words(english_word))


if __name__ == '__main__':
    english_words = import_english_words()
    bot.infinity_polling()


