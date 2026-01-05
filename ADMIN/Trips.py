import streamlit as st
from datetime import date
import pandas as pd
import App

def load_users():
    # Load users from database
    dbUsersList = App.myDatabase.read_all_users()
    dbUsersDict = dict()
    for row in dbUsersList:
        dbUsersDict[row[2]] = row
    print("DB Users Dict:" , dbUsersDict.items())
    st.session_state.UsersList=dbUsersDict 
    #   Display current users

    # Create a copy of userlist to form a dropdownlist and add the new user option 
    userSelectionDropDown = dict()
    for key in st.session_state.UsersList.copy():
        userSelectionDropDown[key] = str(st.session_state.UsersList[key][0])
    return userSelectionDropDown





st.header("Trips Management")

# Load Trips from database
dbTripsList = App.myDatabase.read_all_trips() 

dbTripsDict = dict()
for row in dbTripsList:
    dbTripsDict[row[1]] = row
print("DB Trips Dict:" , dbTripsDict.items())

st.session_state.TripsList=dbTripsDict 

# Display current trips
dfList = pd.DataFrame(
    [(value[0],value[1],value[2],value[3],value[4]) for value in st.session_state.TripsList.values()],
    columns=['Trip ID', 'Destination', 'Start Date','End Date','Status'])

st.data_editor(dfList, disabled=True)

# Create a copy of studentlist to form a dropdownlist and add the new student option 
tripDropdown = dict()
for key in st.session_state.TripsList.copy():
    tripDropdown[key] = "Trip ID:" + str(st.session_state.TripsList[key][0])
tripDropdown["Add New Trip"] = "N/A"
dfDropDown = pd.DataFrame([(key, value) for key, value in tripDropdown.items()],
    columns=['Trip','TripId'])



# Select trip from dropdown
tripSelection = st.selectbox("Select Trip", options=dfDropDown['Trip'],format_func=lambda x: f"{x} ({tripDropdown[x]})")

# new trip ? 
is_new_trip = tripSelection == "Add New Trip"
# get data 
tripdata = None if is_new_trip else st.session_state.TripsList[tripSelection]


#create form with trip details
with st.form("tripForm"):
    st.subheader("Trip Details")
    dfDropDown = load_users()
    newTripID = st.text_input("TripID", value="--" if is_new_trip else tripdata[0], disabled = True) 
    newDestination = st.text_input("Destination",value="" if is_new_trip else tripdata[1])
    newStartDate = st.date_input("Start Date",value=date(2008, 1, 1) if is_new_trip else tripdata[2])
    newEndDate = st.date_input("End Date",value=date(2008, 1, 1) if is_new_trip else tripdata[3])
    newStatus = st.selectbox("Status", options=["Active", "Cancelled"], index=0 if is_new_trip else ["Active", "Cancelled"].index(tripdata[4]))
    if is_new_trip:
        tleaderid_index=0
    else:
        for id in dfDropDown.items():
            if int(tripdata[5]) == int(id[1]):
                tleaderid_index = list(dfDropDown.keys()).index(id[0])
    newLeader = st.selectbox("Leader", options=dfDropDown.keys(), index=tleaderid_index)
    buttonName = "Create" if is_new_trip else "Submit Changes"
    submitted = st.form_submit_button(buttonName)
    deleted_button = False  
    if not is_new_trip:
        deleted_button = True
        deleted = st.form_submit_button("Delete")   
        
  
    if deleted_button and deleted:
            # Delete trip
            st.session_state.TripsList.pop(tripSelection)
            print ("Deleting trip in database")
            App.myDatabase.delete_trip(newTripID)
            print ("UI: Trip deleted")
            st.success(f"Deleted trip: {newDestination}")
            st.rerun()
    else:
        if submitted:
            newTripID = App.myDatabase.generate_next_id()
            leaderID = dfDropDown[newLeader]
            print(dfDropDown[newLeader])            
            if is_new_trip:
                # Add new trip
                st.session_state.TripsList[newTripID] = (newTripID, newDestination, newStartDate, newEndDate, newStatus, leaderID)
                print ("Creating trip in database")
                App.myDatabase.create_trip(newTripID, newDestination, newStartDate, newEndDate, newStatus, leaderID)
                print ("UI: Trip created")
                st.success(f"Added new trip: {newDestination}")
                newTripID = st.text_input("TripID", value=newTripID, disabled = True)     
                
            else:
                # Update existing trip
                st.session_state.TripsList.pop(tripSelection)
                st.session_state.TripsList[newTripID] = (newTripID, newDestination, newStartDate, newEndDate, newStatus, leaderID)    
                print ("Updating trip in database")
                App.myDatabase.update_trip(newTripID, newDestination, newStartDate, newEndDate, newStatus, leaderID)
                print ("UI: Trip updated")
                st.success(f"Updated trip: {newDestination}")
            st.rerun()
