from flask import Flask, jsonify
import requests
import os
from dotenv import load_dotenv  # Add this

load_dotenv()

app = Flask(__name__)

# SerpAPI base URL and API key
SERP_API_URL = "https://serpapi.com/search.json"
SERP_API_KEY = os.getenv("SERP_API_KEY")

@app.route('/')
def hello():
    return "Welcome to the NFL Schedule API!"

@app.route('/sports', methods=['GET'])
def get_nfl_schedule():
    try:
        params = {
            "engine": "google",
            "q": "nfl schedule",
            "api_key": SERP_API_KEY
        }
        response = requests.get(SERP_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Debug: Print the entire SerpAPI response
        print("SerpAPI Response:", data)

        # Extract game spotlight
        game_spotlight = data.get("sports_results", {}).get("game_spotlight", {})

        if not game_spotlight:
            return jsonify({"message": "No NFL schedule available.", "games": []}), 200

        # Extract teams
        teams = game_spotlight.get("teams", [])
        if len(teams) == 2:
            away_team = teams[0].get("name", "Unknown")
            home_team = teams[1].get("name", "Unknown")
        else:
            away_team, home_team = "Unknown", "Unknown"

        # Prepare game info
        game_info = {
            "away_team": away_team,
            "home_team": home_team,
            "venue": game_spotlight.get("venue", "Unknown"),
            "date": game_spotlight.get("date", "Unknown"),
            "time": f"{game_spotlight.get('time', 'Unknown')} ET" if game_spotlight.get("time", "Unknown") != "Unknown" else "Unknown"
        }

        return jsonify({"message": "NFL schedule fetched successfully.", "games": [game_info]}), 200

    except Exception as e:
        return jsonify({"message": "An error occurred.", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
