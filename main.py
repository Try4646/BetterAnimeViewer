import os, time, random
from audioop import reverse
from shutil import ExecError
from types import NoneType
from flask import Flask, render_template, request, send_from_directory, url_for, abort, make_response, redirect
import threading
#shit
import Episode, Episodes, Anime, Populate, Profile
from datetime import datetime

app = Flask(__name__)


app.secret_key = 'niggersinParis69420'

@app.template_filter('datetimeformat')
def datetimeformat(value):
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value).strftime('%Y-%m-%d %H:%M')
    return value


@app.route('/')
def home():
    username = request.cookies.get('username')
    user_profile = Profile.get_user_profile(username) if username else None
    return render_template("home.html", user=user_profile)

@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')


@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')

    if not username or len(username) < 3:
        return render_template('register.html', error="Username must be at least 3 characters")

    if Profile.get_user_profile(username):
        return render_template('register.html', error="Username already exists")

    Profile.save_user_profile(username, {'watched': [], 'favorites': []})

    response = make_response(redirect(url_for('home')))
    response.set_cookie('username', username, max_age=60 * 60 * 24 * 30)
    return response


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')

    if not username:
        return render_template('login.html', error="Please enter a username")

    user_profile = Profile.get_user_profile(username)

    if not user_profile:
        return render_template('login.html', error="Username not found")

    response = make_response(redirect(url_for('home')))
    response.set_cookie('username', username, max_age=60 * 60 * 24 * 30)
    return response


@app.route('/profile')
def profile():
    username = request.cookies.get('username')
    if not username:
        return redirect(url_for('home'))

    user_profile = Profile.get_user_profile(username)
    return render_template("profile.html", user=user_profile)

@app.route('/dubbed-anime-list')
def dubbedanimelist():
    film = Populate.get_all_dubbedAnimes()
    return render_template("index.html", animes=film, title1="Dubbed Anime List")
@app.route('/subbed-anime-list')
def subbedanimelist():
    film = Populate.get_all_subbedAnimes()
    return render_template("index.html", animes=film, title1="Subbed Anime List")
@app.route('/movie-list')
def movielist():
    film = Populate.get_all_subbedAnimes()
    return render_template("index.html", animes=film, title1="Movie List")
@app.route('/cartoon-list')
def cartoonlist():
    film = Populate.get_all_cartoons()
    return render_template("index.html", animes=film, title1="Cartoon List")
@app.route('/ova-list')
def ovalist():
    film = Populate.get_all_subbedAnimes()
    return render_template("index.html", animes=film, title1="OVA Series List")


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').lower()
    animes = []
    dubanimes = Populate.get_all_dubbedAnimes()
    subanimes = Populate.get_all_subbedAnimes()
    cartoons = Populate.get_all_cartoons()
    animes.extend(dubanimes + subanimes + cartoons)
    filtered_animes = [anime for anime in animes if query in anime["title"].lower()]
    return render_template("home.html", animes=filtered_animes, query=query)



@app.route('/anime/<path:anime_url>')
def anime_episodes(anime_url):
    episodes = Episodes.get_episodes_for_anime(anime_url)
    return render_template("episodes.html", episodes=episodes)


@app.route('/downloadall/<path:anime_url>')
def downloadallEpisodes(anime_url):
    return Anime.downloadAllEpisodes(anime_url)


@app.route('/episode/<path:episode_url>')
def watch_episode(episode_url):
    htmlvar,video_url,anime,season,episode,prev_url,next_url =  Episode.watch_episode(episode_url)
    return render_template(htmlvar,
                           video_url=video_url,
                           anime_title=anime,
                           season=season,
                           episode=episode,
                           next_url="http://192.168.178.28:4428/episode/" + prev_url,
                           prev_url="http://192.168.178.28:4428/episode/" + next_url)


@app.route('/animes/<anime_dir>/<filename>')
def serve_anime(anime_dir, filename):
    return send_from_directory(os.path.join('Animes', anime_dir), filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4428, debug=True)
