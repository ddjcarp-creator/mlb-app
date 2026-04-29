import streamlit as st
import datetime
import pandas as pd
import seaborn as sns
from pybaseball import statcast
from utils.mlb_api import get_probable_pitchers
from utils.statcast_utils import (
    get_statcast_hitter_table,
    get_statcast_pitcher_table,
    get_zone_map,
    get_rolling_xwoba
)

# ------------------------------
# Streamlit Configuration
# ------------------------------
st.set_page_config(
    page_title="MLB Statcast Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("⚾ MLB Statcast Dashboard")

# Date parameters
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

# Top tabs for navigation
tabs = st.tabs(["Matchups", "Hitters", "Pitchers", "Zones", "Rolling", "HR Analyzer"])

# ------------------------------
# MATCHUPS TAB
# ------------------------------
with tabs[0]:
    st.header("Matchups Dashboard")

    game_date = st.date_input("Game Date", yesterday)
    pitchers = get_probable_pitchers(game_date)
    st.subheader("📅 Probable Pitchers")
    st.dataframe(pitchers, use_container_width=True)

# ------------------------------
# HITTERS TAB
# ------------------------------
with tabs[1]:
    st.header("Recent Hitter Performance (30 Days)")
    df_hitters = get_statcast_hitter_table()

    hitter_search = st.text_input("Search hitter")
    if hitter_search:
        df_hitters = df_hitters[df_hitters["Hitter"].str.contains(hitter_search, case=False)]

    st.dataframe(df_hitters.style.background_gradient(cmap="RdYlGn_r", axis=None), use_container_width=True)

# ------------------------------
# PITCHERS TAB
# ------------------------------
with tabs[2]:
    st.header("Recent Pitcher Performance (30 Days)")
    df_pitchers = get_statcast_pitcher_table()

    pitcher_search = st.text_input("Search pitcher")
    if pitcher_search:
        df_pitchers = df_pitchers[df_pitchers["Pitcher"].str.contains(pitcher_search, case=False)]

    st.dataframe(df_pitchers.style.background_gradient(cmap="RdYlBu_r", axis=None), use_container_width=True)

# ------------------------------
# ZONES TAB
# ------------------------------
with tabs[3]:
    st.header("Pitch / Hitter Zone Heatmap")
    player = st.text_input("Enter player name")
    if player:
        fig = get_zone_map(player)
        st.pyplot(fig)

# ------------------------------
# ROLLING TAB
# ------------------------------
with tabs[4]:
    st.header("Rolling xwOBA Tracker")
    player = st.text_input("Enter hitter for rolling xwOBA")
    if player:
        data = get_rolling_xwoba(player)
        st.line_chart(data.set_index("game_date")["xwOBA"])

# ------------------------------
# HOME RUN ANALYZER TAB
# ------------------------------
with tabs[5]:
    st.header("Home Run Analyzer")

    start_date = st.date_input("Start Date", today - datetime.timedelta(days=7))
    end_date = st.date_input("End Date", today)

    if st.button("Load Home Run Data"):
        st.info("Fetching Statcast data... this may take a minute.")
        data = statcast(
            start_dt=start_date.strftime("%Y-%m-%d"),
            end_dt=end_date.strftime("%Y-%m-%d")
        )

        hr = data[data["events"] == "home_run"]

        if hr.empty:
            st.warning("No home runs found in that range.")
        else:
            st.success(f"{len(hr)} home runs found.")
            st.dataframe(
                hr[["batter_name", "pitcher_name", "launch_speed", "launch_angle", "events"]],
                use_container_width=True
            )

            st.subheader("Launch Angle vs Exit Velocity")
            st.scatter_chart(hr, x="launch_angle", y="launch_speed")
