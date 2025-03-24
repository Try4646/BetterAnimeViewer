import re, os ,tqdm
from urllib.parse import urljoin, unquote
from bs4 import BeautifulSoup
from curl_cffi import requests

def get_episodes_for_anime(anime_url):
    print("->getepisodesfornanime")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": anime_url,
        "Connection": "keep-alive",
    }

    cookies = { #Cookies Here i just leaked mine but idfc go to wcopremium log in and get cookies this is illegal i think idfk
        }

    try:
        response = requests.get(
            anime_url,
            headers=headers,
            cookies=cookies,
            impersonate="chrome"
        )
    except Exception as e:
        print(f"Request failed: {str(e)}")
        return []

    if response.status_code == 403:
        print("Blocked by AnitBotProtection. reresh ur cookies goodboy")

        return []
    elif response.status_code != 200:
        print(f"Error {response.status_code}")
        return []
    elif response.status_code == 200:
        print("did that shit?")
    soup = BeautifulSoup(response.text, 'html.parser')

    episode_links = soup.select('div#sidebar_right3 a')
    # print(response.text)
    episodes = []
    for link in episode_links:
        episodes.append({
            "title": link.text.strip(),
            "url": link.get('href', '')
        })

    return episodes
