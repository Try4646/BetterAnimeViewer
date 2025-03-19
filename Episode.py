import re, os ,tqdm
import time
from urllib.parse import urljoin, unquote
from bs4 import BeautifulSoup
from curl_cffi import requests
import os
from flask import abort, url_for, render_template, request
import Anime, Episodes, Profile

def parse_anime_link(link):
    pattern = r"https://www\.wcopremium\.tv/(?P<anime>[a-zA-Z0-9-]+?)(?:-season-(?P<season>\d+))?(?:-episode-|-ep)(?P<episode>\d+).*"
    match = re.match(pattern, link, re.IGNORECASE)

    if not match:
        raise ValueError("Invalid link format")

    anime = match.group("anime").replace("-", " ").strip()
    season = match.group("season") or "1"
    episode = match.group("episode").zfill(2)

    # Clean up anime name with numbers
    anime = re.sub(r'(\d+)([a-zA-Z])', r'\1 \2', anime)
    anime = re.sub(r'([a-zA-Z])(\d+)', r'\1 \2', anime)

    return anime, season, episode



def watch_episode(episode_url):
    try:
        anime, season, episode = parse_anime_link(episode_url)
    except ValueError:
        abort(404)

    downloadurl = fetch_episode_download_link(episode_url)
    if not downloadurl:
        return 'Download URL not found'

    anime_url = "https://www.wcopremium.tv/anime/" + anime.replace(" ", "-")
    safe_anime = "".join([c if c.isalnum() else "-" for c in anime]).strip("-")
    filename = f"{safe_anime}-{season}-{episode}.mp4"
    file_path = os.path.join('Animes', safe_anime, filename)
    anime_dir = os.path.join('Animes', safe_anime)

    if not os.path.exists(file_path):
        if not download_episode(downloadurl, safe_anime, filename):
            return "Download failed"

    episodes = Episodes.get_episodes_for_anime(anime_url)

    valid_episodes = []
    for episode_data in episodes:
        if episode_data.get('title') == '' or episode_data.get('url') == '':
            continue
        try:
            anime1, season1, episoden1 = parse_anime_link(episode_data['url'])
        except ValueError:
            abort(404)
        valid_episodes.append(episode_data)

    current_index = None
    for idx, episode_data in enumerate(valid_episodes):
        if episode_data['url'] == episode_url:
            current_index = idx
            break

    if current_index is None:
        abort(404)

    previous_url = valid_episodes[current_index - 1]['url'] if current_index > 0 else None
    next_url = valid_episodes[current_index + 1]['url'] if current_index < len(valid_episodes) - 1 else None

    if not os.path.exists(anime_dir):
        abort(404)



    video_url = url_for('serve_anime',
                        anime_dir=safe_anime,
                        filename=filename)

    if previous_url is None:
        previous_url = episode_url

    if next_url is None:
        next_url = episode_url
    args = []
    args.append("episode.html")
    args.append(video_url)
    args.append(anime)
    args.append(season)
    args.append(episode)
    args.append(previous_url)
    args.append(next_url)

    username = request.cookies.get('username')
    if username:
        try:
            user_profile = Profile.get_user_profile(username)

            episode_id = f"{anime}-{season}-{episode}"

            watched_entry = {
                'anime': anime,
                'season': season,
                'episode': episode,
                'episode_url': episode_url,
                'timestamp': time.time()
            }

            # Check if already exists in watched list
            existing = next((item for item in user_profile['watched']
                             if item['episode_url'] == episode_url), None)

            if not existing:
                user_profile['watched'].append(watched_entry)
                Profile.save_user_profile(username, user_profile)

        except Exception as e:
            print(f"Error updating watched status: {str(e)}")
    else:
        print("User not logged in - watched status not saved")
    return args



def download_episode(download_url, Anime = "Misc",filename = "RENAMETHIS.mp4"):
    #check if alr there before downloading cause might be slow i like Highschool dxd and romance animes Owo~~
    print("->download_episode")
    file_path = os.path.join('Animes', Anime, filename)
    if os.path.exists(file_path):
        return True

    #rewqest hihi >-<
    chunk_size = 256
    r = requests.get(
        download_url,
        stream=True
    )
    if r.status_code == 403:
        print("Blocked by AnitBotProtection. reresh ur cookies goodboy")

        return False
    elif r.status_code != 200:
        print(f"Error {r.status_code}")
        return False
    os.makedirs('Animes/' + Anime, exist_ok=True)
    with open('Animes/'+Anime+"/"+filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=chunk_size):
            f.write(chunk)
    return True



def fetch_episode_download_link(episode_url):
    print("->fetchepisoddownloadlink")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": episode_url,
        "Connection": "keep-alive",
    }

    cookies = {
        "wordpress_test_cookie": "WP%20Cookie%20check;",
        "wordpress_logged_in_52ae307e0b9e736a7dbf74030de2e01a": "airstrike5040%40gmail.com%7C1743112208%7CDdu33PG0wAXDy4zxEwCZOhLrcQSiiaCOoJLkdkL45j5%7Cfaff545bffa0d56cf612d36b75ab2aad0d166f82a28eab02461990222195092f",
        "wordpress_sec_52ae307e0b9e736a7dbf74030de2e01a": "airstrike5040%40gmail.com%7C1743112208%7CDdu33PG0wAXDy4zxEwCZOhLrcQSiiaCOoJLkdkL45j5%7Cec2e25fd67993cf49b2cb6ea07a1e5bf2a48ebb410c490aa4b471fbe86a78289",
        "kndctr_8AD56F28618A50850A495FB6_AdobeOrg_identity": "CiYxMDA2NzIzNjQ5MzUzMDk2MTcxMjE4NDM0OTgzMTkyMDU3MDU5NFIRCPO--9mzMhgBKgRJUkwxMAPwAfO--9mzMg=="
        }

    try:
        response = requests.get(
            episode_url,
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

    soup = BeautifulSoup(response.text, 'html.parser')

    # downloadlinkdefault = soup.select('div#free-jwplayer')

    iframe = soup.select_one('div#free-jwplayer iframe')
    if not iframe:
        print("No video iframe found")
        return None

    iframe_src = iframe.get('src')
    if not iframe_src:
        print("No iframe src found")
        return None

    base_url = "https://www.wcopremium.tv"
    full_iframe_url = urljoin(base_url, iframe_src)
    #print(full_iframe_url)
    #return full_iframe_url

    try:
        lresponse = requests.get(
            episode_url,
            headers=headers,
            cookies=cookies,
            impersonate="chrome"
        )
    except Exception as e:
        print(f"Request failed: {str(e)}")
        return
    if lresponse.status_code == 403:
        print("Blocked by AnitBotProtection. reresh ur cookies goodboy")

        return []
    elif lresponse.status_code != 200:
        print(f"Error {lresponse.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    script_tag = soup.find('script', text=re.compile(r'jwplayer\("myJwVideo"\)\.setup'))
    if not script_tag:
        print("no jwplayer script found")
        return None

    script_text = script_tag.string
    playlist_match = re.search(r'playlist:\s*(\[.*?\])', script_text, re.DOTALL)
    if not playlist_match:
        print("no playlist found in script")
        return None

    playlist_str = playlist_match.group(1)
    try:
        hd_url_match = re.search(r'file:\s*"([^"]+)"\s*,\s*type:\s*"video/mp4"\s*,\s*label:\s*"HD"', playlist_str)
        any_file_match = re.search(r'file:\s*"([^"]+)"\s*,\s*type:\s*"video/[^"]+"', playlist_str)

        if hd_url_match:
            hd_url= hd_url_match.group(1)

        elif any_file_match:
            hd_url = any_file_match.group(1)

        return hd_url

    except Exception as e:
        print(f"Failed to parse playlist: {str(e)}")
        return None

    #print(realurl)
    #return realurl

