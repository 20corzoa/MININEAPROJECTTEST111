import streamlit as st

def login():
    st.title("JUDD TRIPS")                                         
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("LOGIN"):
        if username == "admin" and password == "password":   #This is where the authentication logic would go, called from a database 
            role = "ADMIN"
            st.session_state.role = role
            st.success("Login successful!")
            st.rerun()
        elif username == "teacher" and password == "password":
            role = "TEACHER"
            st.session_state.role = role
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password.")
                #Role is saved in session state for access control throughout the app after rerun

def Logout():
    st.session_state.role = None
    st.success("You have been logged out.")
    st.rerun()                                #Rerun the app to reflect the logout state in role

if "role" not in st.session_state:      #Gatekeeps access to the app only allowing logged in users to access it
    st.session_state.role = None

ROLES = [None, "ADMIN", "TEACHER", "STUDENT"]

role = st.session_state.role

logout_page = st.Page(Logout, title="Logout", icon=":material/logout:")
settings = st.Page("UNIVERSAL/Settings.py",title="Settings", icon=":material/settings:")

TeacherHome = st.Page("TEACHER/TeacherHome.py",title="Teacher Home", icon=":material/home:", default=(role=="TEACHER"))
Documents = st.Page("TEACHER/Documents.py",title="Documents", icon=":material/folder:")
EmergencyInfo = st.Page("TEACHER/EmergencyInfo.py",title="Emergency Info", icon=":material/info:")
TravelPlan = st.Page("TEACHER/TravelPlan.py",title="Travel Plan", icon=":material/flight:")
Register = st.Page("TEACHER/Register.py",title="Register", icon=":material/thumb_up:")

AdminHome = st.Page("ADMIN/AdminHome.py",title="Admin Home", icon=":material/home:", default=(role=="ADMIN"))
Accounts = st.Page("ADMIN/Accounts.py",title="Accounts", icon=":material/thumb_up:")
Calendar = st.Page("ADMIN/Calendar.py",title="Calendar", icon=":material/thumb_up:")
Trips = st.Page("ADMIN/Trips.py",title="Trips", icon=":material/thumb_up:")

account_pages = [logout_page, settings]
teacher_pages = [TeacherHome, Documents, EmergencyInfo, TravelPlan, Register]
admin_pages = [AdminHome, Accounts, Calendar, Trips]

st.title("JUDD TRIPS")
page_dict = {}
if role in ["ADMIN", "TEACHER"]:
    page_dict["Teachers"] = teacher_pages
if role == "ADMIN":
    page_dict["Admins"] = admin_pages

if len(page_dict) > 0:
    pg = st.navigation({"Account": account_pages} | page_dict)
else:
    pg = st.navigation([st.Page(login)])
pg.run()