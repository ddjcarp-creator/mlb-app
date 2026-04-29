import streamlit as st
import pandas as pd
from utils.statcast_utils import get_statcast_hitter_table
from utils.mlb_api import get_probable_pitchers
from datetime import datetime

st.title("Matchups")

date = st.date_input("Game Date", datetime.today())

matchups = get_probable_pitchers(date)
st.subheader("Today's Matchups")
st.dataframe(matchups, use_container_width=True)

st.subheader("Recent Hitter Performance (Last 30 Days)")
df = get_statcast_hitter_table()
st.dataframe(df, use_container_width=True)
