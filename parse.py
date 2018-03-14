#!/usr/bin/env python

from bs4 import BeautifulSoup
from req import get_html


html = get_html('https://yandex.ru/search/?text=python')

if html:
    bs = BeautifulSoup(html, 'html.parser')
    data = []

    for item in bs.find_all('li', class_='serp-item'):
        block_title = item.find('a', class_='organic__url')
        href = item.find_all('a', class_='path__item')[1]
        if not href.get('href').startswith('http://yabs.yandex.ru'):
            data.append({
                'title': block_title.text,
                'link': href.get('href'),
                })

    print(data)
else:
    print('Что-то пошло не так!')
