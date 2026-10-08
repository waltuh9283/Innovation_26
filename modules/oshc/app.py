import streamlit as st
import oshc

st.session_state.setdefault("page", "menu")

def go_to(page_name):
    st.session_state.page = page_name

def main():
    if st.session_state.page == "menu":
        st.title("Cybersecurity and OSHC Awareness")
        st.button("Medibank OSHC Basics", on_click=go_to, args=("oshc",))
        # add the phishing and vishing buttons here the same way
    elif st.session_state.page == "oshc":
        oshc.render()

main()