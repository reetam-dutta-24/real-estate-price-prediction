import os
import streamlit as st

def get_backend_url():
    try:
        return st.secrets["BACKEND_URL"]
    except (KeyError, FileNotFoundError):
        return os.environ.get("BACKEND_URL", "http://127.0.0.1:8000")

BACKEND_URL = get_backend_url()