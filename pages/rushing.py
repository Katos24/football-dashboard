import streamlit as st
import pandas as pd
import altair as alt

# URLs for CSV by year
csv_urls = {
    '2024': "https://docs.google.com/spreadsheets/d/e/2PACX-1vRf8IihZAe5eWGCyglTOuc0TNpYi8M5OY9LmHI90BlGvUTbh4zHQqxZnm_oeioI3SdJnzwLWoYN1qPC/pub?gid=574291986&single=true&output=csv",
    '2023': "https://docs.google.com/spreadsheets/d/e/2PACX-1vRf8IihZAe5eWGCyglTOuc0TNpYi8M5OY9LmHI90BlGvUTbh4zHQqxZnm_oeioI3SdJnzwLWoYN1qPC/pub?gid=1218519657&single=true&output=csv",
    '2022': "https://docs.google.com/spreadsheets/d/e/2PACX-1vRf8IihZAe5eWGCyglTOuc0TNpYi8M5OY9LmHI90BlGvUTbh4zHQqxZnm_oeioI3SdJnzwLWoYN1qPC/pub?gid=107479071&single=true&output=csv",
    '2021': "https://docs.google.com/spreadsheets/d/e/2PACX-1vRf8IihZAe5eWGCyglTOuc0TNpYi8M5OY9LmHI90BlGvUTbh4zHQqxZnm_oeioI3SdJnzwLWoYN1qPC/pub?gid=1376297477&single=true&output=csv",
    '2020': "https://docs.google.com/spreadsheets/d/e/2PACX-1vRf8IihZAe5eWGCyglTOuc0TNpYi8M5OY9LmHI90BlGvUTbh4zHQqxZnm_oeioI3SdJnzwLWoYN1qPC/pub?gid=1118278232&single=true&output=csv",
}

st.set_page_config(page_title="NFL Rushing 1D Stats", layout="wide")
st.title("🏈 NFL Rushing First Down Stats")

# Filter Section
col1, col2 = st.columns([1, 3])
with col1:
    year = st.selectbox("Select Year", options=sorted(csv_urls.keys(), reverse=True))

@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    # Clean 'Rushing First Down Rate' safely
    df['Rushing First Down Rate'] = pd.to_numeric(df['Rushing First Down Rate'].str.rstrip('%'), errors='coerce').fillna(0)
    df['YPC'] = (df['Yds'] / df['Att']).round(2)
    return df

df = load_data(csv_urls[year])
df_sorted = df.sort_values(by="1D", ascending=False).reset_index(drop=True)
df_sorted.index = df_sorted.index + 1
df_sorted.index.name = "Rank"

min_1d = int(df_sorted['1D'].min())
max_1d = int(df_sorted['1D'].max())
with col2:
    selected_1d_range = st.slider("Filter by 1D (First Downs)", min_1d, max_1d, (min_1d, max_1d))

filtered_df = df_sorted[
    (df_sorted['1D'] >= selected_1d_range[0]) &
    (df_sorted['1D'] <= selected_1d_range[1])
]



# Top 5 in 1D – Styled like Top 3 cards
st.markdown(f"<h2 style='color:#1f77b4;'>🏃‍♂️ Top 5 Players in Rushing 1D ({year})</h2>", unsafe_allow_html=True)

top5 = df_sorted.head(5)
card_cols = st.columns(5)

rushing_gradients = [
    "linear-gradient(135deg, #E3F2FD, #BBDEFB)",
    "linear-gradient(135deg, #E8F5E9, #A5D6A7)",
    "linear-gradient(135deg, #FFF3E0, #FFCC80)",
    "linear-gradient(135deg, #F3E5F5, #CE93D8)",
    "linear-gradient(135deg, #ECEFF1, #B0BEC5)",
]

ordinal_suffixes = ["1st 🥇", "2nd 🥈", "3rd 🥉", "4th", "5th"]

for i, (index, row) in enumerate(top5.iterrows()):
    player = row["Player"]
    one_d = row["1D"]
    rank_label = ordinal_suffixes[i]

    with card_cols[i]:
        st.markdown(
            f"""
            <div style="
                background: {rushing_gradients[i]};
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
                '>{rank_label}</p>
                <h4 style='
                    margin: 0 0 6px 0; 
                    font-size: 20px; 
                    font-weight: 900; 
                    color: #111; 
                    text-transform: uppercase;
                '>{player}</h4>
                <p style='font-size:18px; margin: 4px 0; color: #0d47a1; font-weight:700;'>
                    {one_d} 1D
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )


# Add vertical space
st.markdown("<br><br>", unsafe_allow_html=True)


top10 = filtered_df.head(10).copy()

# Ensure numeric column is float/int (Altair can be picky)
top10['1D'] = top10['1D'].astype(float)

# Bar chart
bars = alt.Chart(top10).mark_bar(color="#1f77b4").encode(
    x=alt.X('1D:Q', title='First Downs'),
    y=alt.Y('Player:N', sort='-x', title='Player'),
    tooltip=['Player', '1D', 'Yds', 'TD']
)

# Text labels on bars
labels = alt.Chart(top10).mark_text(
    align='left',
    baseline='middle',
    dx=3,
    fontSize=12,
    color='white'  # 👈 change here
).encode(
    x=alt.X('1D:Q'),
    y=alt.Y('Player:N', sort='-x'),
    text=alt.Text('1D:Q')
)

# Layer both
chart = (bars + labels).properties(height=300)

st.altair_chart(chart, use_container_width=True)



# Full Table
st.subheader(f"📊 Full Rushing Table – {year}")
st.dataframe(
    filtered_df.style
        .format({'Rushing First Down Rate': '{:.2f}%', 'YPC': '{:.2f}'})
        .set_properties(**{'text-align': 'left'}),
    use_container_width=True
)


