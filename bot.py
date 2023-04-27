from config import API_TOKEN, greeting, faq, helper, user_manual, bd, search_by_key, Filter, filter_manual, key_manual
from parse import df, Search_Filtr, Search, Result_generation

import telebot
from telebot import types

solution = 0

filter_class = 0

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def start(message) -> None:

    global filter_class
    filter_class = Filter()

    bd[message.chat.id] = filter_class

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Начать поиск')
    btn2 = types.KeyboardButton('Помощь')
    btn3 = types.KeyboardButton('FAQ')
    markup.add(btn3, btn2, btn1)

    for i_message in (greeting, user_manual):
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
@bot.message_handler(regexp=r'Вызов менеджера')
def first_step(message) -> None:
    flag = False

    match message.text:
        case 'Начать поиск':
            res = f'начат поиск'
            flag = True

        case 'Помощь' | 'Вызов менеджера':
            res = helper

        case 'FAQ':
            res = faq

    bot.reply_to(message, res)

    if flag:

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton('Фильтр')
        btn2 = types.KeyboardButton('Ключевое слово')
        btn3 = types.KeyboardButton('Вывод результата')
        btn4 = types.KeyboardButton('Сброс фильтров')
        btn5 = types.KeyboardButton('Сброс ключевых слов')
        btn6 = types.KeyboardButton('Вызов менеджера')
        markup.add(btn1, btn2, btn4, btn5, btn3, btn6)

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
            search_by_key(message.chat.id).data = ['0', '0', '0', '0']
        case 'Сброс ключевых слов':
            search_by_key(message.chat.id).key_words = []


@bot.message_handler(regexp=r'Вывод результата')
def result(message) -> None:

    markup = types.InlineKeyboardMarkup()
    global solution 
    solution = Result_generation(filt=search_by_key(message.chat.id).data,
                            key_words=search_by_key(message.chat.id).key_words)

    for num, i_message in enumerate(solution[:40]):
        markup.add(types.InlineKeyboardButton(text='Хотите получить больше информации?', callback_data=f'Yes{num}'))

        bot.send_message(message.chat.id, text=i_message, reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: callback.data.startswith('Yes'))
def gpt_search(callback):
    question_part_1 = 'Создай описание того, как технологическое решение с описанием ниже используется в деятельности реальных компаний: '
    index = int(callback.data[-1])
    question_part_2 = solution[index]
    question_final = question_part_1 + question_part_2

    answer = copilot.get_answer(question_final)

    bot.send_message(callback.message.chat.id, text=answer)



@bot.message_handler(commands=['manual'])
def manual(message) -> None:
    bot.reply_to(message, user_manual)


@bot.message_handler(regexp=r'Фильтр')
@bot.message_handler(regexp=r'Ключевое слово')
def second_step(message) -> None:

    flag = None

    match message.text:
        case 'Фильтр':
            flag = True

            bot.send_message(
                text=filter_manual,
                chat_id=message.chat.id,
            )

        case 'Ключевое слово':
            flag = False

            bot.send_message(
                text=key_manual,
                chat_id=message.chat.id,
            )

    if flag:

        btns = []
        markup = types.InlineKeyboardMarkup(row_width=1)

        btns.append(types.InlineKeyboardButton('Функциональная группа', callback_data='func'))
        btns.append(types.InlineKeyboardButton('Домен технологии', callback_data='domen technology'))

        try:
            if search_by_key(message.chat.id).data[1] != '0':
                btns.append(types.InlineKeyboardButton('Технология', callback_data='technology'))
                if search_by_key(message.chat.id).data[2] != '0':
                    btns.append(types.InlineKeyboardButton('Метод использования', callback_data='method'))
        except KeyError:
            pass


        markup.add(*btns)
        cur_filter = []



        for i_filter in search_by_key(message.chat.id).data:
            if i_filter != '0':
                cur_filter.append(i_filter)



        if len(cur_filter) == 0:
            res = 'Фильтры отсутствуют'
        else:
            res = 'Текущие фильтры: ' + ', '.join(cur_filter)


        bot.send_message(
            text=res,
            chat_id=message.chat.id,
            reply_markup=markup
        )

    if not flag:

        bot.send_message(message.chat.id, text='Введите пожалуйста слово для поиска с восклицательного знака')


@bot.callback_query_handler(func=lambda callback: callback.data in ('func', 'domen technology', 'technology', 'method'))
def check_callback_data_2(callback) -> None:
     next_step = 0
     markup = types.InlineKeyboardMarkup(row_width=1)
     group = 'skip'


     match callback.data:
         case 'func':
             next_step = Search(bd[callback.message.chat.id].data, bd[callback.message.chat.id].key_words)['Функциональная группа'].unique()
             group = 0

         case 'domen technology':
             next_step = Search(bd[callback.message.chat.id].data, bd[callback.message.chat.id].key_words)['Домен'].unique()
             group = 1

         case 'technology':
             next_step = Search(bd[callback.message.chat.id].data, bd[callback.message.chat.id].key_words)['Технология'].unique()
             group = 2

         case 'method':
             next_step = Search(bd[callback.message.chat.id].data, bd[callback.message.chat.id].key_words)['Метод использования'].unique()
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
    search_by_key(callback.message.chat.id).data[int(group)] = text
    df_filter = str(Search(filt=search_by_key(callback.message.chat.id).data, key_words=search_by_key(callback.message.chat.id).key_words).shape[0])


    cur_filter = []

    for i_filter in bd[callback.message.chat.id].data:
        if i_filter != '0':
            cur_filter.append(i_filter)

    if len(cur_filter) == 0:
        res = 'Фильтры отсутствуют'
    else:
        res = 'Текущие фильтры: ' + ', '.join(cur_filter)

    bot.send_message(callback.message.chat.id, text=res + \
                                                    '\nСписок выбранных ключевых слов: ' + \
                                           ', '.join(search_by_key(callback.message.chat.id).key_words) + \
                                           '\nНайдено решений: ' + str(df_filter) + \
                                            '\nДля перехода к следующему фильтру нажмите кнопку "фильтр"' + \
                                            '\nДля вывода результатов нажмите кнопку "вывод результатов"')


@bot.message_handler(regexp=r'\!')
def log_keywords(message):
    word = message.text[1:]
    search_by_key(message.chat.id).key_words.append(word)


    search_res = str(Search(filt=search_by_key(message.chat.id).data, key_words=search_by_key(message.chat.id).key_words).shape[0])

    cur_filter = []

    for i_filter in bd[message.chat.id].data:
        if i_filter != '0':
            cur_filter.append(i_filter)

    if len(cur_filter) == 0:
        res = 'Фильтры отсутствуют'
    else:
        res = 'Текущие фильтры: ' + ', '.join(cur_filter)

    bot.send_message(message.chat.id, text='Список выбранных ключевых слов: ' + \
                                           ', '.join(search_by_key(message.chat.id).key_words) + \
                                           '\n' + res + '\nНайдено решений: ' + str(search_res)+ \
                                            '\nДля вывода результатов нажмите кнопку "вывод результатов"')


if __name__ == '__main__':
    bot.infinity_polling()
