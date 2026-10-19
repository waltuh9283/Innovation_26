import streamlit as st

st.set_page_config(
    page_title="Vishing Awareness Game",
    page_icon="📞"
)

# Main Menu
home = st.Page(
    "home.py",
    title="Main Menu",
    icon="🏠",
    default=True
)

# Beginner Level
beginner = st.Page(
    "beginner/beginner.py",
    title="Beginner Level",
    icon="🟢"
)

# Intermediate Level
intermediate = st.Page(
    "intermediate/intermediate.py",
    title="Intermediate Level",
    icon="🟡"
)

# Advanced Level
advanced = st.Page(
    "Advanced/advanced.py",
    title="Advanced Level",
    icon="🔴"
)

# Register all pages
pg = st.navigation(
    [home, beginner, intermediate,advanced],
    position="hidden"
)

pg.run()