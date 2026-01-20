import streamlit as st
import databasetest as dbt
st.header("Documents")
st.write(f"You are logged in as {st.session_state.role}")
db = dbt.dataBase()
leaderID = st.session_state.get("userID")
documents = db.read_documents_by_leader(leaderID)
#st.write(documents)
if not documents:
    st.info("You have no assigned trips.")
else:
    for document in documents:
        destination = document[0]
        tickets = document[2]
        itinerary = document[3]
        st.subheader(f"Trip  -  {destination}")
        st.write(tickets)
        st.write(itinerary)

#print all documents for all trips the teacher is leading