import streamlit as st

st.set_page_config(
    page_title="MLB Statcast Dashboard",
    layout="wide",
)

st.title("MLB Statcast Dashboard")

st.write("""
Welcome to your fully Statcast-powered MLB dashboard.

Use the navigation menu on the left to view:
- Matchups  
- Hitter analytics  
- Pitcher analytics  
- Zone heatmaps  
- Rolling performance  
""")
