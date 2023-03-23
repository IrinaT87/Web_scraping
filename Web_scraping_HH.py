import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
from pprint import pprint
import json

HOST='https://spb.hh.ru'
SEARCH=f'{HOST}/search/vacancy?text=python&area=1&area=2'

def get_headers():
    return Headers(browser='firefox',os='win').generate()

def get_text(url):
    return requests.get(url, headers=get_headers()).text


search_page=requests.get(SEARCH, headers=get_headers()).text
# pprint(search_page)
bs=BeautifulSoup(search_page,features='lxml')
vacancy_list=bs.find(attrs={'data-qa': 'vacancy-serp__results'}).find_all(class_="serp-item")
# pprint(vacancy_list)

vacancy_data=[]
for vacancy in vacancy_list:

    vacancy_name=vacancy.find('a',class_='serp-item__title')
    vacancy_link=vacancy_name['href']
    salary=vacancy.find('span',attrs={'data-qa': "vacancy-serp__vacancy-compensation"})
    salary = salary.text if salary else "Не указана"
    company_name=vacancy.find('a',attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
    city=vacancy.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text
    vacancy_data.append({
        "link": vacancy_link,
        "salary": salary,
        "company": company_name,
        "city": city,
    })
    
vacancy_list_ok=[]    
for vacancy in vacancy_data:
    tag = get_text(vacancy_link)
    if 'Django' in tag or 'Flask' in tag:
        vacancy_list_ok.append(vacancy)
    
pprint(vacancy_list_ok)
with open('vacancy.json', 'w', encoding='utf-8') as file:
        json.dump(vacancy_list_ok, file, ensure_ascii=False, indent=4)