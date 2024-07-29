import asyncio
import json
import os

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from dotenv import load_dotenv

load_dotenv()


BASE_URL = 'https://www.farpost.ru'
URL = 'https://www.farpost.ru/vladivostok/service/construction/guard/+/Системы+видеонаблюдения/'
WEBDRIVER_PATH = os.getenv('WEBDRIVER_PATH')


async def fetch(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            html_content = await response.text()
            return html_content
        else:
            return None


def solve_captcha_and_get_html(url):
    service = Service(WEBDRIVER_PATH)
    options = Options()
    options.headless = False
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    input("Пожалуйста, решите CAPTCHA и нажмите Enter...")
    html = driver.page_source
    driver.quit()
    return html


async def get_ad_links(url):
    html = solve_captcha_and_get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    views = soup.select('.views.nano-eye-text')
    links = [f"{BASE_URL}{a['href']}" for a in soup.find_all('a', class_='bulletinLink', href=True)]
    return links[:10], [view.text for view in views][:10]


async def get_titles(soup):
    title = soup.find(class_='inplace').text.strip()
    id = soup.find(class_='viewbull-bulletin-id__num').text.strip()[1:]
    autor = soup.find(class_='userNick').text.strip()
    print(title, id, autor)
    return title, id, autor


async def get_info(links, views):
    titles = []
    for index, (link, view) in enumerate(zip(links, views), start=1):
        html = solve_captcha_and_get_html(link)
        soup = BeautifulSoup(html, 'html.parser')
        title, id, autor = await get_titles(soup)
        titles.append({
            "title": title,
            "id": id,
            "author": autor,
            "view": view,
            "position": index
        })
    return titles


async def main(url):
    links, views = await get_ad_links(url)
    ad_info = await get_info(links, views)

    with open('ad_info.json', 'w', encoding='utf-8') as f:
        json.dump(ad_info, f, ensure_ascii=False, indent=4)

asyncio.run(main(URL))
