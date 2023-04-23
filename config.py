API_TOKEN = '6277920991:AAGS0U71SqLc-KvFFosNMwmxzAUWBmUEGpA'
table_url = 'https://docs.google.com/spreadsheets/d/1lAR44nxkqTPxxcGkM97tPWBPADLI-Xyr/edit#gid=2074020589'

class Filter:

    def __init__(self):
        self.data = ['0', '0', '0', '0']
        self.key_words = []

greeting = f'Привет, меня зовут GazpromNefteBot\nЯ создан, чтобы находить информацию в гугл-таблице'


user_manual = f'Я могу делать это и то'


commands = f'Список доступных команд:\n'\
           f'Приветствие - /start\n' \
           f'Инструкция - /manual\n' \
           f'Команды - /commands\n'

faq = f'тут будет раздел FAQ'



helper = f'Открываем открытую линию с поддержкой'



bd = {

}


def search_by_key(key):
    res = Filter()
    try:
        res = bd[key]
    except KeyError as er:
        print(er)

    return res

