import os
import requests
from flask import Flask, jsonify
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = Flask(__name__)

openai_api_key = os.getenv("OPENAI_API_KEY")
odds_api_key = os.getenv("ODDS_API_KEY")
client = OpenAI(api_key=openai_api_key)

@app.route("/get-nba-picks", methods=["GET"])
def get_game_totals():
    url = f"https://api.the-odds-api.com/v4/sports/basketball_nba/odds/?regions=us&markets=totals&oddsFormat=decimal&apiKey={odds_api_key}"

    try:
        res = requests.get(url)
        if res.status_code != 200:
            print("OddsAPI Error:", res.status_code, res.text)
            return jsonify({"error": "Failed to fetch totals"}), 500

        data = res.json()[:3]  # top 3 matchups for now
        prompt = f"""These are NBA game totals:\n{data}\n\nPick the best over/under totals and explain each with confidence %, emoji tags (🔒, 🟢, 🔴), and Nova-style notes."""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        reply = response.choices[0].message.content
        return jsonify({"nova_chart": reply})

    except Exception as e:
        print("Server Error:", str(e))
        return jsonify({"error": "Server failed"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)