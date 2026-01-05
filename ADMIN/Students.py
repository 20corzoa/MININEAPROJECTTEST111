import streamlit as st
from datetime import date
import pandas as pd
import App


st.header("Students Management")

# Load students from database
dbStudentsList = App.myDatabase.read_all_students() 

dbStudentsDict = dict()
for row in dbStudentsList:
    dbStudentsDict[row[1] + " " + row[2]] = row
print("DB Students Dict:" , dbStudentsDict.items())
st.session_state.StudentsList=dbStudentsDict 
# Display current students
dfList = pd.DataFrame(
    [(key, str(value[5]), value[6]) for key, value in st.session_state.StudentsList.items()],
    columns=['Name', 'Year Group','Form'])
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
    newfName = st.text_input("First Name",value="" if is_new_student else student_data[1])
    newlName = st.text_input("Last Name",value="" if is_new_student else student_data[2])
    newGender = st.selectbox("Gender", options=["Male", "Female", "Other"], index=0 if is_new_student else ["Male", "Female", "Other"].index(student_data[3]))
    newDOB = st.date_input("Date of Birth",value=date(2008, 1, 1) if is_new_student else student_data[4])
    newYear = st.selectbox("Year", options=[7,8,9,10,11,12,13], index=0 if is_new_student else [7,8,9,10,11,12,13].index(student_data[5]))
    newForm = st.selectbox("Form",options=["7E","7R","7S","7T","7B","7M","8E","8R","8S","8T","8B","8M","9E","9R","9S","9T","9B","9M","10E","10R","10S","10T","10B","10M","11E","11R","11S","11T","11B","11M","LE1","LE2","LR1","LR2","LS1","LS2","LT1","LT2","LB1","LB2","LM1","LM2","UE1","UE2","UR1","UR2","US1","US2","UT1","UT2","UB1","UB2","UM1","UM2"], index=0 if is_new_student else ["7E","7R","7S","7T","7B","7M","8E","8R","8S","8T","8B","8M","9E","9R","9S","9T","9B","9M","10E","10R","10S","10T","10B","10M","11E","11R","11S","11T","11B","11M","LE1","LE2","LR1","LR2","LS1","LS2","LT1","LT2","LB1","LB2","LM1","LM2","UE1","UE2","UR1","UR2","US1","US2","UT1","UT2","UB1","UB2","UM1","UM2"].index(student_data[6]))
    newHouse = st.selectbox("House", options=["Evans", "Morgan", "Rendall", "Taylor", "Starling", "Bryant"], index=0 if is_new_student else ["Evans", "Morgan", "Rendall", "Taylor", "Starling", "Bryant"].index(student_data[7]))
    newEmail = st.text_input("Email",value="" if is_new_student else student_data[8])
    newPhone = st.text_input("Phone Number",value="" if is_new_student else student_data[9])
    newConsent = st.checkbox("Parental Consent", value=False if is_new_student else (student_data[10]==1))
    newMedicalID = st.text_input("Medical Info ID", value="--" if is_new_student else student_data[11], disabled = True)
    newContactID = st.text_input("Emergency Contact ID", value="--" if is_new_student else student_data[12], disabled = True)
    buttonName = "Create" if is_new_student else "Submit Changes"
    submitted = st.form_submit_button(buttonName)
    deleted_button = False  
    if not is_new_student:
        deleted_button = True
        deleted = st.form_submit_button("Delete")   
        
  
    if deleted_button and deleted:
            # Delete student
            st.session_state.StudentsList.pop(studentSelection)
            print ("Deleting student in database")
            App.myDatabase.delete_student(newStudentID)
            print ("UI: Student deleted")
            st.success(f"Deleted student: {newfName} {newlName}")
            st.rerun()
    else:
        if submitted:
            if is_new_student:
                # Add new student
                newStudentID = App.myDatabase.generate_next_id()
                newMedicalID = App.myDatabase.generate_next_id()
                newContactID = App.myDatabase.generate_next_id()
                st.session_state.StudentsList[newStudentID] = (newStudentID, newfName, newlName, newGender, newDOB, newYear, newForm, newHouse, newEmail, newPhone, int(newConsent), newMedicalID, newContactID)
                print ("Creating student in database")
                App.myDatabase.create_student(newStudentID, newfName, newlName, newGender, newDOB, newYear, newForm, newHouse, newEmail, newPhone, newConsent,newMedicalID, newContactID)
                print ("UI: Student created")
                st.success(f"Added new student: {newfName} {newlName}")
                newStudentID = st.text_input("StudentID", value=newStudentID, disabled = True) 
                newMedicalID = st.text_input("Medical Info ID", value=newMedicalID, disabled = True) 
                newContactID = st.text_input("Emergency Contact ID", value=newContactID, disabled = True)        
            else:
                # Update existing student
                st.session_state.StudentsList.pop(studentSelection)
                st.session_state.StudentsList[newStudentID] = (newStudentID, newfName, newlName, newGender, newDOB, newYear, newForm, newHouse, newEmail, newPhone, int(newConsent), newMedicalID, newContactID)    
                print ("Updating student in database")
                App.myDatabase.update_student(newStudentID, newfName, newlName, newGender, newDOB, newYear, newForm, newHouse,  newEmail, newPhone, newConsent, newMedicalID, newContactID)
                print ("UI: Student updated")
                st.success(f"Updated student: {newfName} {newlName}")
            st.rerun()