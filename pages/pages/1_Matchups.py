import streamlit as st
import pandas as pd
import numpy as np
from utils.statcast_utils import get_statcast_hitter_table
from utils.mlb_api import get_probable_pitchers

st.title("Matchup Dashboard")

date = st.date_input("Game Date")

# Probable pitchers from MLB API
matchups = get_probable_pitchers(date)
st.subheader("Today's Matchups")
st.dataframe(matchups, use_container_width=True)

# Statcast hitter performance
st.subheader("Hitter Performance (Last 30 Days)")
df = get_statcast_hitter_table()
st.dataframe(df, use_container_width=True)
