import streamlit as st
from services.api_client import (
    get_project_summary,
    get_projects,
)


def show_dashboard():
    st.title("Project Dashboard")

    token = st.session_state["token"]

    response = get_projects(token)

    if response.status_code != 200:
        st.error("Unable to load projects.")

        return

    projects = response.json()

    if not projects:
        st.info("Create a project to see its dashboard.")

        return

    project_options = {project["name"]: project["id"] for project in projects}

    selected_project = st.selectbox(
        "Select Project",
        list(project_options.keys()),
    )

    project_id = project_options[selected_project]

    response = get_project_summary(
        token,
        project_id,
    )

    if response.status_code != 200:
        st.error(
            response.json().get(
                "detail",
                "Unable to load dashboard",
            )
        )

        return

    summary = response.json()

    total_tasks = summary.get(
        "total_tasks",
        0,
    )

    todo = summary.get(
        "todo",
        0,
    )

    in_progress = summary.get(
        "in_progress",
        0,
    )

    done = summary.get(
        "done",
        0,
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Tasks",
            total_tasks,
        )

    with col2:
        st.metric(
            "To Do",
            todo,
        )

    with col3:
        st.metric(
            "In Progress",
            in_progress,
        )

    with col4:
        st.metric(
            "Done",
            done,
        )

    st.divider()

    chart_data = {
        "To Do": todo,
        "In Progress": in_progress,
        "Done": done,
    }

    st.bar_chart(chart_data)
