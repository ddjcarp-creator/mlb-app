import streamlit as st
import pandas as pd
import datetime
from pybaseball import statcast

st.title("Home Run and Statcast Analyzer")

# --- Date range selection ---
start = st.date_input("Start date", datetime.date(2024, 4, 1))
end = st.date_input("End date", datetime.date.today())

if st.button("Load Statcast Data"):
    st.info("Loading data from MLB Statcast... This may take up to a minute.")
    data = statcast(start_dt=start, end_dt=end)
    st.success(f"Loaded {len(data)} rows of Statcast data.")

    # --- Filter only batted balls ---
    data = data[data["events"].notna()]

    # --- Home runs only ---
    hr = data[data["events"] == "home_run"]

    # --- Basic hitter stats ---
    hitter_stats = (
        data.groupby("batter_name")[["launch_speed", "launch_angle", "estimated_woba_using_speedangle"]]
        .mean()
        .round(2)
        .rename(columns={
            "launch_speed": "Avg EV",
            "launch_angle": "Avg LA",
            "estimated_woba_using_speedangle": "xwOBA"
        })
    )

    # --- Pitcher stats for HRs ---
    pitcher_stats = (
        hr.groupby("pitcher_name")[["release_speed", "zone", "p_throws"]]
        .agg({"release_speed": "mean", "zone": "count", "p_throws": "first"})
        .rename(columns={"release_speed": "Avg Velo", "zone": "HR Allowed"})
        .sort_values("HR Allowed", ascending=False)
    )

    st.subheader("Hitter Summary (All Batted Balls)")
    st.dataframe(hitter_stats)

    st.subheader("Pitchers Allowing the Most HRs")
    st.dataframe(pitcher_stats.head(20))

    st.subheader("Home Run Launch Data")
    st.dataframe(hr[["batter_name", "pitcher_name", "launch_speed", "launch_angle", "bb_type", "stand", "p_throws", "description"]])

    # Optional chart
    st.subheader("Launch Angle vs Exit Velocity (All Home Runs)")
    st.scatter_chart(hr, x="launch_angle", y="launch_speed")
