from config import API_TOKEN, greeting, commands, faq, helper, user_manual
from parse import df, Search_Filtr, Search, Result_generation

import telebot
from telebot import types


filter_class = 0


class Filter:
    data = 0
    key_words = 0

    def __init__(self):
        self.data = ['0', '0', '0', '0']
        self.key_words = []


bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def start(message) -> None:

    global filter_class
    filter_class = Filter()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Начать поиск')
    btn2 = types.KeyboardButton('Помощь')
    btn3 = types.KeyboardButton('FAQ')
    markup.add(btn3, btn2, btn1)

    for i_message in (greeting, user_manual, commands):
        bot.send_message(
            message.chat.id,
            text=i_message
        )

    bot.send_message(
         message.chat.id,
         text="Выберите интересующую вас функцию".format(message.from_user),
         reply_markup=markup
    )


@bot.message_handler(regexp=r'Начать поиск')
@bot.message_handler(regexp=r'Помощь')
@bot.message_handler(regexp=r'FAQ')
def first_step(message) -> None:
    flag = False

    match message.text:
        case 'Начать поиск':
            res = f'начат поиск'
            flag = True

        case 'Помощь':
            res = helper

        case 'FAQ':
            res = faq

    bot.reply_to(message, res)

    if flag:

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton('/filter')
        btn2 = types.KeyboardButton('/key_word')
        btn3 = types.KeyboardButton('Вывод результата')
        btn4 = types.KeyboardButton('Сброс фильтров')
        btn5 = types.KeyboardButton('Сброс ключевых слов')
        markup.add(btn1, btn2, btn4, btn5, btn3)

        bot.send_message(
            text='выберите режим поиска'.format(message.from_user),
            reply_markup=markup,
            chat_id=message.chat.id
        )


@bot.message_handler(regexp=r'Сброс фильтров')
@bot.message_handler(regexp=r'Сброс ключевых слов')
def delete(message) -> None:
    match message.text:
        case 'Сброс фильтров':
            filter_class.data = ['0', '0', '0', '0']
        case 'Сброс ключевых слов':
            filter_class.key_words = []


@bot.message_handler(regexp=r'Вывод результата')
def result(message) -> None:

    res = Result_generation(filter_class.data, filter_class.key_words)

    with open(res, 'rb') as res_file:
        bot.send_message(message.chat.id, text='Ваш результат:')
        bot.send_document(message.chat.id, res_file)


@bot.message_handler(commands=['manual'])
def manual(message) -> None:
    bot.reply_to(message, user_manual)


@bot.message_handler(commands=['commands'])
def available_commands(message) -> None:
    bot.reply_to(message, commands)


@bot.message_handler(commands=['filter', 'key_word'])
def second_step(message) -> None:

    flag = None

    match message.text:
        case '/filter':
            flag = True

            bot.send_message(
                text='Инструкция для поиска по фильтру из класса',
                chat_id=message.chat.id,
            )

        case '/key_word':
            flag = False

            bot.send_message(
                text='Инструкция для поиска по ключевому слову из класса',
                chat_id=message.chat.id,
            )

    if flag:

        btns = []
        markup = types.InlineKeyboardMarkup(row_width=1)

        btns.append(types.InlineKeyboardButton('Функциональная группа', callback_data='func'))
        btns.append(types.InlineKeyboardButton('Домен технологии', callback_data='domen technology'))



        if filter_class.data[1] != '0':
            btns.append(types.InlineKeyboardButton('Технология', callback_data='technology'))
            if filter_class.data[2] != '0':
                btns.append(types.InlineKeyboardButton('Метод использования', callback_data='method'))


        markup.add(*btns)


        bot.send_message(
            text=','.join(filter_class.data),
            chat_id=message.chat.id,
            reply_markup=markup
        )

    if not flag:

        bot.send_message(message.chat.id, text='Введите пожалуйста слово для поиска')



@bot.callback_query_handler(func=lambda callback: callback.data in ('func', 'domen technology', 'technology', 'method'))
def check_callback_data_2(callback) -> None:
     next_step = 0
     markup = types.InlineKeyboardMarkup(row_width=1)
     group = 'skip'


     match callback.data:
         case 'func':
             next_step = Search(filter_class.data, filter_class.key_words)['Функциональная группа'].unique()
                 #Search_Filtr(filter_class.data)['Функциональная группа'].unique()
             group = 0
         case 'domen technology':
             next_step = Search(filter_class.data, filter_class.key_words)['Домен'].unique()
                 #Search_Filtr(filter_class.data)['Домен'].unique()
                 # df['Домен'].unique()
             group = 1
         case 'technology':
             next_step = Search(filter_class.data, filter_class.key_words)['Технология'].unique()
                 #Search_Filtr(filter_class.data)['Технология'].unique()
                 # df['Технология'].unique()
             group = 2
         case 'method':
             next_step = Search(filter_class.data, filter_class.key_words)['Метод использования'].unique()
                 #Search_Filtr(filter_class.data)['Метод использования'].unique()
                 # df['Метод использования'].unique()
             group = 3


     if len(next_step) == 0:
        bot.send_message(chat_id=callback.message.chat.id, text='Ничего не найдено')

     else:

         for i_option in next_step:
            if len(i_option) > 33:
                i_option = i_option[:32]


            btn = types.InlineKeyboardButton(text=i_option, callback_data=str(group) + str(i_option))
            markup.add(btn)


         bot.send_message(chat_id=callback.message.chat.id, text='выберите опцию', reply_markup=markup)


@bot.callback_query_handler(lambda callback: int(callback.data[0]) in (0, 1, 2, 3))
def filter_log(callback) -> None:
    group, text = callback.data[0], callback.data[1:]
    filter_class.data[int(group)] = text
    res = filter_class.data[int(group)]
    df_filter = str(Search_Filtr(filter_class.data).shape[0])


    bot.send_message(callback.message.chat.id, text='Текущие фильтры: ' + ','.join(filter_class.data))
    bot.send_message(callback.message.chat.id, text='Строк:' + str(df_filter) +'\nДля перехода к следующему фильтру нажмите кнопку "фильтр"')


@bot.message_handler(content_types=['text'])
def log_keywords(message):
    filter_class.key_words.append(message.text)

    bot.send_message(message.chat.id, text= 'Список выбранных ключевых слов: ' + ','.join(filter_class.key_words))


if __name__ == '__main__':
    bot.infinity_polling()
