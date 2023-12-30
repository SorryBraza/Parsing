import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
import json
import re
from tqdm import tqdm


def get_headers():
    return Headers(browser='chrome', os='win').generate()

def find_max_page(url, params):
    url_data = requests.get(url=url, params=params, headers=get_headers()).text
    soup = BeautifulSoup(url_data, 'lxml')
    pages = soup.find('div', class_='bloko-gap bloko-gap_top').find('div', \
                class_='pager').find_all('a', class_='bloko-button')
    return pages[-2].find('span').text

def parsed_hh(url, params, parsed_db):
    max_page = int(find_max_page(url, params))
    for _ in tqdm(range(max_page - 1), desc='Поиск ...'):
        response = requests.get(url=url, params=params, headers=get_headers())
        params['page'] += 1
        html_data = response.text
        hh_main = BeautifulSoup(html_data, 'lxml')
        company_tags = hh_main.find('div', id='a11y-main-content').find_all('div',\
                                                                class_='serp-item')

        for company in company_tags:
            link = company.find('a').get('href')
            data_company = requests.get(url=link, headers=get_headers()).text
            company_main = BeautifulSoup(data_company, 'lxml')
            description = company_main.find('div', class_='g-user-content')
            try:
                if re.search(r'\b(Django|Flask)\b', description.text) is None:
                    continue
                try:
                    salary = company.find('span', \
                            class_='bloko-header-section-2').text.replace('\u202f', '')
                except:
                    salary = 'Не указана'
            except:
                continue
            name = company.find('a', \
                class_='bloko-link bloko-link_kind-tertiary').text.replace('\xa0', '')
            city = company.find('div', \
                            class_='vacancy-serp-item__info').contents[1].contents[0]
            parsed_db.append(
                {
                    'link': link,
                    'salary': salary,
                    'name': name,
                    'city': city
                }
            )

def load_json(path, filename, parsed_db):
    with open(path+filename, 'w', encoding='utf-8') as file:
        json.dump(parsed_db, file, indent=4, ensure_ascii=False)