import json
import os

SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        default = {
            "sound": True,
            "difficulty": "normal",
            "car_color": "blue"
        }
        save_settings(default)
        return default
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

def load_scores():
    if not os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "w") as f:
            json.dump([], f)
    with open(LEADERBOARD_FILE, "r") as f:
        return json.load(f)

def save_score(name, score, distance):
    data = load_scores()

    data.append({
        "name": name,
        "score": score,
        "distance": distance
    })

    data = sorted(data, key=lambda x: x["score"], reverse=True)[:10]

    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(data, f, indent=4)