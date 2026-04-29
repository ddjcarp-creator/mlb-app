import streamlit as st
from utils.statcast_utils import get_statcast_pitcher_table

st.title("Pitchers")

search = st.text_input("Search pitcher")

df = get_statcast_pitcher_table()

if search:
    df = df[df["Pitcher"].str.contains(search, case=False)]

st.dataframe(df, use_container_width=True)
