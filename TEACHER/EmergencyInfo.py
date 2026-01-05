import streamlit as st
import databasetest as dbt

st.header("Emergency Information")
st.write(f"You are logged in as {st.session_state.get('role')}")

db = dbt.dataBase()
studentList = db.read_all_student()
if studentList:
    for student in studentList:
        studentID = int(student[0])        
        st.subheader(f"{student[1]} {student[2]}")
        #st.write(f"Student ID: {studentID}")

        medical = db.read_medical_info_by_id(studentID)
        #st.write(db.read_all_medical_info())
        if medical:
            st.write(f"Dietary needs: {medical[1]}")
            st.write(f"Medical: {medical[2]}")
            st.write(f"Notes: {medical[3]}")
            st.write(f"Doctors: {medical[4]}")
        else:
            st.write("No medical information available.")

        emergency = db.read_emergency_info_by_id(studentID)
        if emergency:
            st.write(f"Phone: {emergency[1]}")
            st.write(f"Email: {emergency[2]}")
        else:
            st.write("No emergency contact information available.")
else:
    st.warning("No students found in the database.")