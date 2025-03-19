import re, os ,tqdm
from urllib.parse import urljoin, unquote
from bs4 import BeautifulSoup
from curl_cffi import requests
import os
from flask import abort, url_for, render_template
import Anime, Episodes, Episode

def get_all_dubbedAnimes():
    with open("wcofunsites/dubbedAnimes.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    anime_list = soup.find_all('li', {'data-id': True})

    base_url = "https://www.wcopremium.tv"

    animes = []
    for anime in anime_list:
        anime_title = anime.find('a').text.strip()
        relative_link = anime.find('a')['href']
        complete_url =  relative_link
        animes.append({"title": anime_title, "url": complete_url})

    return animes

def get_all_subbedAnimes():
    with open("wcofunsites/subbedAnimes.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all <li> elements that contain <a> tags
    anime_list = soup.find_all('li')

    animes = []
    for anime in anime_list:
        anime_link = anime.find('a')
        if anime_link:
            anime_title = anime_link.text.strip()
            if(len(anime_title) == 1 and anime_title.isalpha()):
                continue
            relative_link = anime_link['href']
            complete_url = f"https://www.wcopremium.tv{relative_link}"
            animes.append({"title": anime_title, "url": complete_url})

    return animes


def get_all_cartoons():
    with open("wcofunsites/cartoons.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # Target the <ul> elements under the div with id="ddmcc_container"
    cartoon_lists = soup.select('#ddmcc_container ul')

    base_url = "https://www.wcopremium.tv"

    animes = []
    for ul in cartoon_lists:
        for li in ul.find_all('li'):
            link = li.find('a')
            if link:
                title = link.text.strip()
                relative_url = link['href']
                complete_url = f"{base_url}{relative_url}"
                animes.append({"title": title, "url": complete_url})

    return animes






































