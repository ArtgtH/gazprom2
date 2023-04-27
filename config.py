API_TOKEN = '6277920991:AAGS0U71SqLc-KvFFosNMwmxzAUWBmUEGpA'
table_url = 'https://docs.google.com/spreadsheets/d/1lAR44nxkqTPxxcGkM97tPWBPADLI-Xyr/edit#gid=2074020589'

class Filter:

    def __init__(self):
        self.data = ['0', '0', '0', '0']
        self.key_words = []

greeting = f'Привет, меня зовут Цифровой Навигатор\nЯ создан, чтобы находить информацию о различных решениях, которые реализуются в рамках компании ГазпромНефть Цифровые Решения'


commands = ''



user_manual = f'Пользовательский мануал\n\n' \
'Цифровой Навигатор - автоматизированная программа, с помощью которой  вы можете сортировать данные по технологическим решениям компании «Газпромнефть Цифровые решения» с помощью заданных фильтров и ключевых слов и быстро получать необходимую информацию в виде текстового сообщения.\n\n' \
'>В ходе сортировки вы можете фильтровать 4 основных столбца: «Функциональная группа»; «Домен технологии»; «Технология», «Метод использования».\n' \
'Обратите внимание, что «домен технологии», «технология» и «метод использования» связаны иерархически. Соответственно, чтобы выбрать фильтрацию по методу использования, вам необходимо заполнить фильтры по домену технологии и технологии.\n\n' \
'>В ходе сортировки вы можете применять поиск по ключевым словам. Обратите внимание на корректность слова и его наличие в БД.\n\n' \
'>В процессе сортировки вы можете перезаписывать фильтры (нажмите кнопку «Фильтр» и выберите другой фильтр), сбрасывать фильтры (кнопка «Сброс фильтров») и сбрасывать ключевые слова (кнопка «Сброс ключевых слов»).\n\n' \
'>Для вывода результатов поиска нажмите на кнопку «Вывод результата».\n\n' \
'>После вывода результатов вы можете получить дополнительную информацию от Chat-GPT.\n\n' \
'>Некоторые функции, например, кнопки «Помощь» и «Вызов менеджера» получат функционал в следующих версиях бота.\n\n' \
'Цифровой Навигатор осуществляет поиск по следующей гугл-таблице: https://docs.google.com/spreadsheets/d/1CKPbkFdj395mRdDQE-1mOIFYKM2icZ6f'



faq = f'FAQ\n\n' \
'Что делает кнопка «Помощь»?\n' \
'— Кнопка «Помощь» открывает прямую линию с технической поддержкой.\n\n' \
'Что делает кнопка «Вызов менеджера»?\n' \
'— Кнопка «Вызов менеджера» открывает прямую линию с отделом по работе с клиентами.\n\n' \
'Как мне использовать фильтр?\n' \
'— Чтобы использовать фильтр:\n' \
'1. Нажмите на кнопку «Фильтр», расположенную на клавиатуре.\n' \
'2. Выберите необходимые фильтры.\n' \
'3. Если необходимо, дополнительно воспользуйтесь функцией поиска по ключевым словам.\n' \
'4. Нажмите на кнопку «Вывод результата».\n\n' \
'Как мне использовать поиск по ключевым словам?\n' \
'— Чтобы использовать поиск по ключевым словам:\n' \
'1. Нажмите на кнопку «Ключевое слово», расположенную на клавиатуре.\n' \
'2. Введите все ключевые слова через текстовое поле ввода (Используйте восклицательный знак перед словом. Пример: !VR).\n' \
'3. Если необходимо, дополнительно воспользуйтесь функцией фильтрации.\n' \
'4. Нажмите на кнопку «Вывод результата».\n\n' \
'Что делают кнопки «Сброс фильтров» и «Сброс ключевых слов»?\n' \
'— Эти кнопки ПОЛНОСТЬЮ удаляют все ранее внесенные фильтры и ключевые слова соответственно.\n\n' \
'Я дважды выбрал один фильтр, что будет?\n'\
'— Фильтр будет заново перезаписан.\n\n' \
'Когда я могу вывести результат?\n' \
'— Вы можете вывести результат в любой момент работы бота. Максимальный размер вывода ограничен 50 решениями.\n\n' \
'Как вывести стартовую панель?\n' \
'— Очистите историю сообщений с ботом (в окне удаления истории сообщений выберите опцию «Также удалить для …») или отправьте боту команду /start через текстовое поле ввода.\n\n'



helper = f'Открываем открытую линию с поддержкой'


filter_manual = f'Вы можете выбрать всего 4 фильтра: \n\n — функциональная группа – независимый\n\n — ' \
                f'домен технологии – независимый\n\n — технология – зависит от домена технологии ' \
                f'(сначала выбирается домен технологии)\n\n — метод использования – зависит от ' \
                f'технологии (сначала выбирается технология)\n\nСброс фильтров полностью обнулит выбранные фильтры'

key_manual = f'Для ввода ключевого слова воспользуйтесь текстовым вводом\n\n' \
             f'После вам снова нужно будет открыть клавиатуру с кнопками\n\n' \
             f'Количество ключевых слов неограниченно'


bd = {

}


solutions = {

}



def search_by_key(key):
    res = Filter()
    try:
        res = bd[key]
    except KeyError as er:
        print(er)

    return bd[key]



