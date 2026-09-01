import streamlit as st
from pages.dashboard_page import show_dashboard
from pages.project_page import show_projects
from pages.task_page import show_tasks
from services.api_client import login_user, register_user
from utils.session_utils import (
    is_logged_in,
    login,
    logout,
)

st.set_page_config(
    page_title="Project Management",
    layout="wide",
)


if not is_logged_in():
    st.title("Project Management System")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.subheader("Login")

        email = st.text_input(
            "Email",
            key="login_email",
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password",
        )

        if st.button(
            "Login",
            use_container_width=True,
        ):
            if not email or not password:
                st.warning("Please enter email and password.")

            else:
                response = login_user(
                    email,
                    password,
                )

                if response.status_code == 200:
                    data = response.json()

                    login(data["access_token"])

                    st.success("Login successful!")

                    st.rerun()

                else:
                    st.error(
                        response.json().get(
                            "detail",
                            "Invalid email or password",
                        )
                    )

    with tab2:
        st.subheader("Create Account")

        name = st.text_input("Name")

        email = st.text_input(
            "Email",
            key="register_email",
        )

        password = st.text_input(
            "Password",
            type="password",
            key="register_password",
        )

        if st.button(
            "Register",
            use_container_width=True,
        ):
            if not name or not email or not password:
                st.warning("Please fill all fields.")

            else:
                response = register_user(
                    name,
                    email,
                    password,
                )

                if response.status_code == 201:
                    st.success("Registration successful! " "You can now login.")

                else:
                    st.error(
                        response.json().get(
                            "detail",
                            "Registration failed",
                        )
                    )

    st.stop()


st.sidebar.title("Project Management")

st.sidebar.write("You are logged in.")

page = st.sidebar.radio(
    "Navigate",
    [
        "Dashboard",
        "Projects",
        "Tasks",
    ],
)

st.sidebar.divider()

if st.sidebar.button(
    "Logout",
    use_container_width=True,
):
    logout()

    st.rerun()


if page == "Dashboard":
    show_dashboard()
elif page == "Projects":
    show_projects()
elif page == "Tasks":
    show_tasks()
