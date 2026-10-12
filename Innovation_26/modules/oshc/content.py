# Content loader for json files in OSHC module.

import json, os
import streamlit as st

# Look for oshc.json next to this file, so it loads no matter which
# folder `streamlit run` is started from (root app.py or this folder).
CONTENT_DIR = os.path.dirname(os.path.abspath(__file__))


@st.cache_data
def load_oshc():
    with open(os.path.join(CONTENT_DIR, "oshc.json"), encoding="utf-8") as f:
        return json.load(f)
