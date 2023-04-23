import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import aspose.words as aw


# Подсоединение к Google Таблицам
scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("gazpromnefte-b09221520021.json", scope)
client = gspread.authorize(credentials)
data = client.open("GazProm_data")
data_sheets = data.worksheets()

df = pd.DataFrame(data_sheets[0].get_all_records())
df['SEARCH'] = df['Наименование сценария'].astype(str) + ' ' + df['Описание'].astype(str) + ' ' +\
               df['Домен'].astype(str) + ' ' + df['Технология'].astype(str) + ' ' + \
               df['Метод использования'].astype(str) \
               + ' ' + df['Функциональная группа'].astype(str) + ' '\
               + df ['Наименование | Бенчмаркинг (внешний рынок)'].astype(str) + ' ' + \
               df ['Описание | Бенчмаркинг (внешний рынок)'].astype(str) + ' ' + df \
                   ['Описание проекта в ГПН | НИОКР'].astype(str) + \
               ' ' + df ['Название проекта | Проекты ЦТ'].astype(str)


# генерация итогового документа
def Result_generation(data_to_generate):
    document = data_to_generate
    return document


# поиск по фильтру
def Search_Filtr (filt):
    func_role = filt[0]
    domain = filt[1]
    tech = filt[2]
    meth = filt[3]
    filtred_data = df

    if func_role != "0":
        filtred_data = filtred_data.loc[(df['Функциональная группа'].astype(str).str.contains(func_role))]
    if meth != "0":
        filtred_data = filtred_data.loc[(df['Метод использования'].astype(str).str.contains(meth))]
    elif tech != "0":
        filtred_data = filtred_data.loc[(df['Технология'].astype(str).str.contains(tech))]
    elif domain !="0":
        filtred_data = filtred_data.loc[(df['Домен'].astype(str).str.contains(domain))]

    return filtred_data


# поиск по ключевым словам
def Search_Key_Words (key_words, filtred_data):
    if filtred_data.empty:
        filtred_data = df
    else:
        filtred_data_key = filtred_data
    for x in key_words:
        filtred_data_key = filtred_data_key.loc[(df['SEARCH'].astype(str).str.contains(x))]

    return filtred_data_key

# просто поиск
def Search(filt, key_words):
    return Search_Key_Words(key_words, Search_Filtr(filt))

df = Result_generation(df)


def Result_generation (filt, key_words):

    data_to_generate = Search (filt,key_words)
    doc = aw.Document()
    builder = aw.DocumentBuilder(doc)
    font = builder.font
    font.size = 14
    font.bold = False
    font.name = "Arial"
    numb = 0

    for i in data_to_generate['Наименование сценария']:
        numb+=1
        builder.writeln(str(numb)+") "+i)

    doc.save('result.doc')

    return ('result.doc')