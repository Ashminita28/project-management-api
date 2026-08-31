import streamlit as st
from services.api_client import (
    create_task,
    delete_task,
    get_project_tasks,
    get_projects,
    update_task,
)

TASK_STATUSES = [
    "To Do",
    "In Progress",
    "In Review",
    "Done",
]


def show_tasks():
    st.title(" Tasks")

    token = st.session_state["token"]

    response = get_projects(token)

    if response.status_code != 200:
        st.error("Unable to load projects.")

        return

    projects = response.json()

    if not projects:
        st.info("Create a project first.")

        return

    project_options = {project["name"]: project["id"] for project in projects}

    selected_project = st.selectbox(
        "Select Project",
        list(project_options.keys()),
    )

    project_id = project_options[selected_project]

    status_filter = st.selectbox(
        "Filter by Status",
        ["All"] + TASK_STATUSES,
    )

    status_value = None if status_filter == "All" else status_filter

    response = get_project_tasks(
        token,
        project_id,
        status_filter=status_value,
    )

    if response.status_code != 200:
        st.error(
            response.json().get(
                "detail",
                "Unable to load tasks",
            )
        )

        return

    tasks = response.json()

    with st.expander("Add Task"), st.form("create_task_form"):
        title = st.text_input("Task Title")

        description = st.text_area("Description")

        status = st.selectbox(
            "Status",
            TASK_STATUSES,
        )

        submitted = st.form_submit_button("Create Task")

        if submitted:
            if not title:
                st.warning("Task title is required.")

            else:
                response = create_task(
                    token,
                    project_id,
                    title,
                    description,
                    status,
                )

                if response.status_code == 201:
                    st.success("Task created successfully!")

                    st.rerun()

                else:
                    st.error(
                        response.json().get(
                            "detail",
                            "Failed to create task",
                        )
                    )

    if not tasks:
        st.info("No tasks found for this project.")

        return

    for task in tasks:
        st.markdown(f"### {task['title']}")

        st.write(task.get("description", ""))

        st.write(f"**Status:** {task['status']}")

        with st.expander(f"Edit Task: {task['title']}"):
            new_title = st.text_input(
                "Title",
                value=task["title"],
                key=f"title_{task['id']}",
            )

            new_description = st.text_area(
                "Description",
                value=task.get(
                    "description",
                    "",
                ),
                key=f"task_desc_{task['id']}",
            )

            current_status = task["status"]

            if current_status not in TASK_STATUSES:
                current_status = "To Do"

            new_status = st.selectbox(
                "Status",
                TASK_STATUSES,
                index=TASK_STATUSES.index(current_status),
                key=f"status_{task['id']}",
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button(
                    "Update Task",
                    key=f"update_task_{task['id']}",
                ):
                    response = update_task(
                        token,
                        task["id"],
                        new_title,
                        new_description,
                        new_status,
                    )

                    if response.status_code == 200:
                        st.success("Task updated!")

                        st.rerun()

                    else:
                        st.error(
                            response.json().get(
                                "detail",
                                "Failed to update task",
                            )
                        )

            with col2:
                if st.button(
                    "Delete Task",
                    key=f"delete_task_{task['id']}",
                ):
                    response = delete_task(
                        token,
                        task["id"],
                    )

                    if response.status_code in [200, 204]:
                        st.success("Task deleted!")

                        st.rerun()

                    else:
                        st.error(
                            response.json().get(
                                "detail",
                                "Failed to delete task",
                            )
                        )

        st.divider()
