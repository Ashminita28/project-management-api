import streamlit as st


def display_project_card(project):
    st.subheader(project["name"])
    if project.get("description"):
        st.write(project["description"])
    st.caption(f"Project ID: {project['id']}")
    st.divider()
