import streamlit as st
from utils.statcast_utils import get_rolling_xwoba

st.title("Rolling Performance")

player = st.text_input("Enter hitter name")

if player:
    df = get_rolling_xwoba(player)
    st.line_chart(df["xwOBA"])
