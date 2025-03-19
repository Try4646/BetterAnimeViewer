import json
import os

PROFILES_DIR = 'user_profiles'


def get_user_profile(username):
    path = os.path.join(PROFILES_DIR, f"{username}.json")
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return None


def save_user_profile(username, data):
    if not os.path.exists(PROFILES_DIR):
        os.makedirs(PROFILES_DIR)

    path = os.path.join(PROFILES_DIR, f"{username}.json")
    with open(path, 'w') as f:
        json.dump(data, f)