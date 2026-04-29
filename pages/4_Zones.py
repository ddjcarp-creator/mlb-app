import streamlit as st
from utils.statcast_utils import get_zone_map

st.title("Zone Heatmaps")

player = st.text_input("Enter hitter or pitcher name")

if player:
    fig = get_zone_map(player)
    st.pyplot(fig)
