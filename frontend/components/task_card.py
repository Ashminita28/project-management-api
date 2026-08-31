import streamlit as st


def display_task_card(task):
    st.write(f"### {task['title']}")
    if task.get("description"):
        st.write(task["description"])
    st.write(f"**Status:** {task['status']}")
    st.caption(f"Task ID: {task['id']}")
    st.divider()
