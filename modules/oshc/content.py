# Content loader for json files in the OSHC module.
import json
import os
import streamlit as st

# Resolve the path from this file, so it works no matter which folder
# streamlit is launched from (module on its own, or via the hub's app.py).
CONTENT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "oshc.json")


@st.cache_data
def load_oshc():
    with open(CONTENT_PATH, encoding="utf-8") as f:
        return json.load(f)