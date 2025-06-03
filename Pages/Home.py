import streamlit as st

# Set page config
st.set_page_config(page_title="First Down | Football Stats Hub", layout="wide")

# Hide default Streamlit footer/menu
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# Hero Section (with football background image + overlay)
hero_bg_url = "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1950&q=80"

st.markdown(
    f"""
    <style>
    .hero {{
        position: relative;
        background-image: url('{hero_bg_url}');
        background-size: cover;
        background-position: center;
        height: 60vh;
        color: white;
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
        font-family: 'Arial Black', Gadget, sans-serif;
        letter-spacing: 2px;
    }}
    .hero-overlay {{
        position: absolute;
        inset: 0;
        background-color: rgba(0,0,0,0.6);
        z-index: 1;
    }}
    .hero-content {{
        position: relative;
        z-index: 2;
        max-width: 700px;
        padding: 20px;
    }}
    .hero h1 {{
        font-size: 3.5rem;
        margin-bottom: 0.5rem;
    }}
    .hero p {{
        font-size: 1.5rem;
        margin-bottom: 1.5rem;
    }}
    .btn-yellow {{
        background-color: #FBBF24;
        color: black;
        padding: 0.75rem 1.5rem;
        font-weight: bold;
        border-radius: 0.375rem;
        text-decoration: none;
        transition: background-color 0.3s ease;
        display: inline-block;
    }}
    .btn-yellow:hover {{
        background-color: #F59E0B;
        color: white;
    }}
    </style>
    <div class="hero">
        <div class="hero-overlay"></div>
        <div class="hero-content">
            <h1>Welcome to First Down</h1>
            <p>Your Home for Deep-Dive Football Stats</p>
            <a href="#features" class="btn-yellow">Explore Stats</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<br><br>", unsafe_allow_html=True)

# Features Section
st.markdown(
    '<h2 id="features" style="font-family: Arial Black, Gadget, sans-serif; text-align:center; margin-bottom:1rem;">Features</h2>',
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📊 Team Stats")
    st.write("View in-depth stats for teams, including offense, defense, and special teams performance.")

with col2:
    st.markdown("### 🏈 Player Stats")
    st.write("Explore passing, rushing, and receiving stats for individual players.")

with col3:
    st.markdown("### ⚡ Fast & Intuitive")
    st.write("Easy to navigate and quick loading, designed for fans and analysts alike.")

st.markdown("<br><hr>", unsafe_allow_html=True)

# Footer
st.markdown(
    """
    <footer style="text-align:center; padding:1rem 0; color:#555; font-size:0.9rem;">
    &copy; 2025 First Down. Built with ❤️ using Streamlit.
    </footer>
    """,
    unsafe_allow_html=True,
)