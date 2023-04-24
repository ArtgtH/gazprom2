import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from pymystem3 import Mystem

# Подсоединение к Google Таблицам
def Google_Table ():
  scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]
  credentials = ServiceAccountCredentials.from_json_keyfile_name("gazpromnefte-b09221520021.json", scope)
  client = gspread.authorize(credentials)

  data = client.open("GazProm_data")
  data_sheets = data.worksheets()
  return data_sheets

df = pd.DataFrame(Google_Table()[0].get_all_records())
m = Mystem()

df['SEARCH'] = df['Наименование сценария'].astype(str) + ' ' + df['Описание'].astype(str) + ' ' +\
               df['Домен'].astype(str) + ' ' + df['Технология'].astype(str) + ' ' + \
               df['Метод использования'].astype(str) \
               + ' ' + df['Функциональная группа'].astype(str) + ' '\
               + df ['Наименование | Бенчмаркинг (внешний рынок)'].astype(str) + ' ' + \
               df ['Описание | Бенчмаркинг (внешний рынок)'].astype(str) + ' ' + df \
                   ['Описание проекта в ГПН | НИОКР'].astype(str) + \
               ' ' + df ['Название проекта | Проекты ЦТ'].astype(str)


# лемматизация текста для поиска
def lemmatize_sentence(text):
         
         lemmas = m.lemmatize(text)
         return "".join(lemmas).strip()

df['SEARCH'] = (df['SEARCH']).astype(str).apply(lemmatize_sentence)


# генерация итоговых сообщений
def Result_generation (filt, key_words):
  data_to_generate = Search (filt,key_words)
  res = list(('Наименование сценария:  ' + data_to_generate['Наименование сценария'].astype(str) + '\n\n'
   'Описание:  ' + data_to_generate['Описание'].astype(str) + '\n'
  + '\n >КЛАССИФИКАЦИЯ \n'
  + 'Функциональная группа:  ' + data_to_generate['Функциональная группа'].astype(str) + '\n'
  + 'Домен:  ' + data_to_generate['Домен'].astype(str) + '\n' 
  + 'Технология:  ' + data_to_generate['Технология'].astype(str) + '\n' 
  + 'Метод использования:  ' + data_to_generate['Метод использования'].astype(str) + '\n' + '\n'
  + ' >ОСНОВНЫЕ МЕТРИКИ \n'
  + 'Потенциал решения:  ' + data_to_generate['Потенциал решения'].astype(str) + '\n'
  + 'Рыночная зрелость:  ' + data_to_generate['Рыночная зрелость'].astype(str) + '\n'
  + 'Организационная готовность:  ' + data_to_generate['Организационная готовность'].astype(str) + '\n'
  + '\n'
  + 'Реализуется в Газпром нефти?    ' + data_to_generate['Реализуется в Газпром нефти?'].astype(str)).astype(str).values)
  
  return res
         
         
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


def Search_Key_Words (key_words, filtred_data):
  key_words_lem = []
  for word in key_words:
    key_words_lem.extend(m.lemmatize(word))
  
  if filtred_data.empty:
    filtred_data = df

  filtred_data_key = filtred_data

  for x in key_words_lem:
      
      filtred_data_key = filtred_data_key.loc[((df['SEARCH'].astype(str).str.contains(x)))]
  
  return filtred_data_key

# просто поиск
def Search(filt, key_words):
    return Search_Key_Words(key_words, Search_Filtr(filt))
