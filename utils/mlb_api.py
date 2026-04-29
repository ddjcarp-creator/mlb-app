import requests
import pandas as pd

def get_probable_pitchers(date):
    date_str = date.strftime("%Y-%m-%d")
    url = f"[statsapi.mlb.com](https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={date_str}&hydrate=probablePitcher)"
    data = requests.get(url).json()

    matchups = []

    for day in data.get("dates", []):
        for game in day.get("games", []):
            away = game["teams"]["away"]["team"]["name"]
            home = game["teams"]["home"]["team"]["name"]

            away_p = game["teams"]["away"].get("probablePitcher", {}).get("fullName", "TBD")
            home_p = game["teams"]["home"].get("probablePitcher", {}).get("fullName", "TBD")

            matchups.append({
                "Matchup": f"{away} @ {home}",
                "Away Pitcher": away_p,
                "Home Pitcher": home_p
            })

    return pd.DataFrame(matchups)
