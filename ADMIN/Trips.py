import streamlit as st
import databasetest as dbt
db = dbt.dataBase()
st.header("Trips")
st.write(f"You are logged in as {st.session_state.role}")

trips = db.read_all_trips()
if not trips:
    st.info("No trips found.")
else:
    for trip in trips:
        tripID = trip[0]
        destination = trip[1]
        date = trip[2]
        returnDate = trip[3]
        status = trip[4]
        leaderID = trip[5]
        leader = db.read_username_from_userID(leaderID)


        with st.expander(f"Trip {tripID}: {destination}"):
            st.write(f"Date: {date}")
            st.write(f"Return Date: {returnDate}")
            st.write(f"Status: {status}")
            st.write(f"Leader: {leader} (ID: {leaderID})")
            with st.expander("View Students"):
                students = db.read_students_for_trip(tripID)
                if not students:
                    st.info("No students assigned to this trip.")
                else:
                    for student in students:
                        studentID = student[0]
                        fName = student[1]
                        lName = student[2]
                        st.write(f"{fName} {lName} (ID: {studentID})")