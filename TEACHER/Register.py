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
    cur = db.db.cursor()
    # list tables and pick candidates
    cur.execute("SHOW TABLES")
    tables = [r[0].lower() for r in cur.fetchall()]
    students_table = next((t for t in tables if t.startswith("student")), None)
    trip_table = next((t for t in tables if t == "trip" or t.startswith("trip")), None)
    trip_students_table = next((t for t in tables if "trip" in t and "student" in t), None)

    if not students_table or not trip_table or not trip_students_table:
        st.error("Required tables missing. Available tables: " + ", ".join(tables))
    else:
        cur.execute(
            f"SELECT tripID, destination, date, returnDate, status FROM {trip_table} WHERE leaderID = %s",
            (leaderID,),
        )
        trips = cur.fetchall()
        if not trips:
            st.info("You have no assigned trips.")
        else:
            for trip in trips:
                tripID, destination, date, returnDate, status = trip
                st.subheader(f"Trip {tripID}: {destination}")
                cur.execute(
                    f"""
                    SELECT s.studentID, s.fName, s.lName
                    FROM {students_table} s
                    JOIN {trip_students_table} ts ON s.studentID = ts.studentID
                    WHERE ts.tripID = %s
                    """,
                    (tripID,),
                )
                students = cur.fetchall()
                if not students:
                    st.write("No students assigned to this trip.")
                else:
                    for sid, fname, lname in students:
                        st.write(f"{fname} {lname}")
db.close()