import streamlit as st
st.header("Admin Home")
st.write(f"You are logged in as {st.session_state.role}")
st.write(f"UserID: {st.session_state.userID}")
st.write(f"Username: {st.session_state.username}")
st.write("Welcome to the Admin Home Page!")
st.write("From here, you can navigate to other sections using the sidebar.")
st.write("Please select an option from the sidebar to get started.")
st.write("If you need assistance, please contact the system administrator.")
st.write("Thank you for using the Judd Trips Management System!")
st.write("Have a great day!")

if st.button("Manage Users", use_container_width=True):
    st.switch_page(st.Page("ADMIN/Users.py", title="Manage Users")) 
if st.button("Manage Trips", use_container_width=True):
    st.switch_page(st.Page("ADMIN/Trips.py", title="Manage Trips"))
if st.button("Manage Students", use_container_width=True):
    st.switch_page(st.Page("ADMIN/Students.py", title="Manage Students"))
if st.button("Trip Students", use_container_width=True):
    st.switch_page(st.Page("ADMIN/TripStudents.py", title="Trip Students"))