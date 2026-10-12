import streamlit as st

st.set_page_config(
    page_title="Vishing Awareness Game",
    page_icon="📞"
)

home = st.Page(
    "home.py",
    title="Main Menu",
    icon="🏠",
    default=True
)

beginner = st.Page(
    "beginner/beginner.py",
    title="Beginner Level",
    icon="🟢"
)

pg = st.navigation(
    [home, beginner],
    position="hidden"
)

pg.run()