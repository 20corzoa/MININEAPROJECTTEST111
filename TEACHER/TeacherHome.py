import streamlit as st
st.header("Teacher Home")
st.write(f"You are logged in as {st.session_state.role}")
st.write(f"Your user ID is {st.session_state.userID}")
st.write(f"Your username is {st.session_state.username}")
st.write("Welcome to the Teacher Home Page!")
st.write("From here, you can navigate to other sections using the sidebar.")
st.write("Please select an option from the sidebar to get started.")
st.write("If you need assistance, please contact the administrator.")
st.write("Thank you for using the Judd Trips Management System!")
st.write("Have a great day!")

if st.button("Documents", use_container_width=True):
    st.switch_page(st.Page("TEACHER/Documents.py", title="Documents"))


if st.button("Emergency Info", use_container_width=True):
    st.switch_page(st.Page("TEACHER/EmergencyInfo.py", title="Emergency Info"))


if st.button("Travel Plan", use_container_width=True):
    st.switch_page(st.Page("TEACHER/TravelPlan.py", title="Travel Plan"))


if st.button("Register", use_container_width=True):
    st.switch_page(st.Page("TEACHER/Register.py", title="Register"))