import streamlit as st
import databasetest as dbt

def login():
    st.set_page_config(
    page_title="Marble | School Trip Management",
    page_icon="⚪",
    layout="wide"  )
    st.title("MARBLE SCHOOL TRIP MANAGEMENT SYSTEM")                                       
    username = st.text_input("Username")
    password = st.text_input("Password", type="password", autocomplete="off")
    #st.write(myDatabase.read_all_user()) 
    if st.button("LOGIN"):
        if myDatabase.verify_user(username, password) == True:
            roleID = myDatabase.read_user_role(username)
            role = "ADMIN" if roleID == "1" else "TEACHER"
            st.session_state.username = username
            st.session_state.userID = myDatabase.read_userID_from_username(username)
            st.session_state.role = role
            st.write(f"Logged in as {st.session_state.username} with role {st.session_state.role} and userID {st.session_state.userID}")
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password.")

def Logout():
    st.session_state.role = None
    st.success("You have been logged out.")
    st.rerun()                                #Rerun the app to reflect the logout state in role

st.markdown("""
    <style>
        /* Main background color */
        .stApp {
            background-color: #F5F5F5;
        }

        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #333333;
        }

        /* Sidebar text color */
        [data-testid="stSidebar"] .css-17l244g, [data-testid="stSidebar"] span {
            color: white;
        }

        /* Custom Button Styling (Electric Blue) */
        div.stButton > button:first-child {
            background-color: #0084FF;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 10px 24px;
            font-weight: bold;
        }

        /* Headings */
        h1, h2, h3 {
            color: #333333;
            font-family: 'Helvetica Neue', sans-serif;
        }
    </style>
    """, unsafe_allow_html=True)

st.logo("MARBLE LOGO.png", icon_image="MARBLE LOGO.png")
st.sidebar.markdown("---")


if "role" not in st.session_state:      #Gatekeeps access to the app only allowing logged in users to access it
    st.session_state.role = None

ROLES = [None, "ADMIN", "TEACHER"]

role = st.session_state.role

myDatabase = dbt.dataBase()

logout_page = st.Page(Logout, title="Logout", icon=":material/logout:")
settings = st.Page("UNIVERSAL/Settings.py",title="Settings", icon=":material/settings:")

TeacherHome = st.Page("TEACHER/TeacherHome.py",title="Teacher Home", icon=":material/home:", default=(role=="TEACHER"))
Documents = st.Page("TEACHER/Documents.py",title="Documents", icon=":material/folder:")
EmergencyInfo = st.Page("TEACHER/EmergencyInfo.py",title="Emergency Info", icon=":material/info:")
Register = st.Page("TEACHER/Register.py",title="Register", icon=":material/app_registration:")

AdminHome = st.Page("ADMIN/AdminHome.py",title="Admin Home", icon=":material/home:", default=(role=="ADMIN"))
Users = st.Page("ADMIN/Users.py",title="Users", icon=":material/people:")
Trips = st.Page("ADMIN/Trips.py",title="Trips", icon=":material/flight:")
TripStudents = st.Page("ADMIN/TripStudents.py",title="Trip Students", icon=":material/group_add:")
Students = st.Page("ADMIN/Students.py",title="Students", icon=":material/school:")

account_pages = [logout_page, settings]
teacher_pages = [TeacherHome, Documents, EmergencyInfo, Register]
admin_pages = [AdminHome, Users, Trips, Students, TripStudents]

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