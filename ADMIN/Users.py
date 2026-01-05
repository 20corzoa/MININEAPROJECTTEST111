import streamlit as st
import pandas as pd
import App


st.header("Users")

# Load users from database
dbUsersList = App.myDatabase.read_all_users() 

dbUsersDict = dict()
for row in dbUsersList:
    dbUsersDict[row[2]] = row
print("DB Users Dict:" , dbUsersDict.items())
st.session_state.UsersList=dbUsersDict 
# Display current users
dfList = pd.DataFrame(
    [(key, value[1]) for key, value in st.session_state.UsersList.items()],
    columns=['User', 'Role']
)
_ = dfList  # suppress implicit display
st.data_editor(dfList, disabled=True)

# Create a copy of userlist to form a dropdownlist and add the new user option 
userSelectionDropDown = dict()
for key in st.session_state.UsersList.copy():
    userSelectionDropDown[key] = "USER ID:" + str(st.session_state.UsersList[key][0])
userSelectionDropDown["Add New User"] = "N/A"


dfDropDown = pd.DataFrame([(key, value) for key, value in userSelectionDropDown.items()],
    columns=['User','UserId'])



# Select user from dropdown
userSelection = st.selectbox("Select User", options=dfDropDown['User'],format_func=lambda x: f"{x} ({userSelectionDropDown[x]})")

# new user ? 
is_new_user = userSelection == "Add New User"
# get data 
user_data = None if is_new_user else st.session_state.UsersList[userSelection]


#create form with user deai
with st.form("userForm"):
    st.subheader("User Details")


    newUserID = st.text_input("UserID", value="--" if is_new_user else user_data[0], disabled = True) 
    newUsername = st.text_input("Username", value="" if is_new_user else user_data[2])
    newRole = st.selectbox("Role", options=["Admin", "Teacher"], index=0 if is_new_user else ["Admin", "Teacher", "Student"].index(user_data[1]))
    newPassword = st.text_input("Password", type="password", value="" if is_new_user else user_data[3])
    newfName = st.text_input("First Name",value="" if is_new_user else user_data[4])
    newlName = st.text_input("Last Name",value="" if is_new_user else user_data[5])
    newEmail = st.text_input("Email",value="" if is_new_user else user_data[6])
    newPhone = st.text_input("Phone Number",value="" if is_new_user else user_data[7])
    
    buttonName = "Create" if is_new_user else "Submit Changes"
    submitted = st.form_submit_button(buttonName)
    deleted_button = False  
    if not is_new_user:
        deleted_button = True
        deleted = st.form_submit_button("Delete")   
        
  
    if deleted_button:
        if deleted:
            # Delete user
            st.session_state.UsersList.pop(userSelection)
            print ("Deleting user in database")
            App.myDatabase.delete_user(newUserID)
            print ("UI: User deleted")
            st.success(f"Deleted user: {newUsername}")
            st.rerun()
    else:
        if submitted:
            if is_new_user:
                # Add new user
                newUserID = App.myDatabase.generate_next_id()
                st.session_state.UsersList[newUsername] = (newUserID, newRole, newUsername, newPassword, newfName, newlName, newEmail, newPhone)
                print ("Creating user in database")
                App.myDatabase.create_user(newUserID, newUsername, newPassword, newfName, newlName, newEmail, newPhone, newRole)
                print ("UI: User created")
                st.success(f"Added new user: {newUsername} with role {newRole}")
                newUserID = st.text_input("UserID", value=newUserID, disabled = True) 
        
            else:
                # Update existing user
                st.session_state.UsersList.pop(userSelection)
                st.session_state.UsersList[newUsername] = (newUserID, newRole, newUsername, newPassword, newfName, newlName, newEmail, newPhone)    
                print ("Updating user in database")
                App.myDatabase.update_user(newUserID, newUsername, newPassword, newfName, newlName, newEmail, newPhone, newRole)
                print ("UI: User updated")
                st.success(f"Updated user: {newUsername} to role {newRole}")
            st.rerun()



