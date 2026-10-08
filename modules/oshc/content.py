# Content loader for json files in OSHC module.

import json, os
import streamlit as st

#CAN CHANGE DIRECTORY PATH LATERIF REQUIRED
#CONTENT_DIR = os.path.join(os.path.dirname(__file__), "content")

@st.cache_data
def load_oshc():
    with open("oshc.json", encoding="utf-8") as f:
        return json.load(f)