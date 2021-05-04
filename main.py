import requests
import json
import time
import re
import telebot
from bs4 import BeautifulSoup
#import telegram

TOKEN = "1761043291:AAEdj2o3zXHMvNNb83jpLqZvxfdwNrS5aas"
bot = telebot.TeleBot(TOKEN)


html = requests.get('https://www.rbc.ru/story/')

soup = BeautifulSoup(html.text, 'html.parser')


@bot.message_handler(commands=['help'])
def help_command(massage):
    bot.send_message(massage.from_user.id, "help - показать все, что может бот\n"
                                           "new_docs <N> - показать N самых свежих новостей\n"
                                           "new_topics <N> - показать N самых свежих тем\n"
                                           "topic <topic_name> - показать описание темы "
                                           "и заголовки 5 самых свежих новостей в этой теме\n"
                                           "doc <doc_title> - показать текст документа с заданным заголовком\n"
                                           "words <topic_name> - показать 5 слов, лучше всего характеризующих тему\n"
                                           "describe_doc <doc_title> - вывести статистику по документу. Статистика:\n"
                                           "    распределение частот слов\n"
                                           "    распределение длин слов\n"
                                           "describe_topic <topic_name> - вывести статистику по теме. Статистика:\n"
                                           "    количество документов в теме\n"
                                           "    средняя длина документов\n"
                                           "    распределение частот слов в рамках всей темы\n"
                                           "    распределение длин слов в рамках всей темы\n")


@bot.message_handler(commands=['new_docs'])
def new_docs_command(message):
    file = open('TimurHTML.txt', 'w')
    file.write(soup.prettify())
    num = 1
    try:
        num = int((message.text.split(sep=' '))[1])
    except Exception:
        pass
    text = soup.find_all('a', class_="news-feed__item js-news-feed-item js-yandex-counter")
    print(text)
    for i in range(0, min(len(text), num)):
        splited_text_for_name = re.split('<span class="news-feed__item__title news-feed__item_in-main">\n            '
                                '|<span class="news-feed__item__title">\n            |\n        </span>', str(text[i]))
        splited_text_for_desc = re.split('-->|<!--', str(text[i]))
        splited_text_for_url = re.split(' href="|" id', str(text[i]))
        bot.send_message(message.from_user.id,  splited_text_for_desc[2] + '\n' + splited_text_for_name[1] + '\n' + splited_text_for_url[1])


@bot.message_handler(commands=['new_topics'])
def new_topics_command(message):
    file = open('TimurHTML.txt', 'w')
    file.write(soup.prettify())
    num = 1
    try:
        num = int((message.text.split(sep=' '))[1])
    except Exception:
        pass
    text = soup.find_all('a', class_="item__link")
    print(text)
    for i in range(0, min(len(text), num)):
        splited_text_for_name = re.split('<span class="item__title rm-cm-item-text">\n                                                                    |'
                                         '\n                                                            </span>', str(text[i]))
        splited_text_for_url = re.split(' href="|">', str(text[i]))
        bot.send_message(message.from_user.id,  splited_text_for_name[1] + '\n' + splited_text_for_url[1])


bot.polling(none_stop=True, interval=0)
