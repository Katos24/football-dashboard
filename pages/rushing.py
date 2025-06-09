import streamlit as st
import pandas as pd
import altair as alt

# --------------------------
# URLs for CSV by year
# --------------------------
csv_urls = {
    '2024': "https://docs.google.com/spreadsheets/d/e/2PACX-1vRf8IihZAe5eWGCyglTOuc0TNpYi8M5OY9LmHI90BlGvUTbh4zHQqxZnm_oeioI3SdJnzwLWoYN1qPC/pub?gid=574291986&single=true&output=csv",
    '2023': "https://docs.google.com/spreadsheets/d/e/2PACX-1vRf8IihZAe5eWGCyglTOuc0TNpYi8M5OY9LmHI90BlGvUTbh4zHQqxZnm_oeioI3SdJnzwLWoYN1qPC/pub?gid=1218519657&single=true&output=csv",
    '2022': "https://docs.google.com/spreadsheets/d/e/2PACX-1vRf8IihZAe5eWGCyglTOuc0TNpYi8M5OY9LmHI90BlGvUTbh4zHQqxZnm_oeioI3SdJnzwLWoYN1qPC/pub?gid=107479071&single=true&output=csv",
    '2021': "https://docs.google.com/spreadsheets/d/e/2PACX-1vRf8IihZAe5eWGCyglTOuc0TNpYi8M5OY9LmHI90BlGvUTbh4zHQqxZnm_oeioI3SdJnzwLWoYN1qPC/pub?gid=1376297477&single=true&output=csv",
    '2020': "https://docs.google.com/spreadsheets/d/e/2PACX-1vRf8IihZAe5eWGCyglTOuc0TNpYi8M5OY9LmHI90BlGvUTbh4zHQqxZnm_oeioI3SdJnzwLWoYN1qPC/pub?gid=1118278232&single=true&output=csv",
}

# --------------------------
# Streamlit Page Config and Title
# --------------------------
st.set_page_config(page_title="NFL Rushing 1D Stats", layout="wide")
st.title("🏈 NFL Rushing First Down Stats")

# --------------------------
# Cached Data Loaders
# --------------------------
@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    # Clean 'Rushing First Down Rate' safely
    df['Rushing First Down Rate'] = pd.to_numeric(df['Rushing First Down Rate'].str.rstrip('%'), errors='coerce').fillna(0)
    df['YPC'] = (df['Yds'] / df['Att']).round(2)
    return df

@st.cache_data
def load_combined_years(years):
    dfs = []
    for y in years:
        df_year = load_data(csv_urls[y])
        dfs.append(df_year)
    df_all = pd.concat(dfs, ignore_index=True)
    return df_all



# --------------------------
# Filter Section for Single Year View
# --------------------------
col1, col2 = st.columns([1, 3])
with col1:
    year = st.selectbox("Select Year", options=sorted(csv_urls.keys(), reverse=True))

# Load data for selected year
df = load_data(csv_urls[year])
df_sorted = df.sort_values(by="1D", ascending=False).reset_index(drop=True)
df_sorted.index = df_sorted.index + 1
df_sorted.index.name = "Rank"

# Slider filter for 1D
min_1d = int(df_sorted['1D'].min())
max_1d = int(df_sorted['1D'].max())
with col2:
    selected_1d_range = st.slider("Filter by 1D (First Downs)", min_1d, max_1d, (min_1d, max_1d))

filtered_df = df_sorted[
    (df_sorted['1D'] >= selected_1d_range[0]) &
    (df_sorted['1D'] <= selected_1d_range[1])
]

# --------------------------
# Top 5 Players Cards Section
# --------------------------
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

st.markdown("<br><br>", unsafe_allow_html=True)


# --------------------------
# Top 10 Bar Chart Section
# --------------------------
top10 = filtered_df.head(10).copy()
top10['1D'] = top10['1D'].astype(float)

bar_chart = alt.Chart(top10).mark_bar().encode(
    y=alt.Y('Player:N', sort='-x', title=None),
    x=alt.X('1D:Q', title='First Downs'),
    color=alt.Color('Player:N', legend=None)
)

text = alt.Chart(top10).mark_text(
    align='left',
    baseline='middle',
    dx=3,
    color='white'
).encode(
    y=alt.Y('Player:N', sort='-x'),
    x='1D:Q',
    text='1D:Q'
)

final_chart = bar_chart + text

st.altair_chart(final_chart, use_container_width=True)

# --------------------------
# Year Highlights
# --------------------------
# Aggregate stats for selected year
num_cols = ['1D', 'Rushing First Down Rate', 'Explosiveness', 'Att', 'Yds']
df_sorted[num_cols] = df_sorted[num_cols].apply(pd.to_numeric, errors='coerce').fillna(0)
agg = df_sorted.groupby('Player').agg({
    '1D': 'sum',
    'Rushing First Down Rate': 'mean',
    'Explosiveness': 'mean',
    'Att': 'sum',
    'Yds': 'sum',
}).reset_index()
agg['YPC'] = agg['Yds'] / agg['Att']
agg_filtered = agg[agg['Att'] >= 100]

# Get top players by metric for the selected year
top = {
    'Most 1D': agg.loc[agg['1D'].idxmax()],
    'Highest 1D Rate': agg.loc[agg['Rushing First Down Rate'].idxmax()],
    'Highest Explosiveness': agg.loc[agg['Explosiveness'].idxmax()],
    'Most Attempts': agg.loc[agg['Att'].idxmax()],
    'Most Yards': agg.loc[agg['Yds'].idxmax()],
    'Highest YPC (100+ Att)': agg_filtered.loc[agg_filtered['YPC'].idxmax()],
}

# Display summary below cards
summary_html = f"""
<ul style="font-size: 14px; line-height: 1.3; padding-left: 1.2em; margin-top: 0; margin-bottom: 0;">
  <li><b>Most 1D:</b> {top['Most 1D']['Player']} ({int(top['Most 1D']['1D'])})</li>
  <li><b>Highest 1D Rate:</b> {top['Highest 1D Rate']['Player']} ({top['Highest 1D Rate']['Rushing First Down Rate']:.2f}%)</li>
  <li><b>Highest Explosiveness:</b> {top['Highest Explosiveness']['Player']} ({top['Highest Explosiveness']['Explosiveness']:.2f})</li>
  <li><b>Most Attempts:</b> {top['Most Attempts']['Player']} ({int(top['Most Attempts']['Att'])})</li>
  <li><b>Most Yards:</b> {top['Most Yards']['Player']} ({int(top['Most Yards']['Yds'])})</li>
  <li><b>Highest YPC (100+ Att):</b> {top['Highest YPC (100+ Att)']['Player']} ({top['Highest YPC (100+ Att)']['YPC']:.2f})</li>
</ul>
"""

st.markdown("### 🏆 Top Highlights for " + year)
st.markdown(summary_html, unsafe_allow_html=True)
st.markdown("---")




# --------------------------
# Full Table Section
# --------------------------
st.subheader(f"📊 Full Rushing Table (First Downs) – {year}")
st.markdown(f"""
<p style='color:gray; font-size:14px;'>
📅 Stats below reflect the selected year: <strong>{year}</strong>.  
To view a different season, use the <em>Select Year</em> dropdown above.
</p>
""", unsafe_allow_html=True)

search_term = st.text_input("Search for a player:")

df_display = filtered_df.copy()
if search_term:
    df_display = df_display[df_display['Player'].str.contains(search_term, case=False, na=False)]

df_display = df_display.reset_index(drop=True)
df_display.index += 1
df_display.index.name = 'Rank'

st.dataframe(
    df_display.style
        .format({'Rushing First Down Rate': '{:.2f}%', 'YPC': '{:.2f}'})
        .set_properties(**{'text-align': 'left'}),
    use_container_width=True
)

# --------------------------
# Glossary Expander Section
# --------------------------
with st.expander("ℹ️ Glossary"):
    st.markdown("""
    - **1D**: Rushing first downs
    - **Yds**: Total rushing yards
    - **YPC**: Yards per carry
    - **TD**: Touchdowns
    - **Rushing First Down Rate**: % of carries resulting in a 1st down
    - **Explosiveness**: A metric indicating how impactful a player's first down runs are, reflecting both frequency and yardage.
    """)

