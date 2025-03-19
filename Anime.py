import re, os ,tqdm
from time import sleep
from urllib.parse import urljoin, unquote
from bs4 import BeautifulSoup
from curl_cffi import requests
from flask import abort
import Episode, Episodes







def downloadAllEpisodes(anime_url):
    episodes = Episodes.get_episodes_for_anime(anime_url)
    episodes = sorted(episodes, key=lambda x: x.get('episode_number', 0), reverse=True)
    for episode in episodes:
        if episode.get('title') == '':
            continue
        if episode.get('url') == '':
            continue
        try:
            anime, season, episoden = Episode.parse_anime_link(episode.get('url'))
        except ValueError:
            abort(404)

        safe_anime = "".join([c if c.isalnum() else "-" for c in anime]).strip("-")
        filename = f"{safe_anime}-{season}-{episoden}.mp4"
        file_path = os.path.join('Animes', safe_anime, filename)
        print(episode)
        try:
            downloadURL = Episode.fetch_episode_download_link(episode.get('url'))
        except AttributeError:
            continue

        if not downloadURL:
            print('Do something here to show user failed to download?')

        if not os.path.exists(file_path):
            if not Episode.download_episode(downloadURL, safe_anime, filename):
                print("error")  # show here that this download failed and continue to the next one
        sleep(0.1)
    return 'Downloaded Everything owo u can now watch anime without waiting so fucking long owowoowowowoowowow'