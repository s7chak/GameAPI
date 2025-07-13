import json
import gameapi_config as config
import random
CACHE_FILE = config.country_metadata_file

def generate_country_quiz(mode: str = "mix", num_questions: int = 10) -> list:
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
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