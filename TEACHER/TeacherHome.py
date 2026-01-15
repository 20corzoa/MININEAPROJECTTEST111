import streamlit as st

st.header("Teacher Home")
st.write(f"Logged in as {st.session_state.username} with role {st.session_state.role}")


if st.button("Documents", use_container_width=True):
    st.switch_page(st.Page("TEACHER/Documents.py", title="Documents"))


if st.button("Emergency Info", use_container_width=True):
    st.switch_page(st.Page("TEACHER/EmergencyInfo.py", title="Emergency Info"))


if st.button("Travel Plan", use_container_width=True):
    st.switch_page(st.Page("TEACHER/TravelPlan.py", title="Travel Plan"))


if st.button("Register", use_container_width=True):
    st.switch_page(st.Page("TEACHER/Register.py", title="Register"))