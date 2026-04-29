import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pybaseball import statcast
import seaborn as sns
import matplotlib.pyplot as plt

def get_statcast_hitter_table():
    end = datetime.today().date()
    start = end - timedelta(days=30)
    df = statcast(start_dt=str(start), end_dt=str(end))

    g = df.groupby("player_name").agg({
        "launch_speed": "mean",
        "launch_angle": "mean",
        "estimated_woba_using_speedangle": "mean",
        "events": "count"
    }).reset_index()

    g.columns = ["Hitter", "EV", "LA", "xwOBA", "BIP"]

    g["HH%"] = (df.groupby("player_name")["launch_speed"]
                .apply(lambda x: (x >= 95).mean())
                .tolist())

    return g.sort_values("xwOBA", ascending=False)

def get_statcast_pitcher_table():
    end = datetime.today().date()
    start = end - timedelta(days=30)
    df = statcast(start_dt=str(start), end_dt=str(end))

    p = df.groupby("pitcher").agg({
        "release_speed": "mean",
        "effective_speed": "mean",
        "pfx_x": "mean",
        "pfx_z": "mean"
    }).reset_index()

    p.columns = ["Pitcher", "Velo", "EffVelo", "HorizBreak", "VertBreak"]
    return p.sort_values("Velo", ascending=False)

def get_zone_map(player):
    end = datetime.today().date()
    start = end - timedelta(days=60)
    df = statcast(start_dt=str(start), end_dt=str(end))
    df = df[df["player_name"] == player]

    fig, ax = plt.subplots(figsize=(6,6))
    sns.kdeplot(
        x=df["plate_x"],
        y=df["plate_z"],
        fill=True,
        cmap="coolwarm",
        ax=ax
    )
    ax.set_title(f"Zone Map: {player}")
    return fig

def get_rolling_xwoba(player):
    end = datetime.today().date()
    start = end - timedelta(days=90)
    df = statcast(start_dt=str(start), end_dt=str(end))
    df = df[df["player_name"] == player]

    df["xwOBA"] = df["estimated_woba_using_speedangle"].rolling(20).mean()
    return df[["game_date", "xwOBA"]]
