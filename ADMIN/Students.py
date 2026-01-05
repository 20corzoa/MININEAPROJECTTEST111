import streamlit as st
import pandas as pd
import App


st.header("Students Management")

# Load students from database
dbStudentsList = App.myDatabase.read_all_students() 

dbStudentsDict = dict()
for row in dbStudentsList:
    dbStudentsDict[row[2]] = row
print("DB Students Dict:" , dbStudentsDict.items())
st.session_state.StudentsList=dbStudentsDict 
# Display current students
dfList = pd.DataFrame(
    [(key, value[1]) for key, value in st.session_state.StudentsList.items()],
    columns=['Student', 'Role']
)
_ = dfList  # suppress implicit display
st.data_editor(dfList, disabled=True)

# Create a copy of studentlist to form a dropdownlist and add the new student option 
studentSelectionDropDown = dict()
for key in st.session_state.StudentsList.copy():
    studentSelectionDropDown[key] = "STUDENT ID:" + str(st.session_state.StudentsList[key][0])
studentSelectionDropDown["Add New Student"] = "N/A"


dfDropDown = pd.DataFrame([(key, value) for key, value in studentSelectionDropDown.items()],
    columns=['Student','StudentId'])



# Select student from dropdown
studentSelection = st.selectbox("Select Student", options=dfDropDown['Student'],format_func=lambda x: f"{x} ({studentSelectionDropDown[x]})")

# new student ? 
is_new_student = studentSelection == "Add New Student"
# get data 
student_data = None if is_new_student else st.session_state.StudentsList[studentSelection]


#create form with student details
with st.form("studentForm"):
    st.subheader("Student Details")


    newStudentID = st.text_input("StudentID", value="--" if is_new_student else student_data[0], disabled = True) 
    newUsername = st.text_input("Username", value="" if is_new_student else student_data[2])
    newRole = st.selectbox("Role", options=["Admin", "Teacher"], index=0 if is_new_student else ["Admin", "Teacher", "Student"].index(student_data[1]))
    newPassword = st.text_input("Password", type="password", value="" if is_new_student else student_data[3])
    newfName = st.text_input("First Name",value="" if is_new_student else student_data[4])
    newlName = st.text_input("Last Name",value="" if is_new_student else student_data[5])
    newEmail = st.text_input("Email",value="" if is_new_student else student_data[6])
    newPhone = st.text_input("Phone Number",value="" if is_new_student else student_data[7])

    buttonName = "Create" if is_new_student else "Submit Changes"
    submitted = st.form_submit_button(buttonName)
    deleted_button = False  
    if not is_new_student:
        deleted_button = True
        deleted = st.form_submit_button("Delete")   
        
  
    if deleted_button:
        if deleted:
            # Delete student
            st.session_state.StudentsList.pop(studentSelection)
            print ("Deleting student in database")
            App.myDatabase.delete_student(newStudentID)
            print ("UI: Student deleted")
            st.success(f"Deleted student: {newUsername}")
            st.rerun()
    else:
        if submitted:
            if is_new_student:
                # Add new student
                newStudentID = App.myDatabase.generate_next_id()
                st.session_state.StudentsList[newUsername] = (newStudentID, newRole, newUsername, newPassword, newfName, newlName, newEmail, newPhone)
                print ("Creating student in database")
                App.myDatabase.create_student(newStudentID, newUsername, newPassword, newfName, newlName, newEmail, newPhone, newRole)
                print ("UI: Student created")
                st.success(f"Added new student: {newUsername} with role {newRole}")
                newStudentID = st.text_input("StudentID", value=newStudentID, disabled = True) 
        
            else:
                # Update existing student
                st.session_state.StudentsList.pop(studentSelection)
                st.session_state.StudentsList[newUsername] = (newStudentID, newRole, newUsername, newPassword, newfName, newlName, newEmail, newPhone)    
                print ("Updating student in database")
                App.myDatabase.update_student(newStudentID, newUsername, newPassword, newfName, newlName, newEmail, newPhone, newRole)
                print ("UI: Student updated")
                st.success(f"Updated student: {newUsername} to role {newRole}")
            st.rerun()