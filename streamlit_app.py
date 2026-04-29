import streamlit as st
import pandas as pd
import numpy as np
from pybaseball import statcast
import requests
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

def get_probable_pitchers(date_str):
    url = f"[statsapi.mlb.com](https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={date_str}&hydrate=probablePitcher)"
    data = requests.get(url).json()

    matchups = []
    for date in data.get("dates", []):
        for game in date.get("games", []):
            away = game["teams"]["away"]["team"]["name"]
            home = game["teams"]["home"]["team"]["name"]

            away_pitcher = game["teams"]["away"].get("probablePitcher", {}).get("fullName", "TBD")
            home_pitcher = game["teams"]["home"].get("probablePitcher", {}).get("fullName", "TBD")

            matchups.append({
                "matchup": f"{away} @ {home}",
                "away_pitcher": away_pitcher,
                "home_pitcher": home_pitcher
            })

    return pd.DataFrame(matchups)

def color_scale(val, min_val=None, max_val=None):
    if pd.isna(val):
        return ""
    pct = (val - min_val) / (max_val - min_val)
    pct = np.clip(pct, 0, 1)
    r = int(255 * (1 - pct))
    g = int(255 * pct)
    return f"background-color: rgb({r},{g},50); color: white;"

today = datetime.today().strftime("%Y-%m-%d")
st.sidebar.title("MLB Matchups")

date_pick = st.sidebar.date_input("Game Date", datetime.today())
date_str = date_pick.strftime("%Y-%m-%d")

matchups_df = get_probable_pitchers(date_str)

if matchups_df.empty:
    st.sidebar.error("No games for this date.")
else:
    games_list = list(matchups_df["matchup"])
    selected_games = st.sidebar.multiselect("Select Matchups", games_list, default=games_list[:3])

tabs = st.tabs(["Matchup", "Rolling", "Pitcher Zones", "Hitter Zones", "Export"])

with tabs[0]:
    st.subheader("Matchup Dashboard")

    start = (datetime.today() - timedelta(days=30)).strftime("%Y-%m-%d")
    end = datetime.today().strftime("%Y-%m-%d")

    try:
        stat_df = statcast(start_dt=start, end_dt=end)
    except Exception:
        st.error("Statcast error.")
        st.stop()

    grouped = stat_df.groupby("player_name").agg({
        "launch_speed": "mean",
        "launch_angle": "mean",
        "estimated_woba_using_speedangle": "mean",
        "events": "count"
    }).reset_index()

    grouped.columns = ["Hitter","EV","LA","xwOBA","BIP"]
    grouped["Test Score"] = np.random.uniform(20,80,len(grouped))
    grouped["Ceiling"] = np.random.uniform(0.02,0.15,len(grouped))
    grouped["HR Form"] = np.random.randint(20,80,len(grouped))
    grouped["ISO"] = grouped["EV"]/120

    order = ["Hitter","Test Score","Ceiling","HR Form","ISO","EV","LA","xwOBA","BIP"]
    df = grouped[order].head(20)

    numeric = df.select_dtypes(include=[np.number]).columns
    mins = df[numeric].min()
    maxs = df[numeric].max()

    styled = df.style.apply(
        lambda row: [
            color_scale(row[col], mins[col], maxs[col]) if col in numeric else ""
            for col in df.columns
        ],
        axis=1
    )

    st.dataframe(styled, use_container_width=True)

with tabs[1]:
    rolling = stat_df.groupby("game_date")["estimated_woba_using_speedangle"].mean()
    st.line_chart(rolling)

with tabs[2]:
    st.write("Pitcher Zones placeholder")

with tabs[3]:
    st.write("Hitter Zones placeholder")

with tabs[4]:
    st.download_button("Download CSV", df.to_csv(index=False), "matchup_export.csv")
