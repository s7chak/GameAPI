from flask import Flask, jsonify, request
from flask_cors import CORS
import gameutil as util
import json
import os

app = Flask(__name__)
CORS(app)

@app.route("/api/game_counter", methods=["POST"])
def game_meta_update():
    data = request.get_json()
    try:
        message = util.update_game_metadata(data)
        return jsonify({"message": message}), 200
    except Exception as e:
        return jsonify({"message": f"Error updating game metadata {str(data)}"}), 200

@app.route("/leaderboard/<game_id>")
def leaderboard(game_id):
    res = util.get_leaderboard(game_id)
    return res

@app.route("/api/game_metadata", methods=["GET"])
def game_metadata():
    try:
        result = util.fetch_game_metadata()
        return jsonify({"game_data": result}), 200
    except Exception as e:
        return jsonify({"message": f"Error updating game metadata {str(e)}"}), 500

@app.route("/api/capquiz", methods=["GET"])
def quiz():
    try:
        mode = request.args.get("mode", "mix").lower()
        num_questions = int(request.args.get("numQuestions", 10))
        questions = util.generate_country_quiz(mode, num_questions)
        print(f"Generated {len(questions)} questions in mode: {mode}")
        return jsonify({"questions": questions})
    except Exception as e:
        print(str(e))
        return jsonify({"message": str(e)})

@app.route("/")
def home_gameapi():
    return "GameAPI running for scaiverse: v2.1"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Default to 8080 if PORT is not set
    app.run(host="0.0.0.0", port=port)
