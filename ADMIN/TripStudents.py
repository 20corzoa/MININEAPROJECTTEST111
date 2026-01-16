import streamlit as st
import pandas as pd
import App

def load_students():
    # Load students from database
    dbStudentsList = App.myDatabase.read_all_students()
    dbStudentsDict = dict()
    for row in dbStudentsList:
        #dictionmary key is the full name
        dbStudentsDict[row[1]+" "+row[2]] = row
    print("DB Students Dict:" , dbStudentsDict.items())
    #load to streamlit in studentlist
    st.session_state.StudentsList=dbStudentsDict 
    #   Display current students

    # Create a copy of studentlist to form a dropdownlist and add the new student option 
    studentSelectionDropDown = dict()
    for key in st.session_state.StudentsList.copy():
        studentSelectionDropDown[key] = str(st.session_state.StudentsList[key][0])
    return studentSelectionDropDown

dbTripsList = App.myDatabase.read_all_trips() 
dbTripsDict = dict()
for row in dbTripsList:
      dbTripsDict[row[1]] = row
st.session_state.TripsList=dbTripsDict 

st.header("Trip Students Management")
# Display current trips
dfList = pd.DataFrame(
    [(value[0],value[1],value[2],value[3],value[4]) for value in st.session_state.TripsList.values()],
    columns=['Trip ID', 'Destination', 'Start Date','End Date','Status'])
tripDropdown = dict()
for key in st.session_state.TripsList.copy():
    tripDropdown[key] = "Trip ID:" + str(st.session_state.TripsList[key][0])


dfDropDown = pd.DataFrame([(key, value) for key, value in tripDropdown.items()],
    columns=['Trip','TripId'])
# Persistent storage within the session
if "pairs" not in st.session_state:
    st.session_state.pairs = []

# Load students for dropdown
studentDropdown = load_students()
# Two dropdowns to pick a pair

trip = st.selectbox("Select Trip", dfDropDown['Trip'], format_func=lambda x: f"{x} ({tripDropdown[x]})") 
#st.session_state.pairs = App.myDatabase.get_trip_students(trip.split("(")[0].strip())
tripStudentIds = App.myDatabase.get_trip_students(trip.split("(")[0].strip())
print("Trip Student Ids:", tripStudentIds)
for studentLabel in studentDropdown.items():
    print("Checking studentLabel:", studentLabel)
    studentID = studentLabel[1]
    studentName = studentLabel[0]
    pairStr = f"{studentName} ↔ {trip}"
    print("Checking studentID %s in tripStudentIds %s", studentID, tripStudentIds)
    print("First id in tripStudentIds is:", tripStudentIds[0] if len(tripStudentIds)>0 else "None")
    studentInTrip = any( print(f"Comparing {studentID} with {tripListRow[0]}") or str(studentID).strip() == str(tripListRow[0]).strip() for tripListRow in tripStudentIds)
    print("Is student in trip?", studentInTrip)
    if studentInTrip:
        print("Adding pairStr to session state pairs:", pairStr)
        if pairStr not in st.session_state.pairs:
            st.session_state.pairs.append(pairStr)

#studentPlusTripPairs = [f"{name} ↔ {trip}" 
print(f"Loaded pairs from DB before %s and after %s:", st.session_state.pairs, st.session_state.pairs)
newStudent = st.selectbox("Student", list(studentDropdown.keys()), format_func=lambda x: f"{x} (Student ID:{studentDropdown[x]})")


# Add selected pair
choice1 = st.button("Add student")
choice2 = st.button("Remove student")

if choice1:
    pair = f"{newStudent} ↔ {trip}"
    if pair not in st.session_state.pairs:
        st.session_state.pairs.append(pair)
      # Update database with new pair
        #studentfName =  studentDropdown[newStudent].split(" ")[0]
        #studentlName =  studentDropdown
        #tripDestination = tripDropdown[trip].split("(")[0].strip()
        #print(trip,"->",tripDropdown[trip],tripDestination)
        App.myDatabase.assign_student_to_trip(trip, newStudent)
elif choice2:
    pair = f"{newStudent} ↔ {trip}"
    if pair in st.session_state.pairs:
        st.session_state.pairs.remove(pair)
        # Update database to remove pair
        #studentfName = studentDropdown[newStudent].split(" ")[0]
        #studentlName = studentDropdown[newStudent].split(" ")[1]
        tripDestination = tripDropdown[trip]
        App.myDatabase.remove_student_from_trip(trip, newStudent)

# Display stored pairs
st.write("Trip-Student table going to:" + trip)
st.text_area("", value="\n".join(st.session_state.pairs), height=200)