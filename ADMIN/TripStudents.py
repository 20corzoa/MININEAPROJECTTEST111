import streamlit as st
st.header("Trip Students")
st.write(f"You are logged in as {st.session_state.role}")
import streamlit as st

# Example data
students = ["Amy", "Ben", "Cara", "Dan"]
trips = ["London", "Paris", "Berlin"]

# Persistent storage within the session
if "pairs" not in st.session_state:
    st.session_state.pairs = []

# Two dropdowns to pick a pair
student = st.selectbox("Select Student", students)
trip = st.selectbox("Select Trip", trips)

# Add selected pair
if st.button("Add Pair"):
    pair = f"{student} ↔ {trip}"
    if pair not in st.session_state.pairs:
        st.session_state.pairs.append(pair)

# Display stored pairs
st.write("Selected Pairs:")
st.listbox = st.selectbox("Pairs", st.session_state.pairs if st.session_state.pairs else ["(none yet)"])
