import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# CSV URLs for each year
csv_urls = {
    '2024': "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ8nXQrw7rxiNxNFCHAcmPcZsKzH3f_CnYX7ZIijsduJ-suI4lPUyxbAL0HFH14E7xMv5IW-Ov8t6cM/pub?gid=0&single=true&output=csv",
    '2023': "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ8nXQrw7rxiNxNFCHAcmPcZsKzH3f_CnYX7ZIijsduJ-suI4lPUyxbAL0HFH14E7xMv5IW-Ov8t6cM/pub?gid=891552912&single=true&output=csv",
    '2022': "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ8nXQrw7rxiNxNFCHAcmPcZsKzH3f_CnYX7ZIijsduJ-suI4lPUyxbAL0HFH14E7xMv5IW-Ov8t6cM/pub?gid=1500595878&single=true&output=csv",
    '2021': "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ8nXQrw7rxiNxNFCHAcmPcZsKzH3f_CnYX7ZIijsduJ-suI4lPUyxbAL0HFH14E7xMv5IW-Ov8t6cM/pub?gid=1119294445&single=true&output=csv",
    '2020': "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ8nXQrw7rxiNxNFCHAcmPcZsKzH3f_CnYX7ZIijsduJ-suI4lPUyxbAL0HFH14E7xMv5IW-Ov8t6cM/pub?gid=1068926879&single=true&output=csv",
}

team_conference = {
    'Detroit Lions': 'NFC', 'Tampa Bay Buccaneers': 'NFC', 'Baltimore Ravens': 'AFC',
    'Washington Commanders': 'NFC', 'Cincinnati Bengals': 'AFC', 'Buffalo Bills': 'AFC',
    'Philadelphia Eagles': 'NFC', 'Atlanta Falcons': 'NFC', 'Arizona Cardinals': 'NFC',
    'Minnesota Vikings': 'NFC', 'San Francisco 49ers': 'NFC', 'Kansas City Chiefs': 'AFC',
    'Miami Dolphins': 'AFC', 'Green Bay Packers': 'NFC', 'Los Angeles Rams': 'NFC',
    'Seattle Seahawks': 'NFC', 'Dallas Cowboys': 'NFC', 'Pittsburgh Steelers': 'AFC',
    'Los Angeles Chargers': 'AFC', 'Denver Broncos': 'AFC', 'Indianapolis Colts': 'AFC',
    'New York Jets': 'AFC', 'Las Vegas Raiders': 'AFC', 'Tennessee Titans': 'AFC',
    'Houston Texans': 'AFC', 'New Orleans Saints': 'NFC', 'Cleveland Browns': 'AFC',
    'New England Patriots': 'AFC', 'New York Giants': 'NFC', 'Jacksonville Jaguars': 'AFC',
    'Chicago Bears': 'NFC', 'Carolina Panthers': 'NFC',
}


st.markdown("<h1 style='color:#1f77b4;'>NFL First Down Stats Dashboard</h1>", unsafe_allow_html=True)

# Select year
selected_year = st.selectbox("Select Year", options=sorted(csv_urls.keys(), reverse=True), index=0)

# Load data for selected year
df = pd.read_csv(csv_urls[selected_year])
df['Conference'] = df['TEAM'].map(team_conference)


# Top 3 team cards
top3 = df.nlargest(3, 'TOTAL')
st.markdown(f"<h2 style='color:#1f77b4;'>Top 3 Teams in Total First Downs ({selected_year})</h2>", unsafe_allow_html=True)
card_cols = st.columns(3)

# Gradient backgrounds for gold, silver, bronze
gradients = [
    "linear-gradient(135deg, #FFD700, #FFC300)",   # Gold
    "linear-gradient(135deg, #C0C0C0, #A9A9A9)",   # Silver
    "linear-gradient(135deg, #CD7F32, #B87333)"    # Bronze
]

for i, row in top3.iterrows():
    with card_cols[i]:
        st.markdown(
            f"""
            <div style="
                background: {gradients[i]};
                padding: 10px 12px;
                border-radius: 12px;
                box-shadow: 0 3px 8px rgba(0,0,0,0.2);
                text-align: center;
                color: #222;
                font-weight: 600;
                min-width: 260px;
                margin: 0 auto;
            ">
                <h4 style='
                    margin: 0 0 6px 0; 
                    font-size: 22px; 
                    font-weight: 900; 
                    color: #111; 
                    text-shadow: 1px 1px 2px rgba(255,255,255,0.7);
                    text-transform: uppercase;
                    letter-spacing: 1.5px;
                    text-align: center;
                '>{row['TEAM']}</h4>
                <p style='font-size:18px; margin: 4px 0; color: #111; font-weight:700;'>
                    {row['TOTAL']} Total
                </p>
                <p style='font-size:13px; margin: 2px 0;'>
                    Pass: {row['PASS']} | Rush: {row['RUSH']} | Pen: {row['PEN']}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )



# Top 10 for each category
top_total = df.nlargest(10, 'TOTAL')
top_pass = df.nlargest(10, 'PASS')
top_rush = df.nlargest(10, 'RUSH')
top_pen = df.nlargest(10, 'PEN')

# Create Plotly bar charts with value labels on top
fig_total = px.bar(
    top_total, x="TEAM", y="TOTAL",
    color="TEAM",
    color_discrete_sequence=px.colors.sequential.Viridis,
    text="TOTAL"
)
fig_total.update_traces(textposition='auto')

fig_pass = px.bar(
    top_pass, x="TEAM", y="PASS",
    color="TEAM",
    color_discrete_sequence=px.colors.sequential.Plasma,
    text="PASS"
)
fig_pass.update_traces(textposition='auto')

fig_rush = px.bar(
    top_rush, x="TEAM", y="RUSH",
    color="TEAM",
    color_discrete_sequence=px.colors.sequential.Magma,
    text="RUSH"
)
fig_rush.update_traces(textposition='auto')

fig_pen = px.bar(
    top_pen, x="TEAM", y="PEN",
    color="TEAM",
    color_discrete_sequence=px.colors.sequential.Cividis,
    text="PEN"
)
fig_pen.update_traces(textposition='auto')

# Tabs for charts
tabs = st.tabs([
    f"🏈 {selected_year} Total First Downs",
    f"🎯 {selected_year} Passing First Downs",
    f"🏃‍♂️ {selected_year} Rushing First Downs",
    f"🚫 {selected_year} Penalty First Downs"
])

with tabs[0]:
    st.markdown(f"<h3 style='color:#6a0dad;'>{selected_year} Top 10 Total First Downs</h3>", unsafe_allow_html=True)
    st.plotly_chart(fig_total, use_container_width=True)

with tabs[1]:
    st.markdown(f"<h3 style='color:#ff6347;'>{selected_year} Top 10 Passing First Downs</h3>", unsafe_allow_html=True)
    st.plotly_chart(fig_pass, use_container_width=True)

with tabs[2]:
    st.markdown(f"<h3 style='color:#2e8b57;'>{selected_year} Top 10 Rushing First Downs</h3>", unsafe_allow_html=True)
    st.plotly_chart(fig_rush, use_container_width=True)

with tabs[3]:
    st.markdown(f"<h3 style='color:#ff1493;'>{selected_year} Top 10 Penalty First Downs</h3>", unsafe_allow_html=True)
    st.plotly_chart(fig_pen, use_container_width=True)

st.markdown("---")



# --- Filter Section (on top of the table) ---

st.markdown(f"### Team First Down Stats ({selected_year})")

# Conference filter dropdown
conferences = ['All'] + sorted(df['Conference'].dropna().unique().tolist())
selected_conf = st.selectbox("Select Conference", conferences)

# Filter df by conference
if selected_conf != 'All':
    df_filtered = df[df['Conference'] == selected_conf]
else:
    df_filtered = df.copy()

# Total First Downs slider
min_total = int(df_filtered['TOTAL'].min())
max_total = int(df_filtered['TOTAL'].max())
total_range = st.slider("Total First Downs Range", min_value=min_total, max_value=max_total, value=(min_total, max_total))

df_filtered = df_filtered[(df_filtered['TOTAL'] >= total_range[0]) & (df_filtered['TOTAL'] <= total_range[1])]

# Prepare and show filtered dataframe sorted by TOTAL desc, with index starting at 1
df_display = df_filtered.sort_values(by='TOTAL', ascending=False).reset_index(drop=True)
df_display.index = df_display.index + 1

st.dataframe(df_display, use_container_width=True, height=400)







# --- Historic First Downs Line Chart ---

st.markdown("### 📈 Historic First Downs Line Chart (Team Over Years)")
st.markdown("Visualize how TOTAL, RUSH, PASS, and PEN first downs changed year-over-year.")

# Load and combine full data for all years
full_dfs = []
for year, url in csv_urls.items():
    temp_df = pd.read_csv(url)
    temp_df = temp_df[['TEAM', 'TOTAL', 'RUSH', 'PASS', 'PEN']].copy()
    temp_df['YEAR'] = int(year)
    full_dfs.append(temp_df)

historic_full = pd.concat(full_dfs).sort_values(by=['TEAM', 'YEAR'], ascending=[True, True]).reset_index(drop=True)

# Select team to plot
team_options = sorted(historic_full['TEAM'].unique())
with st.expander("📊 Historic Team Selector", expanded=True):
    selected_team_hist = st.selectbox("Select Team for Historic Chart", team_options)

# Filter data for selected team
team_df = historic_full[historic_full['TEAM'] == selected_team_hist]

# Melt the DataFrame for easier plotting with Plotly
team_melted = team_df.melt(id_vars=['YEAR'], value_vars=['TOTAL', 'RUSH', 'PASS', 'PEN'], 
                           var_name='Category', value_name='First Downs')

# Create line chart
fig = px.line(
    team_melted,
    x='YEAR',
    y='First Downs',
    color='Category',
    markers=True,
    title=f"{selected_team_hist} First Downs by Type Over Time",
    color_discrete_map={
        'TOTAL': '#1f77b4',
        'RUSH': '#2ca02c',
        'PASS': '#ff7f0e',
        'PEN': '#d62728'
    }
)
fig.update_layout(xaxis=dict(dtick=1))

st.plotly_chart(fig, use_container_width=True)