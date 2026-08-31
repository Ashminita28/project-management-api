import streamlit as st


def is_logged_in() -> bool:
    return "token" in st.session_state


def get_token():
    return st.session_state.get("token")


def login(token: str):
    st.session_state["token"] = token


def logout():
    st.session_state.clear()
