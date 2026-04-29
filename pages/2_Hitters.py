import streamlit as st
from utils.statcast_utils import get_statcast_hitter_table
st.title("Hitters")
search = st.text_input("Search hitter")
df = get_statcast_hitter_table()
if search:
    df = df[df["Hitter"].str.contains(search, case=False)]
st.dataframe(df, use_container_width=True)
