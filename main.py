import requests
import json
import time
import re
import telebot
from bs4 import BeautifulSoup
#import telegram

TOKEN = "TOKEN"
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
    num = 1
    try:
        num = int((message.text.split(sep=' '))[1])
    except Exception:
        pass
    text = soup.find_all('a', class_="news-feed__item js-news-feed-item js-yandex-counter")
    for i in range(0, min(len(text), num)):
        splited_text_for_name = re.split('<span class="news-feed__item__title news-feed__item_in-main">\n            '
                                '|<span class="news-feed__item__title">\n            |\n        </span>', str(text[i]))
        splited_text_for_desc = re.split('-->|<!--', str(text[i]))
        splited_text_for_url = re.split(' href="|" id', str(text[i]))
        bot.send_message(message.from_user.id,  splited_text_for_desc[2] + '\n' + splited_text_for_name[1] + '\n' + splited_text_for_url[1])


@bot.message_handler(commands=['new_topics'])
def new_topics_command(message):
    num = 1
    try:
        num = int((message.text.split(sep=' '))[1])
    except Exception:
        pass
    text = soup.find_all('a', class_="item__link")
    for i in range(0, min(len(text), num)):
        splited_text_for_name = re.split('<span class="item__title rm-cm-item-text">\n                                                                    |'
                                         '\n                                                            </span>', str(text[i]))
        splited_text_for_url = re.split(' href="|">', str(text[i]))
        bot.send_message(message.from_user.id,  splited_text_for_name[1] + '\n' + splited_text_for_url[1])


@bot.message_handler(commands=['topic'])
def topic_command(message):
    text = soup.find_all('a', class_="item__link")
    topic_name = "".join(list(message.text)[list(message.text).index(' ') + 1:])
    names_of_topics = []
    urls_of_topics = []
    for i in text:
        names_of_topics.append((re.split('<span class="item__title rm-cm-item-text">\n                                                                    |'
                                         '\n                                                            </span>', str(i)))[1])
        urls_of_topics.append(re.split(' href="|">', str(i))[1])
    ind = 0
    try:
        ind = names_of_topics.index(topic_name)
    except Exception:
        pass
    needed_url = urls_of_topics[ind]
    html_of_needed_site = requests.get(needed_url)
    soup_of_needed_site = BeautifulSoup(html_of_needed_site.text, 'html.parser')
    text = soup_of_needed_site.find_all('a', class_="item__link")
    for i in range(0, 5):
        splited_text_for_name = re.split(
            '<span class="item__title rm-cm-item-text">\n                                                                    |'
            '\n                                                            </span>', str(text[i]))
        splited_text_for_url = re.split(' href="|">', str(text[i]))
        bot.send_message(message.from_user.id, splited_text_for_name[1] + '\n' + splited_text_for_url[1])


@bot.message_handler(commands=['doc'])
def doc_command(message):
    text = soup.find_all('a', class_="item__link")
    subtopic_name = "".join(list(message.text)[list(message.text).index(' ') + 1:])
    names_of_topics = []
    urls_of_topics = []
    for i in text:
        names_of_topics.append((re.split('<span class="item__title rm-cm-item-text">\n                                                                    |'
                                         '\n                                                            </span>', str(i)))[1])
        urls_of_topics.append(re.split(' href="|">', str(i))[1])
    names_of_subtopics = []
    urls_of_subtopics = []
    for i in urls_of_topics:
        html_of_subtopics = requests.get(i)
        soup_of_subtopics = BeautifulSoup(html_of_subtopics.text, 'html.parser')
        text = soup_of_subtopics.find_all('a', class_="item__link")
        for j in text:
            names_of_subtopics.append(re.split('<span class="item__title rm-cm-item-text">\n                                                                    |'
                                             '\n                                                            </span>', str(j))[1])
            urls_of_subtopics.append(re.split(' href="|">', str(j))[1])
    needed_url = urls_of_subtopics[names_of_subtopics.index(subtopic_name)]
    html_of_needed_subtopic = requests.get(needed_url)
    soup_of_needed_subtopic = BeautifulSoup(html_of_needed_subtopic.text, 'html.parser')
    telegram_text = soup_of_needed_subtopic.find_all('p')
    bot.send_message(message.from_user.id, needed_url)


bot.polling(none_stop=True, interval=0)
