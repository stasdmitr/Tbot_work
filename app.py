import telebot
import requests
import json
from config import keys, TOKEN  # Импортируем ключи и токен из config.py
from utils import ConvertionException, CryptoConverter  # Импортировали классы из utils.py

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])  # Обработчик 1 - выводит инструкцию
def help(message: telebot.types.Message):
    text = 'Чтобы проверить мои знания введите :\n>Биткоин\Эфириум \
<Рубль\Доллар> \
<Какое количество>\n \
<Увидеть список доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])  # Обработчик 2
def values(message: telebot.types.Message):
    text = 'доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))  # Функция join (перенос строки)
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])  #  - конвертируем валюту.
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:  # Отлавливаю исключение
            raise ConvertionException('Беда с количеством параметров).')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Не совсем понял...\n{e}')

    except Exception as e:
        bot.reply_to(message, f'не удалось обработать\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
