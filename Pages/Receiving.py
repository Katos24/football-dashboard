import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(layout="wide")
st.title("NFL Receiving Stats Viewer")

# CSV URLs by year
csv_urls = {
    '2024': "https://docs.google.com/spreadsheets/d/e/2PACX-1vSB3lqA0ukLtNUK9E_FwHfqs7z1hMFsqg-7Uz_qfD3RXr3h5m4lxw_i7HT8iNq2oLCBNp6D64BMsNcQ/pub?gid=972788191&single=true&output=csv",
    '2023': "https://docs.google.com/spreadsheets/d/e/2PACX-1vSB3lqA0ukLtNUK9E_FwHfqs7z1hMFsqg-7Uz_qfD3RXr3h5m4lxw_i7HT8iNq2oLCBNp6D64BMsNcQ/pub?gid=110992447&single=true&output=csv",
    '2022': "https://docs.google.com/spreadsheets/d/e/2PACX-1vSB3lqA0ukLtNUK9E_FwHfqs7z1hMFsqg-7Uz_qfD3RXr3h5m4lxw_i7HT8iNq2oLCBNp6D64BMsNcQ/pub?gid=174961977&single=true&output=csv",
    '2021': "https://docs.google.com/spreadsheets/d/e/2PACX-1vSB3lqA0ukLtNUK9E_FwHfqs7z1hMFsqg-7Uz_qfD3RXr3h5m4lxw_i7HT8iNq2oLCBNp6D64BMsNcQ/pub?gid=1512587819&single=true&output=csv",
    '2020': "https://docs.google.com/spreadsheets/d/e/2PACX-1vSB3lqA0ukLtNUK9E_FwHfqs7z1hMFsqg-7Uz_qfD3RXr3h5m4lxw_i7HT8iNq2oLCBNp6D64BMsNcQ/pub?gid=542561212&single=true&output=csv",
}



# Sidebar Filters
col1, col2 = st.columns([1, 2])
with col1:
    year = st.selectbox("Select Year", options=sorted(csv_urls.keys(), reverse=True))
with col2:
    min_1d = st.slider("Minimum First Downs", 0, 100, 25)

# Load Data
@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df

df = load_data(csv_urls[year])

# Filter data by minimum first downs
df_filtered = df[df["1D"] >= min_1d]

# Sort by '1D' descending for top 5 and for table display
df_filtered = df_filtered.sort_values(by="1D", ascending=False)

# Top 5 Players by First Downs
top5 = df_filtered.head(5)

# Top 5 Players by First Downs – Styled Cards (Receiving)
st.markdown(f"<h2 style='color:#1f77b4;'>📬 Top 5 Players in Receiving 1D ({year})</h2>", unsafe_allow_html=True)

receiving_gradients = [
    "linear-gradient(135deg, #E3F2FD, #BBDEFB)",
    "linear-gradient(135deg, #E8F5E9, #A5D6A7)",
    "linear-gradient(135deg, #FFF3E0, #FFCC80)",
    "linear-gradient(135deg, #F3E5F5, #CE93D8)",
    "linear-gradient(135deg, #ECEFF1, #B0BEC5)",
]

ordinal_suffixes = ["1st 🥇", "2nd 🥈", "3rd 🥉", "4th", "5th"]

card_cols = st.columns(5)

for i, (_, row) in enumerate(top5.iterrows()):
    player = row["Player"]
    team = row.get("Team", "")  # safer get
    first_downs = row["1D"]

    with card_cols[i]:
        st.markdown(
            f"""
            <div style="
                background: {receiving_gradients[i]};
                padding: 10px 12px;
                border-radius: 12px;
                box-shadow: 0 3px 8px rgba(0,0,0,0.2);
                text-align: center;
                color: #222;
                font-weight: 600;
                min-width: 200px;
                margin: 0 auto;
            ">
                <p style='
                    margin: 0 0 6px 0; 
                    font-size: 16px; 
                    font-weight: 700; 
                    color: #333;
                    letter-spacing: 1px;
                '>{ordinal_suffixes[i]}</p>
                <h4 style='
                    margin: 0 0 6px 0; 
                    font-size: 20px; 
                    font-weight: 900; 
                    color: #111; 
                    text-transform: uppercase;
                '>{player} ({team})</h4>
                <p style='font-size:18px; margin: 4px 0; color: #0d47a1; font-weight:700;'>
                    {first_downs} 1D
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )


# Add spacer before bar chart
st.markdown("<div style='margin-top:30px;'></div>", unsafe_allow_html=True)

# Top 10 Players by First Downs - Horizontal Bar Chart
top10 = df_filtered.head(10)

bar_chart = alt.Chart(top10).mark_bar().encode(
    y=alt.Y('Player:N', sort='-x', title=None),
    x=alt.X('1D:Q', title='First Downs'),
    color=alt.Color('Player:N', legend=None)
)

# Add text labels at the end of the bars
text = alt.Chart(top10).mark_text(
    align='left',
    baseline='middle',
    dx=3,
    color='white'   # <-- add this to make text white
).encode(
    y=alt.Y('Player:N', sort='-x'),
    x='1D:Q',
    text='1D:Q'
)

final_chart = bar_chart + text

st.altair_chart(final_chart, use_container_width=True)



# Display Filtered Data Table with index starting at 1
st.subheader("Filtered Receiving Stats")
df_display = df_filtered.reset_index(drop=True)
df_display.index = df_display.index + 1  # start index at 1
df_display.index.name = 'Rank'

st.dataframe(df_display)