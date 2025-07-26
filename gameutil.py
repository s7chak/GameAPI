import os
import json
import gameapi_config as config
import random
from flask import jsonify
CAPQUIZ_CACHE_FILE = config.country_metadata_file
METADATA_FILE = config.games_metadata_file

def get_leaderboard(game_id):
    with open(METADATA_FILE) as f:
        data = json.load(f)
    res = jsonify(data.get(game_id, {}))
    return res

def fetch_game_metadata():
    meta = {}
    with open(METADATA_FILE, "r") as f:
        meta = json.load(f)
    return meta

def update_game_metadata(data):
    game_id = data.get("game_id")
    result = data.get("result")  # 'won', 'lost', 'abandoned'
    duration_seconds = data.get("duration_seconds")
    started_at = data.get("started_at")
    ended_at = data.get("ended_at")
    username = data.get("username")  # optional
    score = data.get("score")        # optional
    if not all([game_id, result, duration_seconds is not None]):
        return "Invalid payload"
    if os.path.exists(METADATA_FILE):
        # Load file
        with open(METADATA_FILE, "r") as f:
            meta = json.load(f)
    else:
        os.makedirs(os.path.dirname(METADATA_FILE), exist_ok=True)
        with open(METADATA_FILE, "w") as f:
            json.dump({}, f)
    if game_id not in meta:
        meta[game_id] = {
            "played": 0,
            "won": 0,
            "lost": 0,
            "abandoned": 0,
            "max_score": config.max_scores[game_id.lower()],
            "minutes": [],
            "seconds": [],
            "scorers": []
        }
    game = meta[game_id]
    game["played"] += 1
    if result in ["won", "lost", "abandoned"]:
        game[result] += 1

    game["minutes"].append(int(duration_seconds // 60))
    game["seconds"].append(int(duration_seconds))
    if score is not None:
        if score > game.get("max_score", 0):
            game["max_score"] = score

    if username and score is not None:
        game["scorers"].append({
            "user": username,
            "score": score
        })
    with open(METADATA_FILE, "w") as f:
        json.dump(meta, f, indent=2)

    return f"Game metadata updated successfully: {str(meta[game_id])}"


def generate_country_quiz(mode: str = "mix", num_questions: int = 10) -> list:
    with open(CAPQUIZ_CACHE_FILE, "r", encoding="utf-8") as f:
        all_countries = json.load(f)

    modes = ["country", "capital", "flag"]
    if mode not in modes and mode != "mix":
        mode = "mix"

    questions = []
    for _ in range(num_questions):
        q_mode = random.choice(modes) if mode == "mix" else mode
        country = random.choice(all_countries)

        if q_mode == "country":
            correct = country["capital"][0]
            wrong = random.sample(
                [c["capital"][0] for c in all_countries if c != country and c["capital"]],
                3
            )
            options = wrong + [correct]
            random.shuffle(options)
            questions.append({
                "question": f"What is the capital of {country['name']}?",
                "answer": correct,
                "options": options,
                "mode": "country"
            })

        elif q_mode == "capital":
            correct = country["name"]
            wrong = random.sample(
                [c["name"] for c in all_countries if c != country],
                3
            )
            options = wrong + [correct]
            random.shuffle(options)
            questions.append({
                "question": f"{country['capital'][0]} is the capital of which country?",
                "answer": correct,
                "options": options,
                "mode": "capital"
            })

        elif q_mode == "flag":
            correct = country["name"]
            wrong = random.sample(
                [c["name"] for c in all_countries if c != country],
                3
            )
            options = wrong + [correct]
            random.shuffle(options)
            questions.append({
                "question": "Which country's flag is shown?",
                "flag": country["flag"],
                "answer": correct,
                "options": options,
                "mode": "flag"
            })

    return questions