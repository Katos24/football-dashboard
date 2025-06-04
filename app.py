import streamlit as st

with st.sidebar:
    st.header("Your Sidebar Header")
    st.selectbox("Choose a page:", ["Home", "Stats", "Compare"])

st.title("Welcome to the Football Dashboard!")