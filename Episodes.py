import re, os ,tqdm
from urllib.parse import urljoin, unquote
from bs4 import BeautifulSoup
from curl_cffi import requests

def get_episodes_for_anime(anime_url):
    # Configure headers
    print("->getepisodesfornanime")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": anime_url,
        "Connection": "keep-alive",
    }

    # Set cookies (update cf_clearance if needed)
    cookies = {
        "wordpress_test_cookie": "WP%20Cookie%20check;",
        "wordpress_logged_in_52ae307e0b9e736a7dbf74030de2e01a": "airstrike5040%40gmail.com%7C1743112208%7CDdu33PG0wAXDy4zxEwCZOhLrcQSiiaCOoJLkdkL45j5%7Cfaff545bffa0d56cf612d36b75ab2aad0d166f82a28eab02461990222195092f",
        "wordpress_sec_52ae307e0b9e736a7dbf74030de2e01a": "airstrike5040%40gmail.com%7C1743112208%7CDdu33PG0wAXDy4zxEwCZOhLrcQSiiaCOoJLkdkL45j5%7Cec2e25fd67993cf49b2cb6ea07a1e5bf2a48ebb410c490aa4b471fbe86a78289",
        "kndctr_8AD56F28618A50850A495FB6_AdobeOrg_identity": "CiYxMDA2NzIzNjQ5MzUzMDk2MTcxMjE4NDM0OTgzMTkyMDU3MDU5NFIRCPO--9mzMhgBKgRJUkwxMAPwAfO--9mzMg=="
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
    # Parse with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find episode links
    episode_links = soup.select('div#sidebar_right3 a')
    # print(response.text)
    episodes = []
    for link in episode_links:
        episodes.append({
            "title": link.text.strip(),
            "url": link.get('href', '')
        })

    return episodes
