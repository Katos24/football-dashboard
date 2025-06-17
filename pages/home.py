import streamlit as st

st.set_page_config(page_title="First Down | Home", layout="wide")

st.markdown(
    """
    <style>
    .home-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 70vh;
        font-family: 'Arial Black', Gadget, sans-serif;
        color: #333;
        text-align: center;
        padding: 2rem;
    }
    .home-title {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    .home-subtitle {
        font-size: 1.5rem;
        margin-bottom: 2rem;
    }
    .home-instruction {
        font-size: 1.25rem;
        color: #555;
    }
    </style>

    <div class="home-container">
        <div class="home-title">Welcome to First Down</div>
        <div class="home-subtitle">Your Hub for Deep-Dive Football Stats</div>
        <div class="home-instruction">
            Please select a page from the sidebar to explore passing, rushing, receiving, team comparisons, and more.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)