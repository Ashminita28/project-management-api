import streamlit as st
from components.project_card import display_project_card
from services.api_client import (
    create_project,
    delete_project,
    get_projects,
    update_project,
)


def show_projects():
    st.title("MY PROJECTS")
    token = st.session_state["token"]
    search = st.text_input("Search projects", placeholder="Enter project name...")
    response = get_projects(token=token, search=search)
    if response.status_code != 200:
        st.error(response.json().get("detail", "Failed to load projects"))
        return
    projects = response.json()
    with st.expander("Create New Project"), st.form("create_project_form"):
        name = st.text_input("Project Name")
        description = st.text_area("Description")
        submitted = st.form_submit_button("Create Project")
        if submitted:
            if not name:
                st.warning("Project name is required.")
            else:
                response = create_project(token, name, description)
                if response.status_code == 201:
                    st.success("Project created successfully!")
                    st.rerun()
                else:
                    st.error(response.json().get("detail", "Failed to create project"))

    if not projects:
        st.info("No projects found.")
        return
    for project in projects:
        display_project_card(project)

        with st.expander(f"Edit: {project['name']}"):
            new_name = st.text_input(
                "Project Name",
                value=project["name"],
                key=f"name_{project['id']}",
            )

            new_description = st.text_area(
                "Description",
                value=project.get(
                    "description",
                    "",
                ),
                key=f"description_{project['id']}",
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button(
                    "Update",
                    key=f"update_{project['id']}",
                ):
                    response = update_project(
                        token,
                        project["id"],
                        new_name,
                        new_description,
                    )

                    if response.status_code == 200:
                        st.success("Project updated!")

                        st.rerun()

                    else:
                        st.error(
                            response.json().get(
                                "detail",
                                "Update failed",
                            )
                        )

            with col2:
                if st.button(
                    "Delete",
                    key=f"delete_{project['id']}",
                ):
                    response = delete_project(
                        token,
                        project["id"],
                    )

                    if response.status_code in [200, 204]:
                        st.success("Project deleted!")

                        st.rerun()

                    else:
                        st.error(
                            response.json().get(
                                "detail",
                                "Delete failed",
                            )
                        )
