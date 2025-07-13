from flask import Flask, jsonify, request
from flask_cors import CORS
import gameutil as util

app = Flask(__name__)
CORS(app)

@app.route("/api/quiz", methods=["GET"])
def quiz():
    try:
        mode = request.args.get("mode", "mix").lower()
        num_questions = int(request.args.get("num_questions", 10))
        questions = util.generate_country_quiz(mode, num_questions)
        print(f"Generated {len(questions)} questions in mode: {mode}")
        return jsonify({"questions": questions})
    except Exception as e:
        print(str(e))
        return jsonify({"message": str(e)})




@app.route("/")
def home_gameapi():
    return "GameAPI running for scaiverse: v1.0"

if __name__ == "__main__":
    app.run(port=8091, debug=True)
