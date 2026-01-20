import streamlit as st
import databasetest as dbt

st.header("Register")
st.write(f"You are logged in as {st.session_state.get('role')}")
st.write(f"Logged in as {st.session_state.get('username')} with userID {st.session_state.get('userID')}")
db = dbt.dataBase()

leaderID = st.session_state.get("userID") or st.session_state.get("userid")
if not leaderID:
    st.error("No leaderID in session. Please log in.")
else:
    trips = db.read_trips_by_leader(leaderID)
    if not trips:
        st.info("You have no assigned trips.")
    else:
        for trip in trips:
            tripID, destination, date, returnDate, status, leader = trip
            with st.expander(f"Trip {tripID}: {destination}"):
                st.write(f"Date: {date}")
                st.write(f"Return Date: {returnDate}")
                st.write(f"Status: {status}")
                st.write(f"Leader ID: {leader}")
                st.subheader("Registered Students:")
                students = db.read_students_for_trip(tripID)
                if not students:
                    st.write("No students assigned to this trip.")
                else:
                    for sid, fname, lname in students:
                        st.write(f"{fname} {lname}")
db.close()
